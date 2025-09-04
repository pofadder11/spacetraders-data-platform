# flake8: noqa

if __import__("typing").TYPE_CHECKING:
    # import apis into api package
    from openapi_client.api.accounts_api import AccountsApi
    from openapi_client.api.agents_api import AgentsApi
    from openapi_client.api.contracts_api import ContractsApi
    from openapi_client.api.data_api import DataApi
    from openapi_client.api.factions_api import FactionsApi
    from openapi_client.api.fleet_api import FleetApi
    from openapi_client.api.global_api import GlobalApi
    from openapi_client.api.systems_api import SystemsApi

else:
    from lazy_imports import LazyModule, as_package, load

    load(
        LazyModule(
            *as_package(__file__),
            """# import apis into api package
from openapi_client.api.accounts_api import AccountsApi
from openapi_client.api.agents_api import AgentsApi
from openapi_client.api.contracts_api import ContractsApi
from openapi_client.api.data_api import DataApi
from openapi_client.api.factions_api import FactionsApi
from openapi_client.api.fleet_api import FleetApi
from openapi_client.api.global_api import GlobalApi
from openapi_client.api.systems_api import SystemsApi

""",
            name=__name__,
            doc=__doc__,
        )
    )
