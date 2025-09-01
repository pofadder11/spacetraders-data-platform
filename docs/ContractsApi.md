# openapi_client.ContractsApi

All URIs are relative to *https://api.spacetraders.io/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**accept_contract**](ContractsApi.md#accept_contract) | **POST** /my/contracts/{contractId}/accept | Accept Contract
[**deliver_contract**](ContractsApi.md#deliver_contract) | **POST** /my/contracts/{contractId}/deliver | Deliver Cargo to Contract
[**fulfill_contract**](ContractsApi.md#fulfill_contract) | **POST** /my/contracts/{contractId}/fulfill | Fulfill Contract
[**get_contract**](ContractsApi.md#get_contract) | **GET** /my/contracts/{contractId} | Get Contract
[**get_contracts**](ContractsApi.md#get_contracts) | **GET** /my/contracts | List Contracts
[**negotiate_contract**](ContractsApi.md#negotiate_contract) | **POST** /my/ships/{shipSymbol}/negotiate/contract | Negotiate Contract


# **accept_contract**
> AcceptContract200Response accept_contract(contract_id)

Accept Contract

Accept a contract by ID. 

You can only accept contracts that were offered to you, were not accepted yet, and whose deadlines has not passed yet.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.accept_contract200_response import AcceptContract200Response
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
    api_instance = openapi_client.ContractsApi(api_client)
    contract_id = 'contract_id_example' # str | The contract ID to accept.

    try:
        # Accept Contract
        api_response = api_instance.accept_contract(contract_id)
        print("The response of ContractsApi->accept_contract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractsApi->accept_contract: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_id** | **str**| The contract ID to accept. | 

### Return type

[**AcceptContract200Response**](AcceptContract200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully accepted contract. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deliver_contract**
> DeliverContract200Response deliver_contract(contract_id, deliver_contract_request)

Deliver Cargo to Contract

Deliver cargo to a contract.

In order to use this API, a ship must be at the delivery location (denoted in the delivery terms as `destinationSymbol` of a contract) and must have a number of units of a good required by this contract in its cargo.

Cargo that was delivered will be removed from the ship's cargo.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.deliver_contract200_response import DeliverContract200Response
from openapi_client.models.deliver_contract_request import DeliverContractRequest
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
    api_instance = openapi_client.ContractsApi(api_client)
    contract_id = 'contract_id_example' # str | The ID of the contract.
    deliver_contract_request = openapi_client.DeliverContractRequest() # DeliverContractRequest | 

    try:
        # Deliver Cargo to Contract
        api_response = api_instance.deliver_contract(contract_id, deliver_contract_request)
        print("The response of ContractsApi->deliver_contract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractsApi->deliver_contract: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_id** | **str**| The ID of the contract. | 
 **deliver_contract_request** | [**DeliverContractRequest**](DeliverContractRequest.md)|  | 

### Return type

[**DeliverContract200Response**](DeliverContract200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully delivered cargo to contract. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fulfill_contract**
> FulfillContract200Response fulfill_contract(contract_id)

Fulfill Contract

Fulfill a contract. Can only be used on contracts that have all of their delivery terms fulfilled.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.fulfill_contract200_response import FulfillContract200Response
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
    api_instance = openapi_client.ContractsApi(api_client)
    contract_id = 'contract_id_example' # str | The ID of the contract to fulfill.

    try:
        # Fulfill Contract
        api_response = api_instance.fulfill_contract(contract_id)
        print("The response of ContractsApi->fulfill_contract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractsApi->fulfill_contract: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_id** | **str**| The ID of the contract to fulfill. | 

### Return type

[**FulfillContract200Response**](FulfillContract200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully fulfilled a contract. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_contract**
> GetContract200Response get_contract(contract_id)

Get Contract

Get the details of a specific contract.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_contract200_response import GetContract200Response
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
    api_instance = openapi_client.ContractsApi(api_client)
    contract_id = 'contract_id_example' # str | The contract ID to accept.

    try:
        # Get Contract
        api_response = api_instance.get_contract(contract_id)
        print("The response of ContractsApi->get_contract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractsApi->get_contract: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **contract_id** | **str**| The contract ID to accept. | 

### Return type

[**GetContract200Response**](GetContract200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully fetched contract. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_contracts**
> GetContracts200Response get_contracts(page=page, limit=limit)

List Contracts

Return a paginated list of all your contracts.

### Example

* Bearer (JWT) Authentication (AgentToken):

```python
import openapi_client
from openapi_client.models.get_contracts200_response import GetContracts200Response
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
    api_instance = openapi_client.ContractsApi(api_client)
    page = 1 # int | What entry offset to request (optional) (default to 1)
    limit = 10 # int | How many entries to return per page (optional) (default to 10)

    try:
        # List Contracts
        api_response = api_instance.get_contracts(page=page, limit=limit)
        print("The response of ContractsApi->get_contracts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractsApi->get_contracts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| What entry offset to request | [optional] [default to 1]
 **limit** | **int**| How many entries to return per page | [optional] [default to 10]

### Return type

[**GetContracts200Response**](GetContracts200Response.md)

### Authorization

[AgentToken](../README.md#AgentToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully listed contracts. |  -  |

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
    api_instance = openapi_client.ContractsApi(api_client)
    ship_symbol = 'ship_symbol_example' # str | The symbol of the ship.

    try:
        # Negotiate Contract
        api_response = api_instance.negotiate_contract(ship_symbol)
        print("The response of ContractsApi->negotiate_contract:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ContractsApi->negotiate_contract: %s\n" % e)
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

