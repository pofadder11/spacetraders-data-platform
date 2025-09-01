# openapi_client.SystemsApi

All URIs are relative to *https://api.spacetraders.io/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_construction**](SystemsApi.md#get_construction) | **GET** /systems/{systemSymbol}/waypoints/{waypointSymbol}/construction | Get Construction Site
[**get_jump_gate**](SystemsApi.md#get_jump_gate) | **GET** /systems/{systemSymbol}/waypoints/{waypointSymbol}/jump-gate | Get Jump Gate
[**get_market**](SystemsApi.md#get_market) | **GET** /systems/{systemSymbol}/waypoints/{waypointSymbol}/market | Get Market
[**get_shipyard**](SystemsApi.md#get_shipyard) | **GET** /systems/{systemSymbol}/waypoints/{waypointSymbol}/shipyard | Get Shipyard
[**get_system**](SystemsApi.md#get_system) | **GET** /systems/{systemSymbol} | Get System
[**get_system_waypoints**](SystemsApi.md#get_system_waypoints) | **GET** /systems/{systemSymbol}/waypoints | List Waypoints in System
[**get_systems**](SystemsApi.md#get_systems) | **GET** /systems | List Systems
[**get_waypoint**](SystemsApi.md#get_waypoint) | **GET** /systems/{systemSymbol}/waypoints/{waypointSymbol} | Get Waypoint
[**supply_construction**](SystemsApi.md#supply_construction) | **POST** /systems/{systemSymbol}/waypoints/{waypointSymbol}/construction/supply | Supply Construction Site


# **get_construction**
> GetConstruction200Response get_construction(system_symbol, waypoint_symbol)

Get Construction Site

Get construction details for a waypoint. Requires a waypoint with a property of `isUnderConstruction` to be true.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_construction200_response import GetConstruction200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.spacetraders.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.spacetraders.io/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): AgentToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SystemsApi(api_client)
    system_symbol = 'system_symbol_example' # str | The system symbol
    waypoint_symbol = 'waypoint_symbol_example' # str | The waypoint symbol

    try:
        # Get Construction Site
        api_response = api_instance.get_construction(system_symbol, waypoint_symbol)
        print("The response of SystemsApi->get_construction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemsApi->get_construction: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **system_symbol** | **str**| The system symbol | 
 **waypoint_symbol** | **str**| The waypoint symbol | 

### Return type

[**GetConstruction200Response**](GetConstruction200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully fetched construction site. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_jump_gate**
> GetJumpGate200Response get_jump_gate(system_symbol, waypoint_symbol)

Get Jump Gate

Get jump gate details for a waypoint. Requires a waypoint of type `JUMP_GATE` to use.

Waypoints connected to this jump gate can be found by querying the waypoints in the system.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_jump_gate200_response import GetJumpGate200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.spacetraders.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.spacetraders.io/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): AgentToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SystemsApi(api_client)
    system_symbol = 'system_symbol_example' # str | The system symbol
    waypoint_symbol = 'waypoint_symbol_example' # str | The waypoint symbol

    try:
        # Get Jump Gate
        api_response = api_instance.get_jump_gate(system_symbol, waypoint_symbol)
        print("The response of SystemsApi->get_jump_gate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemsApi->get_jump_gate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **system_symbol** | **str**| The system symbol | 
 **waypoint_symbol** | **str**| The waypoint symbol | 

### Return type

[**GetJumpGate200Response**](GetJumpGate200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Jump gate details retrieved successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_market**
> GetMarket200Response get_market(system_symbol, waypoint_symbol)

Get Market

Retrieve imports, exports and exchange data from a marketplace. Requires a waypoint that has the `Marketplace` trait to use.

Send a ship to the waypoint to access trade good prices and recent transactions. Refer to the [Market Overview page](https://docs.spacetraders.io/game-concepts/markets) to gain better a understanding of the market in the game.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_market200_response import GetMarket200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.spacetraders.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.spacetraders.io/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): AgentToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SystemsApi(api_client)
    system_symbol = 'system_symbol_example' # str | The system symbol
    waypoint_symbol = 'waypoint_symbol_example' # str | The waypoint symbol

    try:
        # Get Market
        api_response = api_instance.get_market(system_symbol, waypoint_symbol)
        print("The response of SystemsApi->get_market:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemsApi->get_market: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **system_symbol** | **str**| The system symbol | 
 **waypoint_symbol** | **str**| The waypoint symbol | 

### Return type

[**GetMarket200Response**](GetMarket200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully fetched the market. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_shipyard**
> GetShipyard200Response get_shipyard(system_symbol, waypoint_symbol)

Get Shipyard

Get the shipyard for a waypoint. Requires a waypoint that has the `Shipyard` trait to use. Send a ship to the waypoint to access data on ships that are currently available for purchase and recent transactions.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_shipyard200_response import GetShipyard200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.spacetraders.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.spacetraders.io/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): AgentToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SystemsApi(api_client)
    system_symbol = 'system_symbol_example' # str | The system symbol
    waypoint_symbol = 'waypoint_symbol_example' # str | The waypoint symbol

    try:
        # Get Shipyard
        api_response = api_instance.get_shipyard(system_symbol, waypoint_symbol)
        print("The response of SystemsApi->get_shipyard:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemsApi->get_shipyard: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **system_symbol** | **str**| The system symbol | 
 **waypoint_symbol** | **str**| The waypoint symbol | 

### Return type

[**GetShipyard200Response**](GetShipyard200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully fetched the shipyard. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_system**
> GetSystem200Response get_system(system_symbol)

Get System

Get the details of a system. Requires the system to have been visited or charted.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_system200_response import GetSystem200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.spacetraders.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.spacetraders.io/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): AgentToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SystemsApi(api_client)
    system_symbol = 'system_symbol_example' # str | 

    try:
        # Get System
        api_response = api_instance.get_system(system_symbol)
        print("The response of SystemsApi->get_system:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemsApi->get_system: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **system_symbol** | **str**|  | 

### Return type

[**GetSystem200Response**](GetSystem200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully fetched the system. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_system_waypoints**
> GetSystemWaypoints200Response get_system_waypoints(system_symbol, page=page, limit=limit, type=type, traits=traits)

List Waypoints in System

Return a paginated list of all of the waypoints for a given system.

If a waypoint is uncharted, it will return the `Uncharted` trait instead of its actual traits.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_system_waypoints200_response import GetSystemWaypoints200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.spacetraders.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.spacetraders.io/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): AgentToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SystemsApi(api_client)
    system_symbol = 'system_symbol_example' # str | 
    page = 1 # int | What entry offset to request (optional) (default to 1)
    limit = 10 # int | How many entries to return per page (optional) (default to 10)
    type = openapi_client.WaypointType() # WaypointType | Filter waypoints by type. (optional)
    traits = openapi_client.GetSystemWaypointsTraitsParameter() # GetSystemWaypointsTraitsParameter | Filter waypoints by one or more traits. (optional)

    try:
        # List Waypoints in System
        api_response = api_instance.get_system_waypoints(system_symbol, page=page, limit=limit, type=type, traits=traits)
        print("The response of SystemsApi->get_system_waypoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemsApi->get_system_waypoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **system_symbol** | **str**|  | 
 **page** | **int**| What entry offset to request | [optional] [default to 1]
 **limit** | **int**| How many entries to return per page | [optional] [default to 10]
 **type** | [**WaypointType**](.md)| Filter waypoints by type. | [optional] 
 **traits** | [**GetSystemWaypointsTraitsParameter**](.md)| Filter waypoints by one or more traits. | [optional] 

### Return type

[**GetSystemWaypoints200Response**](GetSystemWaypoints200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully listed waypoints. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_systems**
> GetSystems200Response get_systems(page=page, limit=limit)

List Systems

Return a paginated list of all systems.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_systems200_response import GetSystems200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.spacetraders.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.spacetraders.io/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): AgentToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SystemsApi(api_client)
    page = 1 # int | What entry offset to request (optional) (default to 1)
    limit = 10 # int | How many entries to return per page (optional) (default to 10)

    try:
        # List Systems
        api_response = api_instance.get_systems(page=page, limit=limit)
        print("The response of SystemsApi->get_systems:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemsApi->get_systems: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| What entry offset to request | [optional] [default to 1]
 **limit** | **int**| How many entries to return per page | [optional] [default to 10]

### Return type

[**GetSystems200Response**](GetSystems200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully listed systems. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_waypoint**
> GetWaypoint200Response get_waypoint(system_symbol, waypoint_symbol)

Get Waypoint

View the details of a waypoint.

If the waypoint is uncharted, it will return the 'Uncharted' trait instead of its actual traits.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_waypoint200_response import GetWaypoint200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.spacetraders.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.spacetraders.io/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): AgentToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SystemsApi(api_client)
    system_symbol = 'system_symbol_example' # str | The system symbol
    waypoint_symbol = 'waypoint_symbol_example' # str | The waypoint symbol

    try:
        # Get Waypoint
        api_response = api_instance.get_waypoint(system_symbol, waypoint_symbol)
        print("The response of SystemsApi->get_waypoint:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemsApi->get_waypoint: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **system_symbol** | **str**| The system symbol | 
 **waypoint_symbol** | **str**| The waypoint symbol | 

### Return type

[**GetWaypoint200Response**](GetWaypoint200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully fetched waypoint details. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **supply_construction**
> SupplyConstruction201Response supply_construction(system_symbol, waypoint_symbol, supply_construction_request)

Supply Construction Site

Supply a construction site with the specified good. Requires a waypoint with a property of `isUnderConstruction` to be true.

The good must be in your ship's cargo. The good will be removed from your ship's cargo and added to the construction site's materials.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.supply_construction201_response import SupplyConstruction201Response
from openapi_client.models.supply_construction_request import SupplyConstructionRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.spacetraders.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.spacetraders.io/v2"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): AgentToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SystemsApi(api_client)
    system_symbol = 'system_symbol_example' # str | The system symbol
    waypoint_symbol = 'waypoint_symbol_example' # str | The waypoint symbol
    supply_construction_request = openapi_client.SupplyConstructionRequest() # SupplyConstructionRequest | 

    try:
        # Supply Construction Site
        api_response = api_instance.supply_construction(system_symbol, waypoint_symbol, supply_construction_request)
        print("The response of SystemsApi->supply_construction:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemsApi->supply_construction: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **system_symbol** | **str**| The system symbol | 
 **waypoint_symbol** | **str**| The waypoint symbol | 
 **supply_construction_request** | [**SupplyConstructionRequest**](SupplyConstructionRequest.md)|  | 

### Return type

[**SupplyConstruction201Response**](SupplyConstruction201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully supplied construction site. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

