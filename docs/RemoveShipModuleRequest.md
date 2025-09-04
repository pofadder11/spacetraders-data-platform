# RemoveShipModuleRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the module to remove. | 

## Example

```python
from openapi_client.models.remove_ship_module_request import RemoveShipModuleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RemoveShipModuleRequest from a JSON string
remove_ship_module_request_instance = RemoveShipModuleRequest.from_json(json)
# print the JSON string representation of the object
print(RemoveShipModuleRequest.to_json())

# convert the object into a dict
remove_ship_module_request_dict = remove_ship_module_request_instance.to_dict()
# create an instance of RemoveShipModuleRequest from a dict
remove_ship_module_request_from_dict = RemoveShipModuleRequest.from_dict(remove_ship_module_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


