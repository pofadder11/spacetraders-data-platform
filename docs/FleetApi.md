# openapi_client.FleetApi

All URIs are relative to *https://api.spacetraders.io/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_chart**](FleetApi.md#create_chart) | **POST** /my/ships/{shipSymbol}/chart | Create Chart
[**create_ship_ship_scan**](FleetApi.md#create_ship_ship_scan) | **POST** /my/ships/{shipSymbol}/scan/ships | Scan Ships
[**create_ship_system_scan**](FleetApi.md#create_ship_system_scan) | **POST** /my/ships/{shipSymbol}/scan/systems | Scan Systems
[**create_ship_waypoint_scan**](FleetApi.md#create_ship_waypoint_scan) | **POST** /my/ships/{shipSymbol}/scan/waypoints | Scan Waypoints
[**create_survey**](FleetApi.md#create_survey) | **POST** /my/ships/{shipSymbol}/survey | Create Survey
[**dock_ship**](FleetApi.md#dock_ship) | **POST** /my/ships/{shipSymbol}/dock | Dock Ship
[**extract_resources**](FleetApi.md#extract_resources) | **POST** /my/ships/{shipSymbol}/extract | Extract Resources
[**extract_resources_with_survey**](FleetApi.md#extract_resources_with_survey) | **POST** /my/ships/{shipSymbol}/extract/survey | Extract Resources with Survey
[**get_mounts**](FleetApi.md#get_mounts) | **GET** /my/ships/{shipSymbol}/mounts | Get Mounts
[**get_my_ship**](FleetApi.md#get_my_ship) | **GET** /my/ships/{shipSymbol} | Get Ship
[**get_my_ship_cargo**](FleetApi.md#get_my_ship_cargo) | **GET** /my/ships/{shipSymbol}/cargo | Get Ship Cargo
[**get_my_ships**](FleetApi.md#get_my_ships) | **GET** /my/ships | List Ships
[**get_repair_ship**](FleetApi.md#get_repair_ship) | **GET** /my/ships/{shipSymbol}/repair | Get Repair Ship
[**get_scrap_ship**](FleetApi.md#get_scrap_ship) | **GET** /my/ships/{shipSymbol}/scrap | Get Scrap Ship
[**get_ship_cooldown**](FleetApi.md#get_ship_cooldown) | **GET** /my/ships/{shipSymbol}/cooldown | Get Ship Cooldown
[**get_ship_modules**](FleetApi.md#get_ship_modules) | **GET** /my/ships/{shipSymbol}/modules | Get Ship Modules
[**get_ship_nav**](FleetApi.md#get_ship_nav) | **GET** /my/ships/{shipSymbol}/nav | Get Ship Nav
[**install_mount**](FleetApi.md#install_mount) | **POST** /my/ships/{shipSymbol}/mounts/install | Install Mount
[**install_ship_module**](FleetApi.md#install_ship_module) | **POST** /my/ships/{shipSymbol}/modules/install | Install Ship Module
[**jettison**](FleetApi.md#jettison) | **POST** /my/ships/{shipSymbol}/jettison | Jettison Cargo
[**jump_ship**](FleetApi.md#jump_ship) | **POST** /my/ships/{shipSymbol}/jump | Jump Ship
[**navigate_ship**](FleetApi.md#navigate_ship) | **POST** /my/ships/{shipSymbol}/navigate | Navigate Ship
[**negotiate_contract**](FleetApi.md#negotiate_contract) | **POST** /my/ships/{shipSymbol}/negotiate/contract | Negotiate Contract
[**orbit_ship**](FleetApi.md#orbit_ship) | **POST** /my/ships/{shipSymbol}/orbit | Orbit Ship
[**patch_ship_nav**](FleetApi.md#patch_ship_nav) | **PATCH** /my/ships/{shipSymbol}/nav | Patch Ship Nav
[**purchase_cargo**](FleetApi.md#purchase_cargo) | **POST** /my/ships/{shipSymbol}/purchase | Purchase Cargo
[**purchase_ship**](FleetApi.md#purchase_ship) | **POST** /my/ships | Purchase Ship
[**refuel_ship**](FleetApi.md#refuel_ship) | **POST** /my/ships/{shipSymbol}/refuel | Refuel Ship
[**remove_mount**](FleetApi.md#remove_mount) | **POST** /my/ships/{shipSymbol}/mounts/remove | Remove Mount
[**remove_ship_module**](FleetApi.md#remove_ship_module) | **POST** /my/ships/{shipSymbol}/modules/remove | Remove Ship Module
[**repair_ship**](FleetApi.md#repair_ship) | **POST** /my/ships/{shipSymbol}/repair | Repair Ship
[**scrap_ship**](FleetApi.md#scrap_ship) | **POST** /my/ships/{shipSymbol}/scrap | Scrap Ship
[**sell_cargo**](FleetApi.md#sell_cargo) | **POST** /my/ships/{shipSymbol}/sell | Sell Cargo
[**ship_refine**](FleetApi.md#ship_refine) | **POST** /my/ships/{shipSymbol}/refine | Ship Refine
[**siphon_resources**](FleetApi.md#siphon_resources) | **POST** /my/ships/{shipSymbol}/siphon | Siphon Resources
[**transfer_cargo**](FleetApi.md#transfer_cargo) | **POST** /my/ships/{shipSymbol}/transfer | Transfer Cargo
[**warp_ship**](FleetApi.md#warp_ship) | **POST** /my/ships/{shipSymbol}/warp | Warp Ship


# **create_chart**
> CreateChart201Response create_chart(ship_symbol)

Create Chart

Command a ship to chart the waypoint at its current location.

Most waypoints in the universe are uncharted by default. These waypoints have their traits hidden until they have been charted by a ship.

Charting a waypoint will record your agent as the one who created the chart, and all other agents would also be able to see the waypoint's traits. Charting a waypoint gives you a one time reward of credits based on the rarity of the waypoint's traits.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.create_chart201_response import CreateChart201Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Create Chart
        api_response = api_instance.create_chart(ship_symbol)
        print("The response of FleetApi->create_chart:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->create_chart: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**CreateChart201Response**](CreateChart201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully charted waypoint. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_ship_ship_scan**
> CreateShipShipScan201Response create_ship_ship_scan(ship_symbol)

Scan Ships

Scan for nearby ships, retrieving information for all ships in range.

Requires a ship to have the `Sensor Array` mount installed to use.

The ship will enter a cooldown after using this function, during which it cannot execute certain actions.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.create_ship_ship_scan201_response import CreateShipShipScan201Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Scan Ships
        api_response = api_instance.create_ship_ship_scan(ship_symbol)
        print("The response of FleetApi->create_ship_ship_scan:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->create_ship_ship_scan: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**CreateShipShipScan201Response**](CreateShipShipScan201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully scanned for nearby ships. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_ship_system_scan**
> CreateShipSystemScan201Response create_ship_system_scan(ship_symbol)

Scan Systems

Scan for nearby systems, retrieving information on the systems' distance from the ship and their waypoints. Requires a ship to have the `Sensor Array` mount installed to use.

The ship will enter a cooldown after using this function, during which it cannot execute certain actions.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.create_ship_system_scan201_response import CreateShipSystemScan201Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Scan Systems
        api_response = api_instance.create_ship_system_scan(ship_symbol)
        print("The response of FleetApi->create_ship_system_scan:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->create_ship_system_scan: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**CreateShipSystemScan201Response**](CreateShipSystemScan201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully scanned for nearby systems. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_ship_waypoint_scan**
> CreateShipWaypointScan201Response create_ship_waypoint_scan(ship_symbol)

Scan Waypoints

Scan for nearby waypoints, retrieving detailed information on each waypoint in range. Scanning uncharted waypoints will allow you to ignore their uncharted state and will list the waypoints' traits.

Requires a ship to have the `Sensor Array` mount installed to use.

The ship will enter a cooldown after using this function, during which it cannot execute certain actions.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.create_ship_waypoint_scan201_response import CreateShipWaypointScan201Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Scan Waypoints
        api_response = api_instance.create_ship_waypoint_scan(ship_symbol)
        print("The response of FleetApi->create_ship_waypoint_scan:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->create_ship_waypoint_scan: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**CreateShipWaypointScan201Response**](CreateShipWaypointScan201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully scanned for nearby waypoints. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_survey**
> CreateSurvey201Response create_survey(ship_symbol)

Create Survey

Create surveys on a waypoint that can be extracted such as asteroid fields. A survey focuses on specific types of deposits from the extracted location. When ships extract using this survey, they are guaranteed to procure a high amount of one of the goods in the survey.

In order to use a survey, send the entire survey details in the body of the extract request.

Each survey may have multiple deposits, and if a symbol shows up more than once, that indicates a higher chance of extracting that resource.

Your ship will enter a cooldown after surveying in which it is unable to perform certain actions. Surveys will eventually expire after a period of time or will be exhausted after being extracted several times based on the survey's size. Multiple ships can use the same survey for extraction.

A ship must have the `Surveyor` mount installed in order to use this function.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.create_survey201_response import CreateSurvey201Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Create Survey
        api_response = api_instance.create_survey(ship_symbol)
        print("The response of FleetApi->create_survey:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->create_survey: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**CreateSurvey201Response**](CreateSurvey201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Surveys has been created. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dock_ship**
> DockShip200Response dock_ship(ship_symbol)

Dock Ship

Attempt to dock your ship at its current location. Docking will only succeed if your ship is capable of docking at the time of the request.

Docked ships can access elements in their current location, such as the market or a shipyard, but cannot do actions that require the ship to be above surface such as navigating or extracting.

The endpoint is idempotent - successive calls will succeed even if the ship is already docked.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.dock_ship200_response import DockShip200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Dock Ship
        api_response = api_instance.dock_ship(ship_symbol)
        print("The response of FleetApi->dock_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->dock_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**DockShip200Response**](DockShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ship has successfully docked at its current location. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **extract_resources**
> ExtractResources201Response extract_resources(ship_symbol)

Extract Resources

Extract resources from a waypoint that can be extracted, such as asteroid fields, into your ship. Send an optional survey as the payload to target specific yields.

The ship must be in orbit to be able to extract and must have mining equipments installed that can extract goods, such as the `Gas Siphon` mount for gas-based goods or `Mining Laser` mount for ore-based goods.

The survey property is now deprecated. See the `extract/survey` endpoint for more details.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.extract_resources201_response import ExtractResources201Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Extract Resources
        api_response = api_instance.extract_resources(ship_symbol)
        print("The response of FleetApi->extract_resources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->extract_resources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**ExtractResources201Response**](ExtractResources201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully extracted resources. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **extract_resources_with_survey**
> ExtractResources201Response extract_resources_with_survey(ship_symbol, survey=survey)

Extract Resources with Survey

Use a survey when extracting resources from a waypoint. This endpoint requires a survey as the payload, which allows your ship to extract specific yields.

Send the full survey object as the payload which will be validated according to the signature. If the signature is invalid, or any properties of the survey are changed, the request will fail.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.extract_resources201_response import ExtractResources201Response
from openapi_client.models.survey import Survey
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    survey = openapi_client.Survey() # Survey |  (optional)

    try:
        # Extract Resources with Survey
        api_response = api_instance.extract_resources_with_survey(ship_symbol, survey=survey)
        print("The response of FleetApi->extract_resources_with_survey:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->extract_resources_with_survey: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **survey** | [**Survey**](Survey.md)|  | [optional] 

### Return type

[**ExtractResources201Response**](ExtractResources201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully extracted resources. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_mounts**
> GetMounts200Response get_mounts(ship_symbol)

Get Mounts

Get the mounts installed on a ship.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_mounts200_response import GetMounts200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Get Mounts
        api_response = api_instance.get_mounts(ship_symbol)
        print("The response of FleetApi->get_mounts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->get_mounts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**GetMounts200Response**](GetMounts200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved ship mounts. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_my_ship**
> GetMyShip200Response get_my_ship(ship_symbol)

Get Ship

Retrieve the details of a ship under your agent's ownership.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_my_ship200_response import GetMyShip200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Get Ship
        api_response = api_instance.get_my_ship(ship_symbol)
        print("The response of FleetApi->get_my_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->get_my_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**GetMyShip200Response**](GetMyShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully fetched ship. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_my_ship_cargo**
> GetMyShipCargo200Response get_my_ship_cargo(ship_symbol)

Get Ship Cargo

Retrieve the cargo of a ship under your agent's ownership.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_my_ship_cargo200_response import GetMyShipCargo200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Get Ship Cargo
        api_response = api_instance.get_my_ship_cargo(ship_symbol)
        print("The response of FleetApi->get_my_ship_cargo:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->get_my_ship_cargo: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**GetMyShipCargo200Response**](GetMyShipCargo200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully fetched ship&#39;s cargo. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_my_ships**
> GetMyShips200Response get_my_ships(page=page, limit=limit)

List Ships

Return a paginated list of all of ships under your agent's ownership.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_my_ships200_response import GetMyShips200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    page = 1 # int | What entry offset to request (optional) (default to 1)
    limit = 10 # int | How many entries to return per page (optional) (default to 10)

    try:
        # List Ships
        api_response = api_instance.get_my_ships(page=page, limit=limit)
        print("The response of FleetApi->get_my_ships:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->get_my_ships: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| What entry offset to request | [optional] [default to 1]
 **limit** | **int**| How many entries to return per page | [optional] [default to 10]

### Return type

[**GetMyShips200Response**](GetMyShips200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully listed ships. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_repair_ship**
> GetRepairShip200Response get_repair_ship(ship_symbol)

Get Repair Ship

Get the cost of repairing a ship. Requires the ship to be docked at a waypoint that has the `Shipyard` trait.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_repair_ship200_response import GetRepairShip200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Get Repair Ship
        api_response = api_instance.get_repair_ship(ship_symbol)
        print("The response of FleetApi->get_repair_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->get_repair_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**GetRepairShip200Response**](GetRepairShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the cost of repairing a ship. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scrap_ship**
> GetScrapShip200Response get_scrap_ship(ship_symbol)

Get Scrap Ship

Get the value of scrapping a ship. Requires the ship to be docked at a waypoint that has the `Shipyard` trait.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_scrap_ship200_response import GetScrapShip200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Get Scrap Ship
        api_response = api_instance.get_scrap_ship(ship_symbol)
        print("The response of FleetApi->get_scrap_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->get_scrap_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**GetScrapShip200Response**](GetScrapShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the amount of value that will be returned when scrapping a ship. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ship_cooldown**
> GetShipCooldown200Response get_ship_cooldown(ship_symbol)

Get Ship Cooldown

Retrieve the details of your ship's reactor cooldown. Some actions such as activating your jump drive, scanning, or extracting resources taxes your reactor and results in a cooldown.

Your ship cannot perform additional actions until your cooldown has expired. The duration of your cooldown is relative to the power consumption of the related modules or mounts for the action taken.

Response returns a 204 status code (no-content) when the ship has no cooldown.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_ship_cooldown200_response import GetShipCooldown200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Get Ship Cooldown
        api_response = api_instance.get_ship_cooldown(ship_symbol)
        print("The response of FleetApi->get_ship_cooldown:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->get_ship_cooldown: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**GetShipCooldown200Response**](GetShipCooldown200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully fetched ship&#39;s cooldown. |  -  |
**204** | No cooldown. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ship_modules**
> GetShipModules200Response get_ship_modules(ship_symbol)

Get Ship Modules

Get the modules installed on a ship.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_ship_modules200_response import GetShipModules200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Get Ship Modules
        api_response = api_instance.get_ship_modules(ship_symbol)
        print("The response of FleetApi->get_ship_modules:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->get_ship_modules: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**GetShipModules200Response**](GetShipModules200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved ship modules. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ship_nav**
> GetShipNav200Response get_ship_nav(ship_symbol)

Get Ship Nav

Get the current nav status of a ship.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_ship_nav200_response import GetShipNav200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Get Ship Nav
        api_response = api_instance.get_ship_nav(ship_symbol)
        print("The response of FleetApi->get_ship_nav:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->get_ship_nav: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**GetShipNav200Response**](GetShipNav200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The current nav status of the ship. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **install_mount**
> InstallMount201Response install_mount(ship_symbol, install_mount_request)

Install Mount

Install a mount on a ship.

In order to install a mount, the ship must be docked and located in a waypoint that has a `Shipyard` trait. The ship also must have the mount to install in its cargo hold.

An installation fee will be deduced by the Shipyard for installing the mount on the ship.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.install_mount201_response import InstallMount201Response
from openapi_client.models.install_mount_request import InstallMountRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    install_mount_request = openapi_client.InstallMountRequest() # InstallMountRequest | 

    try:
        # Install Mount
        api_response = api_instance.install_mount(ship_symbol, install_mount_request)
        print("The response of FleetApi->install_mount:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->install_mount: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **install_mount_request** | [**InstallMountRequest**](InstallMountRequest.md)|  | 

### Return type

[**InstallMount201Response**](InstallMount201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully installed the mount. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **install_ship_module**
> InstallShipModule201Response install_ship_module(ship_symbol, install_ship_module_request)

Install Ship Module

Install a module on a ship. The module must be in your cargo.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.install_ship_module201_response import InstallShipModule201Response
from openapi_client.models.install_ship_module_request import InstallShipModuleRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    install_ship_module_request = openapi_client.InstallShipModuleRequest() # InstallShipModuleRequest | 

    try:
        # Install Ship Module
        api_response = api_instance.install_ship_module(ship_symbol, install_ship_module_request)
        print("The response of FleetApi->install_ship_module:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->install_ship_module: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **install_ship_module_request** | [**InstallShipModuleRequest**](InstallShipModuleRequest.md)|  | 

### Return type

[**InstallShipModule201Response**](InstallShipModule201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully installed the module on the ship. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jettison**
> Jettison200Response jettison(ship_symbol, jettison_request)

Jettison Cargo

Jettison cargo from your ship's cargo hold.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.jettison200_response import Jettison200Response
from openapi_client.models.jettison_request import JettisonRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    jettison_request = openapi_client.JettisonRequest() # JettisonRequest | 

    try:
        # Jettison Cargo
        api_response = api_instance.jettison(ship_symbol, jettison_request)
        print("The response of FleetApi->jettison:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->jettison: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **jettison_request** | [**JettisonRequest**](JettisonRequest.md)|  | 

### Return type

[**Jettison200Response**](Jettison200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Jettison successful. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **jump_ship**
> JumpShip200Response jump_ship(ship_symbol, jump_ship_request)

Jump Ship

Jump your ship instantly to a target connected waypoint. The ship must be in orbit to execute a jump.

A unit of antimatter is purchased and consumed from the market when jumping. The price of antimatter is determined by the market and is subject to change. A ship can only jump to connected waypoints

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.jump_ship200_response import JumpShip200Response
from openapi_client.models.jump_ship_request import JumpShipRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    jump_ship_request = openapi_client.JumpShipRequest() # JumpShipRequest | 

    try:
        # Jump Ship
        api_response = api_instance.jump_ship(ship_symbol, jump_ship_request)
        print("The response of FleetApi->jump_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->jump_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **jump_ship_request** | [**JumpShipRequest**](JumpShipRequest.md)|  | 

### Return type

[**JumpShip200Response**](JumpShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Jump successful. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **navigate_ship**
> NavigateShip200Response navigate_ship(ship_symbol, navigate_ship_request)

Navigate Ship

Navigate to a target destination. The ship must be in orbit to use this function. The destination waypoint must be within the same system as the ship's current location. Navigating will consume the necessary fuel from the ship's manifest based on the distance to the target waypoint.

The returned response will detail the route information including the expected time of arrival. Most ship actions are unavailable until the ship has arrived at it's destination.

To travel between systems, see the ship's Warp or Jump actions.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.navigate_ship200_response import NavigateShip200Response
from openapi_client.models.navigate_ship_request import NavigateShipRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    navigate_ship_request = openapi_client.NavigateShipRequest() # NavigateShipRequest | 

    try:
        # Navigate Ship
        api_response = api_instance.navigate_ship(ship_symbol, navigate_ship_request)
        print("The response of FleetApi->navigate_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->navigate_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **navigate_ship_request** | [**NavigateShipRequest**](NavigateShipRequest.md)|  | 

### Return type

[**NavigateShip200Response**](NavigateShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The successful transit information including the route details and changes to ship fuel. The route includes the expected time of arrival. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **negotiate_contract**
> NegotiateContract201Response negotiate_contract(ship_symbol)

Negotiate Contract

Negotiate a new contract with the HQ.

In order to negotiate a new contract, an agent must not have ongoing or offered contracts over the allowed maximum amount. Currently the maximum contracts an agent can have at a time is 1.

Once a contract is negotiated, it is added to the list of contracts offered to the agent, which the agent can then accept. 

The ship must be present at any waypoint with a faction present to negotiate a contract with that faction.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.negotiate_contract201_response import NegotiateContract201Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Negotiate Contract
        api_response = api_instance.negotiate_contract(ship_symbol)
        print("The response of FleetApi->negotiate_contract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->negotiate_contract: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**NegotiateContract201Response**](NegotiateContract201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully negotiated a new contract. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **orbit_ship**
> OrbitShip200Response orbit_ship(ship_symbol)

Orbit Ship

Attempt to move your ship into orbit at its current location. The request will only succeed if your ship is capable of moving into orbit at the time of the request.

Orbiting ships are able to do actions that require the ship to be above surface such as navigating or extracting, but cannot access elements in their current waypoint, such as the market or a shipyard.

The endpoint is idempotent - successive calls will succeed even if the ship is already in orbit.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.orbit_ship200_response import OrbitShip200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | 

    try:
        # Orbit Ship
        api_response = api_instance.orbit_ship(ship_symbol)
        print("The response of FleetApi->orbit_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->orbit_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**|  | 

### Return type

[**OrbitShip200Response**](OrbitShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ship has successfully moved into orbit at its current location. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_ship_nav**
> PatchShipNav200Response patch_ship_nav(ship_symbol, patch_ship_nav_request=patch_ship_nav_request)

Patch Ship Nav

Update the nav configuration of a ship.

Currently only supports configuring the Flight Mode of the ship, which affects its speed and fuel consumption.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.patch_ship_nav200_response import PatchShipNav200Response
from openapi_client.models.patch_ship_nav_request import PatchShipNavRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    patch_ship_nav_request = openapi_client.PatchShipNavRequest() # PatchShipNavRequest |  (optional)

    try:
        # Patch Ship Nav
        api_response = api_instance.patch_ship_nav(ship_symbol, patch_ship_nav_request=patch_ship_nav_request)
        print("The response of FleetApi->patch_ship_nav:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->patch_ship_nav: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **patch_ship_nav_request** | [**PatchShipNavRequest**](PatchShipNavRequest.md)|  | [optional] 

### Return type

[**PatchShipNav200Response**](PatchShipNav200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response for updating the nav configuration of a ship. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **purchase_cargo**
> PurchaseCargo201Response purchase_cargo(ship_symbol, purchase_cargo_request)

Purchase Cargo

Purchase cargo from a market.

The ship must be docked in a waypoint that has `Marketplace` trait, and the market must be selling a good to be able to purchase it.

The maximum amount of units of a good that can be purchased in each transaction are denoted by the `tradeVolume` value of the good, which can be viewed by using the Get Market action.

Purchased goods are added to the ship's cargo hold.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.purchase_cargo201_response import PurchaseCargo201Response
from openapi_client.models.purchase_cargo_request import PurchaseCargoRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    purchase_cargo_request = openapi_client.PurchaseCargoRequest() # PurchaseCargoRequest | 

    try:
        # Purchase Cargo
        api_response = api_instance.purchase_cargo(ship_symbol, purchase_cargo_request)
        print("The response of FleetApi->purchase_cargo:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->purchase_cargo: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **purchase_cargo_request** | [**PurchaseCargoRequest**](PurchaseCargoRequest.md)|  | 

### Return type

[**PurchaseCargo201Response**](PurchaseCargo201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Purchased goods successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **purchase_ship**
> PurchaseShip201Response purchase_ship(purchase_ship_request)

Purchase Ship

Purchase a ship from a Shipyard. In order to use this function, a ship under your agent's ownership must be in a waypoint that has the `Shipyard` trait, and the Shipyard must sell the type of the desired ship.

Shipyards typically offer ship types, which are predefined templates of ships that have dedicated roles. A template comes with a preset of an engine, a reactor, and a frame. It may also include a few modules and mounts.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.purchase_ship201_response import PurchaseShip201Response
from openapi_client.models.purchase_ship_request import PurchaseShipRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    purchase_ship_request = openapi_client.PurchaseShipRequest() # PurchaseShipRequest | 

    try:
        # Purchase Ship
        api_response = api_instance.purchase_ship(purchase_ship_request)
        print("The response of FleetApi->purchase_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->purchase_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **purchase_ship_request** | [**PurchaseShipRequest**](PurchaseShipRequest.md)|  | 

### Return type

[**PurchaseShip201Response**](PurchaseShip201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Purchased ship successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **refuel_ship**
> RefuelShip200Response refuel_ship(ship_symbol, refuel_ship_request=refuel_ship_request)

Refuel Ship

Refuel your ship by buying fuel from the local market.

Requires the ship to be docked in a waypoint that has the `Marketplace` trait, and the market must be selling fuel in order to refuel.

Each fuel bought from the market replenishes 100 units in your ship's fuel.

Ships will always be refuel to their frame's maximum fuel capacity when using this action.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.refuel_ship200_response import RefuelShip200Response
from openapi_client.models.refuel_ship_request import RefuelShipRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    refuel_ship_request = openapi_client.RefuelShipRequest() # RefuelShipRequest |  (optional)

    try:
        # Refuel Ship
        api_response = api_instance.refuel_ship(ship_symbol, refuel_ship_request=refuel_ship_request)
        print("The response of FleetApi->refuel_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->refuel_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **refuel_ship_request** | [**RefuelShipRequest**](RefuelShipRequest.md)|  | [optional] 

### Return type

[**RefuelShip200Response**](RefuelShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json, text/plain
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Refueled successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_mount**
> RemoveMount201Response remove_mount(ship_symbol, remove_mount_request)

Remove Mount

Remove a mount from a ship.

The ship must be docked in a waypoint that has the `Shipyard` trait, and must have the desired mount that it wish to remove installed.

A removal fee will be deduced from the agent by the Shipyard.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.remove_mount201_response import RemoveMount201Response
from openapi_client.models.remove_mount_request import RemoveMountRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    remove_mount_request = openapi_client.RemoveMountRequest() # RemoveMountRequest | 

    try:
        # Remove Mount
        api_response = api_instance.remove_mount(ship_symbol, remove_mount_request)
        print("The response of FleetApi->remove_mount:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->remove_mount: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **remove_mount_request** | [**RemoveMountRequest**](RemoveMountRequest.md)|  | 

### Return type

[**RemoveMount201Response**](RemoveMount201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully removed the mount. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_ship_module**
> RemoveShipModule201Response remove_ship_module(ship_symbol, remove_ship_module_request)

Remove Ship Module

Remove a module from a ship. The module will be placed in cargo.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.remove_ship_module201_response import RemoveShipModule201Response
from openapi_client.models.remove_ship_module_request import RemoveShipModuleRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    remove_ship_module_request = openapi_client.RemoveShipModuleRequest() # RemoveShipModuleRequest | 

    try:
        # Remove Ship Module
        api_response = api_instance.remove_ship_module(ship_symbol, remove_ship_module_request)
        print("The response of FleetApi->remove_ship_module:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->remove_ship_module: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **remove_ship_module_request** | [**RemoveShipModuleRequest**](RemoveShipModuleRequest.md)|  | 

### Return type

[**RemoveShipModule201Response**](RemoveShipModule201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully removed the module from the ship. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **repair_ship**
> RepairShip200Response repair_ship(ship_symbol)

Repair Ship

Repair a ship, restoring the ship to maximum condition. The ship must be docked at a waypoint that has the `Shipyard` trait in order to use this function. To preview the cost of repairing the ship, use the Get action.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.repair_ship200_response import RepairShip200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Repair Ship
        api_response = api_instance.repair_ship(ship_symbol)
        print("The response of FleetApi->repair_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->repair_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**RepairShip200Response**](RepairShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Ship repaired successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scrap_ship**
> ScrapShip200Response scrap_ship(ship_symbol)

Scrap Ship

Scrap a ship, removing it from the game and receiving a portion of the ship's value back in credits. The ship must be docked in a waypoint that has the `Shipyard` trait to be scrapped.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.scrap_ship200_response import ScrapShip200Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Scrap Ship
        api_response = api_instance.scrap_ship(ship_symbol)
        print("The response of FleetApi->scrap_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->scrap_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**ScrapShip200Response**](ScrapShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Ship scrapped successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sell_cargo**
> SellCargo201Response sell_cargo(ship_symbol, sell_cargo_request)

Sell Cargo

Sell cargo in your ship to a market that trades this cargo. The ship must be docked in a waypoint that has the `Marketplace` trait in order to use this function.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.sell_cargo201_response import SellCargo201Response
from openapi_client.models.sell_cargo_request import SellCargoRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    sell_cargo_request = openapi_client.SellCargoRequest() # SellCargoRequest | 

    try:
        # Sell Cargo
        api_response = api_instance.sell_cargo(ship_symbol, sell_cargo_request)
        print("The response of FleetApi->sell_cargo:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->sell_cargo: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **sell_cargo_request** | [**SellCargoRequest**](SellCargoRequest.md)|  | 

### Return type

[**SellCargo201Response**](SellCargo201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Cargo was successfully sold. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ship_refine**
> ShipRefine201Response ship_refine(ship_symbol, ship_refine_request)

Ship Refine

Attempt to refine the raw materials on your ship. The request will only succeed if your ship is capable of refining at the time of the request. In order to be able to refine, a ship must have goods that can be refined and have installed a `Refinery` module that can refine it.

When refining, 100 basic goods will be converted into 10 processed goods.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.ship_refine201_response import ShipRefine201Response
from openapi_client.models.ship_refine_request import ShipRefineRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    ship_refine_request = openapi_client.ShipRefineRequest() # ShipRefineRequest | 

    try:
        # Ship Refine
        api_response = api_instance.ship_refine(ship_symbol, ship_refine_request)
        print("The response of FleetApi->ship_refine:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->ship_refine: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **ship_refine_request** | [**ShipRefineRequest**](ShipRefineRequest.md)|  | 

### Return type

[**ShipRefine201Response**](ShipRefine201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The ship has successfully refined goods. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **siphon_resources**
> SiphonResources201Response siphon_resources(ship_symbol)

Siphon Resources

Siphon gases or other resources from gas giants.

The ship must be in orbit to be able to siphon and must have siphon mounts and a gas processor installed.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.siphon_resources201_response import SiphonResources201Response
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Siphon Resources
        api_response = api_instance.siphon_resources(ship_symbol)
        print("The response of FleetApi->siphon_resources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->siphon_resources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 

### Return type

[**SiphonResources201Response**](SiphonResources201Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Siphon successful. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **transfer_cargo**
> TransferCargo200Response transfer_cargo(ship_symbol, transfer_cargo_request)

Transfer Cargo

Transfer cargo between ships.

The receiving ship must be in the same waypoint as the transferring ship, and it must able to hold the additional cargo after the transfer is complete. Both ships also must be in the same state, either both are docked or both are orbiting.

The response body's cargo shows the cargo of the transferring ship after the transfer is complete.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.transfer_cargo200_response import TransferCargo200Response
from openapi_client.models.transfer_cargo_request import TransferCargoRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    transfer_cargo_request = openapi_client.TransferCargoRequest() # TransferCargoRequest | 

    try:
        # Transfer Cargo
        api_response = api_instance.transfer_cargo(ship_symbol, transfer_cargo_request)
        print("The response of FleetApi->transfer_cargo:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->transfer_cargo: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **transfer_cargo_request** | [**TransferCargoRequest**](TransferCargoRequest.md)|  | 

### Return type

[**TransferCargo200Response**](TransferCargo200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cargo transferred successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **warp_ship**
> NavigateShip200Response warp_ship(ship_symbol, navigate_ship_request)

Warp Ship

Warp your ship to a target destination in another system. The ship must be in orbit to use this function and must have the `Warp Drive` module installed. Warping will consume the necessary fuel from the ship's manifest.

The returned response will detail the route information including the expected time of arrival. Most ship actions are unavailable until the ship has arrived at its destination.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.navigate_ship200_response import NavigateShip200Response
from openapi_client.models.navigate_ship_request import NavigateShipRequest
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
    api_instance = openapi_client.FleetApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.
    navigate_ship_request = openapi_client.NavigateShipRequest() # NavigateShipRequest | 

    try:
        # Warp Ship
        api_response = api_instance.warp_ship(ship_symbol, navigate_ship_request)
        print("The response of FleetApi->warp_ship:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FleetApi->warp_ship: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ship_symbol** | **str**| The symbol of the ship. | 
 **navigate_ship_request** | [**NavigateShipRequest**](NavigateShipRequest.md)|  | 

### Return type

[**NavigateShip200Response**](NavigateShip200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The successful transit information including the route details and changes to ship fuel. The route includes the expected time of arrival. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

