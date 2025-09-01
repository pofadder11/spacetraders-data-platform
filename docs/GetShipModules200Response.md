# GetShipModules200Response

Successfully retrieved ship modules.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[ShipModule]**](ShipModule.md) |  | 

## Example

```python
from openapi_client.models.get_ship_modules200_response import GetShipModules200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipModules200Response from a JSON string
get_ship_modules200_response_instance = GetShipModules200Response.from_json(json)
# print the JSON string representation of the object
print(GetShipModules200Response.to_json())

# convert the object into a dict
get_ship_modules200_response_dict = get_ship_modules200_response_instance.to_dict()
# create an instance of GetShipModules200Response from a dict
get_ship_modules200_response_from_dict = GetShipModules200Response.from_dict(get_ship_modules200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


