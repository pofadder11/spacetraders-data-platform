# SiphonYield

A yield from the siphon operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**TradeSymbol**](TradeSymbol.md) |  | 
**units** | **int** | The number of units siphoned that were placed into the ship&#39;s cargo hold. | 

## Example

```python
from openapi_client.models.siphon_yield import SiphonYield

# TODO update the JSON string below
json = "{}"
# create an instance of SiphonYield from a JSON string
siphon_yield_instance = SiphonYield.from_json(json)
# print the JSON string representation of the object
print(SiphonYield.to_json())

# convert the object into a dict
siphon_yield_dict = siphon_yield_instance.to_dict()
# create an instance of SiphonYield from a dict
siphon_yield_from_dict = SiphonYield.from_dict(siphon_yield_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


