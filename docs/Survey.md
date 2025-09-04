# Survey

A resource survey of a waypoint, detailing a specific extraction location and the types of resources that can be found there.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**signature** | **str** | A unique signature for the location of this survey. This signature is verified when attempting an extraction using this survey. | 
**symbol** | **str** | The symbol of the waypoint that this survey is for. | 
**deposits** | [**List[SurveyDeposit]**](SurveyDeposit.md) | A list of deposits that can be found at this location. A ship will extract one of these deposits when using this survey in an extraction request. If multiple deposits of the same type are present, the chance of extracting that deposit is increased. | 
**expiration** | **datetime** | The date and time when the survey expires. After this date and time, the survey will no longer be available for extraction. | 
**size** | [**SurveySize**](SurveySize.md) |  | 

## Example

```python
from openapi_client.models.survey import Survey

# TODO update the JSON string below
json = "{}"
# create an instance of Survey from a JSON string
survey_instance = Survey.from_json(json)
# print the JSON string representation of the object
print(Survey.to_json())

# convert the object into a dict
survey_dict = survey_instance.to_dict()
# create an instance of Survey from a dict
survey_from_dict = Survey.from_dict(survey_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


