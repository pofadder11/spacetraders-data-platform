# InstallMount201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent** | [**Agent**](Agent.md) |  | 
**mounts** | [**List[ShipMount]**](ShipMount.md) | List of installed mounts after the installation of the new mount. | 
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 
**transaction** | [**ShipModificationTransaction**](ShipModificationTransaction.md) |  | 

## Example

```python
from openapi_client.models.install_mount201_response_data import InstallMount201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of InstallMount201ResponseData from a JSON string
install_mount201_response_data_instance = InstallMount201ResponseData.from_json(json)
# print the JSON string representation of the object
print(InstallMount201ResponseData.to_json())

# convert the object into a dict
install_mount201_response_data_dict = install_mount201_response_data_instance.to_dict()
# create an instance of InstallMount201ResponseData from a dict
install_mount201_response_data_from_dict = InstallMount201ResponseData.from_dict(install_mount201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


