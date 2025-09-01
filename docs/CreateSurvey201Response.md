# CreateSurvey201Response

Surveys has been created.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**CreateSurvey201ResponseData**](CreateSurvey201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.create_survey201_response import CreateSurvey201Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSurvey201Response from a JSON string
create_survey201_response_instance = CreateSurvey201Response.from_json(json)
# print the JSON string representation of the object
print(CreateSurvey201Response.to_json())

# convert the object into a dict
create_survey201_response_dict = create_survey201_response_instance.to_dict()
# create an instance of CreateSurvey201Response from a dict
create_survey201_response_from_dict = CreateSurvey201Response.from_dict(create_survey201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


