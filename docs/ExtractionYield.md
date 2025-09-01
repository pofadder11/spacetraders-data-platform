# ExtractionYield

A yield from the extraction operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**TradeSymbol**](TradeSymbol.md) |  | 
**units** | **int** | The number of units extracted that were placed into the ship&#39;s cargo hold. | 

## Example

```python
from openapi_client.models.extraction_yield import ExtractionYield

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractionYield from a JSON string
extraction_yield_instance = ExtractionYield.from_json(json)
# print the JSON string representation of the object
print(ExtractionYield.to_json())

# convert the object into a dict
extraction_yield_dict = extraction_yield_instance.to_dict()
# create an instance of ExtractionYield from a dict
extraction_yield_from_dict = ExtractionYield.from_dict(extraction_yield_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


