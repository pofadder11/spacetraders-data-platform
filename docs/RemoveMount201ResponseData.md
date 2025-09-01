# RemoveMount201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent** | [**Agent**](Agent.md) |  | 
**mounts** | [**List[ShipMount]**](ShipMount.md) | List of installed mounts after the removal of the selected mount. | 
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 
**transaction** | [**ShipModificationTransaction**](ShipModificationTransaction.md) |  | 

## Example

```python
from openapi_client.models.remove_mount201_response_data import RemoveMount201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of RemoveMount201ResponseData from a JSON string
remove_mount201_response_data_instance = RemoveMount201ResponseData.from_json(json)
# print the JSON string representation of the object
print(RemoveMount201ResponseData.to_json())

# convert the object into a dict
remove_mount201_response_data_dict = remove_mount201_response_data_instance.to_dict()
# create an instance of RemoveMount201ResponseData from a dict
remove_mount201_response_data_from_dict = RemoveMount201ResponseData.from_dict(remove_mount201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


