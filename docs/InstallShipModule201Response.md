# InstallShipModule201Response

Successfully installed the module on the ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**InstallShipModule201ResponseData**](InstallShipModule201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.install_ship_module201_response import InstallShipModule201Response

# TODO update the JSON string below
json = "{}"
# create an instance of InstallShipModule201Response from a JSON string
install_ship_module201_response_instance = InstallShipModule201Response.from_json(json)
# print the JSON string representation of the object
print(InstallShipModule201Response.to_json())

# convert the object into a dict
install_ship_module201_response_dict = install_ship_module201_response_instance.to_dict()
# create an instance of InstallShipModule201Response from a dict
install_ship_module201_response_from_dict = InstallShipModule201Response.from_dict(install_ship_module201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


