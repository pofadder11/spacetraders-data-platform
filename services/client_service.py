# services/client_service.py
from __future__ import annotations

import os
from dotenv import load_dotenv
import inspect
from typing import Any, Callable, Dict
import time
import threading
import json

import openapi_client
import openapi_client.api as api_pkg


def _camel_to_snake(name: str) -> str:
    out = []
    for i, c in enumerate(name):
        if c.isupper() and i > 0 and (not name[i - 1].isupper()):
            out.append("_")
        out.append(c.lower())
    return "".join(out)


class _DataApiProxy:
    """
    Wraps a generated *Api instance so that any method call returns
    `result.data` when available, otherwise returns `result` unchanged.
    """

    def __init__(self, api_instance: Any, service: "OpenAPIService") -> None:
        self._api = api_instance
        self._svc = service

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._api, name)
        if callable(attr):
            def _call(*args, **kwargs):
                # Token-bucket throttle and 429-aware retry
                attempts = 0
                while True:
                    attempts += 1
                    self._svc._throttle()
                    try:
                        res = attr(*args, **kwargs)
                        return getattr(res, "data", res)
                    except Exception as e:  # openapi_client.exceptions.ApiException
                        # Try to read headers/status/body
                        status = getattr(e, "status", None) or getattr(getattr(e, "response", None), "status", None)
                        headers = getattr(e, "headers", None) or getattr(getattr(e, "response", None), "headers", None) or {}
                        body = getattr(e, "body", None)
                        retry_after = None
                        if isinstance(headers, dict):
                            ra = headers.get("Retry-After")
                            try:
                                if ra is not None:
                                    retry_after = float(ra)
                            except Exception:
                                retry_after = None
                        if retry_after is None and body:
                            try:
                                data = json.loads(body)
                                retry_after = float(data.get("error", {}).get("data", {}).get("retryAfter", 0)) or None
                            except Exception:
                                retry_after = None
                        if status == 429 or retry_after is not None:
                            # backoff and retry a few times
                            self._svc._throttle(retry_after or 0.7)
                            if attempts < 5:
                                continue
                        # Not rate-limit or retries exhausted
                        raise
            _call.__name__ = getattr(attr, "__name__", name)
            _call.__doc__ = getattr(attr, "__doc__", None)
            return _call
        return attr


class _Namespace:
    """
    Simple attribute namespace backed by a dict.
    """
    def __init__(self, mapping: Dict[str, Any]) -> None:
        self.__dict__.update(mapping)

    def __repr__(self) -> str:
        keys = ", ".join(sorted(self.__dict__.keys()))
        return f"<Namespace [{keys}]>"


class OpenAPIService:
    """
    DRY façade around openapi_client.

    - Configures bearer token once
    - Creates one ApiClient
    - Auto-loads all *Api classes
    - Exposes both CamelCase and snake_case: e.g., `svc.SystemsApi` and `svc.systems`
    - `svc.d` exposes “data-proxy” APIs: `svc.d.systems.get_system(..)` returns .data automatically
    - `svc.call("systems.get_system", ...)` and `svc.call_data(...)` helpers
    """

    def __init__(
        self,
        bearer_token: str | None = None,
        host: str | None = None,
        user_agent: str | None = None,
        configure: Callable[[openapi_client.Configuration], None] | None = None,
    ) -> None:
        load_dotenv()
        token = bearer_token or os.getenv("BEARER_TOKEN")
        if not token:
            raise RuntimeError("Missing BEARER_TOKEN")

        cfg = openapi_client.Configuration(access_token=token)
        if host:
            cfg.host = host
        if user_agent:
            cfg.user_agent = user_agent
        if configure:
            configure(cfg)

        self._client = openapi_client.ApiClient(cfg)
        # Simple thread-safe token bucket for rate limiting
        self._rate_capacity = float(os.getenv("API_RATE_BURST", 30))
        self._rate_per_sec = float(os.getenv("API_RATE_PER_SEC", 2))
        self._tokens = self._rate_capacity
        self._last_refill = time.monotonic()
        self._rate_lock = threading.Lock()
        self._apis: Dict[str, Any] = {}
        self._data_apis: Dict[str, Any] = {}
        self._bind_all_apis()

        # Namespaces for convenient access
        self.apis = _Namespace(self._apis)
        self.d = _Namespace(self._data_apis)  # data-proxy namespace

    def _throttle(self, extra_sleep: float | None = None) -> None:
        """Block to respect a burst/steady rate. Optionally sleep extra (Retry-After)."""
        if extra_sleep and extra_sleep > 0:
            time.sleep(extra_sleep)
        with self._rate_lock:
            now = time.monotonic()
            # Refill tokens
            elapsed = now - self._last_refill
            if elapsed > 0:
                self._tokens = min(self._rate_capacity, self._tokens + elapsed * self._rate_per_sec)
                self._last_refill = now
            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return
            # Need to wait for next token
            needed = 1.0 - self._tokens
            wait = max(0.0, needed / self._rate_per_sec)
        # release lock while sleeping
        if wait > 0:
            time.sleep(wait)
        with self._rate_lock:
            # consume token after sleep
            self._tokens = max(0.0, self._tokens - 1.0)

    def _bind_all_apis(self) -> None:
        for attr in dir(api_pkg):
            if not attr.endswith("Api"):
                continue
            obj = getattr(api_pkg, attr, None)
            if not inspect.isclass(obj):
                continue

            instance = obj(self._client)
            data_proxy = _DataApiProxy(instance, self)

            # Expose CamelCase
            setattr(self, attr, instance)
            self._apis[attr] = instance

            # Expose snake_case alias without 'Api'
            base = attr[:-3]  # drop "Api"
            snake = _camel_to_snake(base)
            # Avoid Python keyword 'global'
            if snake == "global":
                snake = "global_api"

            setattr(self, snake, instance)
            self._apis[snake] = instance

            # Data-proxy aliases
            self._data_apis[attr] = data_proxy
            self._data_apis[snake] = data_proxy
            setattr(self, f"{snake}_data", data_proxy)  # optional explicit alias: systems_data, etc.

    def get_api(self, name: str) -> Any:
        try:
            return self._apis[name]
        except KeyError:
            raise AttributeError(f"No such API: {name!r}. Available: {sorted(self._apis.keys())}")

    def get_data_api(self, name: str) -> Any:
        try:
            return self._data_apis[name]
        except KeyError:
            raise AttributeError(f"No such data API: {name!r}. Available: {sorted(self._data_apis.keys())}")

    def call(self, qualified: str, *args, **kwargs) -> Any:
        """
        Call by 'systems.get_system' or 'SystemsApi.get_system'.
        Returns raw result (may include .data).
        """
        if "." not in qualified:
            raise ValueError("Use 'ApiName.method' or 'alias.method', e.g., 'systems.get_system'")
        api_name, method_name = qualified.split(".", 1)
        api = self.get_api(api_name)
        method = getattr(api, method_name, None)
        if not callable(method):
            raise AttributeError(f"{api_name}.{method_name} not found or not callable")
        return method(*args, **kwargs)

    def call_data(self, qualified: str, *args, **kwargs) -> Any:
        """
        Same as call(), but returns `result.data` when available.
        """
        if "." not in qualified:
            raise ValueError("Use 'ApiName.method' or 'alias.method', e.g., 'systems.get_system'")
        api_name, method_name = qualified.split(".", 1)
        api = self.get_data_api(api_name)
        method = getattr(api, method_name, None)
        if not callable(method):
            raise AttributeError(f"{api_name}.{method_name} not found or not callable")
        return method(*args, **kwargs)

    def close(self) -> None:
        self._apis.clear()
        self._data_apis.clear()

    def __enter__(self) -> "OpenAPIService":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
