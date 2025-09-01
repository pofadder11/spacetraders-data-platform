# JettisonRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**TradeSymbol**](TradeSymbol.md) |  | 
**units** | **int** | Amount of units to jettison of this good. | 

## Example

```python
from openapi_client.models.jettison_request import JettisonRequest

# TODO update the JSON string below
json = "{}"
# create an instance of JettisonRequest from a JSON string
jettison_request_instance = JettisonRequest.from_json(json)
# print the JSON string representation of the object
print(JettisonRequest.to_json())

# convert the object into a dict
jettison_request_dict = jettison_request_instance.to_dict()
# create an instance of JettisonRequest from a dict
jettison_request_from_dict = JettisonRequest.from_dict(jettison_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


