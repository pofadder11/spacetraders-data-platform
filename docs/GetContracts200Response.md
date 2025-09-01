# GetContracts200Response

Successfully listed contracts.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[Contract]**](Contract.md) |  | 
**meta** | [**Meta**](Meta.md) |  | 

## Example

```python
from openapi_client.models.get_contracts200_response import GetContracts200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetContracts200Response from a JSON string
get_contracts200_response_instance = GetContracts200Response.from_json(json)
# print the JSON string representation of the object
print(GetContracts200Response.to_json())

# convert the object into a dict
get_contracts200_response_dict = get_contracts200_response_instance.to_dict()
# create an instance of GetContracts200Response from a dict
get_contracts200_response_from_dict = GetContracts200Response.from_dict(get_contracts200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


