# Register201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** | A Bearer token for accessing secured API endpoints. | 
**agent** | [**Agent**](Agent.md) |  | 
**faction** | [**Faction**](Faction.md) |  | 
**contract** | [**Contract**](Contract.md) |  | 
**ships** | [**List[Ship]**](Ship.md) |  | 

## Example

```python
from openapi_client.models.register201_response_data import Register201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of Register201ResponseData from a JSON string
register201_response_data_instance = Register201ResponseData.from_json(json)
# print the JSON string representation of the object
print(Register201ResponseData.to_json())

# convert the object into a dict
register201_response_data_dict = register201_response_data_instance.to_dict()
# create an instance of Register201ResponseData from a dict
register201_response_data_from_dict = Register201ResponseData.from_dict(register201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


