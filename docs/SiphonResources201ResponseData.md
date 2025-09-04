# SiphonResources201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**siphon** | [**Siphon**](Siphon.md) |  | 
**cooldown** | [**Cooldown**](Cooldown.md) |  | 
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 
**events** | [**List[ShipConditionEvent]**](ShipConditionEvent.md) |  | 

## Example

```python
from openapi_client.models.siphon_resources201_response_data import SiphonResources201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of SiphonResources201ResponseData from a JSON string
siphon_resources201_response_data_instance = SiphonResources201ResponseData.from_json(json)
# print the JSON string representation of the object
print(SiphonResources201ResponseData.to_json())

# convert the object into a dict
siphon_resources201_response_data_dict = siphon_resources201_response_data_instance.to_dict()
# create an instance of SiphonResources201ResponseData from a dict
siphon_resources201_response_data_from_dict = SiphonResources201ResponseData.from_dict(siphon_resources201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


