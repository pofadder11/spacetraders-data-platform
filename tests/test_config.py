import os
import pytest
import config


def test_api_token_loaded():
    token = os.getenv("SPACETRADERS_TOKEN")
    assert config.API_TOKEN == token
    assert config.API_TOKEN is not None
