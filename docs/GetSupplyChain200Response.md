# GetSupplyChain200Response

Successfully retrieved the supply chain information

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**GetSupplyChain200ResponseData**](GetSupplyChain200ResponseData.md) |  | 

## Example

```python
from openapi_client.models.get_supply_chain200_response import GetSupplyChain200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetSupplyChain200Response from a JSON string
get_supply_chain200_response_instance = GetSupplyChain200Response.from_json(json)
# print the JSON string representation of the object
print(GetSupplyChain200Response.to_json())

# convert the object into a dict
get_supply_chain200_response_dict = get_supply_chain200_response_instance.to_dict()
# create an instance of GetSupplyChain200Response from a dict
get_supply_chain200_response_from_dict = GetSupplyChain200Response.from_dict(get_supply_chain200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


