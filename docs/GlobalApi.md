# openapi_client.GlobalApi

All URIs are relative to *https://api.spacetraders.io/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_error_codes**](GlobalApi.md#get_error_codes) | **GET** /error-codes | Error code list
[**get_status**](GlobalApi.md#get_status) | **GET** / | Server status


# **get_error_codes**
> GetErrorCodes200Response get_error_codes()

Error code list

Return a list of all possible error codes thrown by the game server.

### Example

* Bearer (JWT) Authentication (AccountToken):
* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_error_codes200_response import GetErrorCodes200Response
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

# Configure Bearer authorization (JWT): AccountToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Configure Bearer authorization (JWT): AgentToken
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.GlobalApi(api_client)

    try:
        # Error code list
        api_response = api_instance.get_error_codes()
        print("The response of GlobalApi->get_error_codes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GlobalApi->get_error_codes: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetErrorCodes200Response**](GetErrorCodes200Response.md)

### Authorization

[AccountToken](../README.md#AccountToken), [AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Fetched error codes successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_status**
> GetStatus200Response get_status()

Server status

Return the status of the game server.
This also includes a few global elements, such as announcements, server reset dates and leaderboards.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_status200_response import GetStatus200Response
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
    api_instance = openapi_client.GlobalApi(api_client)

    try:
        # Server status
        api_response = api_instance.get_status()
        print("The response of GlobalApi->get_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GlobalApi->get_status: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetStatus200Response**](GetStatus200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Fetched status successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

