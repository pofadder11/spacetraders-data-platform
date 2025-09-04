# InstallShipModuleRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the module to install. | 

## Example

```python
from openapi_client.models.install_ship_module_request import InstallShipModuleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of InstallShipModuleRequest from a JSON string
install_ship_module_request_instance = InstallShipModuleRequest.from_json(json)
# print the JSON string representation of the object
print(InstallShipModuleRequest.to_json())

# convert the object into a dict
install_ship_module_request_dict = install_ship_module_request_instance.to_dict()
# create an instance of InstallShipModuleRequest from a dict
install_ship_module_request_from_dict = InstallShipModuleRequest.from_dict(install_ship_module_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


