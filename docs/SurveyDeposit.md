# SurveyDeposit

A surveyed deposit of a mineral or resource available for extraction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**TradeSymbol**](TradeSymbol.md) | The symbol of the deposit. | 

## Example

```python
from openapi_client.models.survey_deposit import SurveyDeposit

# TODO update the JSON string below
json = "{}"
# create an instance of SurveyDeposit from a JSON string
survey_deposit_instance = SurveyDeposit.from_json(json)
# print the JSON string representation of the object
print(SurveyDeposit.to_json())

# convert the object into a dict
survey_deposit_dict = survey_deposit_instance.to_dict()
# create an instance of SurveyDeposit from a dict
survey_deposit_from_dict = SurveyDeposit.from_dict(survey_deposit_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


