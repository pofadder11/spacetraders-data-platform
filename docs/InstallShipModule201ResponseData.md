# InstallShipModule201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent** | [**Agent**](Agent.md) |  | 
**modules** | [**List[ShipModule]**](ShipModule.md) |  | 
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 
**transaction** | [**ShipModificationTransaction**](ShipModificationTransaction.md) |  | 

## Example

```python
from openapi_client.models.install_ship_module201_response_data import InstallShipModule201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of InstallShipModule201ResponseData from a JSON string
install_ship_module201_response_data_instance = InstallShipModule201ResponseData.from_json(json)
# print the JSON string representation of the object
print(InstallShipModule201ResponseData.to_json())

# convert the object into a dict
install_ship_module201_response_data_dict = install_ship_module201_response_data_instance.to_dict()
# create an instance of InstallShipModule201ResponseData from a dict
install_ship_module201_response_data_from_dict = InstallShipModule201ResponseData.from_dict(install_ship_module201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


