# CreateSurvey201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cooldown** | [**Cooldown**](Cooldown.md) |  | 
**surveys** | [**List[Survey]**](Survey.md) | Surveys created by this action. | 

## Example

```python
from openapi_client.models.create_survey201_response_data import CreateSurvey201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSurvey201ResponseData from a JSON string
create_survey201_response_data_instance = CreateSurvey201ResponseData.from_json(json)
# print the JSON string representation of the object
print(CreateSurvey201ResponseData.to_json())

# convert the object into a dict
create_survey201_response_data_dict = create_survey201_response_data_instance.to_dict()
# create an instance of CreateSurvey201ResponseData from a dict
create_survey201_response_data_from_dict = CreateSurvey201ResponseData.from_dict(create_survey201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


