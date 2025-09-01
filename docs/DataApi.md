# openapi_client.DataApi

All URIs are relative to *https://api.spacetraders.io/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_supply_chain**](DataApi.md#get_supply_chain) | **GET** /market/supply-chain | Describes trade relationships
[**websocket_departure_events**](DataApi.md#websocket_departure_events) | **GET** /my/socket.io | Subscribe to events


# **get_supply_chain**
> GetSupplyChain200Response get_supply_chain()

Describes trade relationships

Describes which import and exports map to each other.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_supply_chain200_response import GetSupplyChain200Response
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
    api_instance = openapi_client.DataApi(api_client)

    try:
        # Describes trade relationships
        api_response = api_instance.get_supply_chain()
        print("The response of DataApi->get_supply_chain:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_supply_chain: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetSupplyChain200Response**](GetSupplyChain200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the supply chain information |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **websocket_departure_events**
> websocket_departure_events()

Subscribe to events

Subscribe to departure events for a system.

          ## WebSocket Events

          The following events are available:

          - `systems.{systemSymbol}.departure`: A ship has departed from the system.

          ## Subscribe using a message with the following format:

          ```json
          {
            "action": "subscribe",
            "systemSymbol": "{systemSymbol}"
          }
          ```

          ## Unsubscribe using a message with the following format:

          ```json
          {
            "action": "unsubscribe",
            "systemSymbol": "{systemSymbol}"
          }
          ```

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
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
    api_instance = openapi_client.DataApi(api_client)

    try:
        # Subscribe to events
        api_instance.websocket_departure_events()
    except Exception as e:
        print("Exception when calling DataApi->websocket_departure_events: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Default Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

