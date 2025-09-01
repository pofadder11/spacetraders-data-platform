# Extraction

Extraction details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_symbol** | **str** | Symbol of the ship that executed the extraction. | 
**var_yield** | [**ExtractionYield**](ExtractionYield.md) |  | 

## Example

```python
from openapi_client.models.extraction import Extraction

# TODO update the JSON string below
json = "{}"
# create an instance of Extraction from a JSON string
extraction_instance = Extraction.from_json(json)
# print the JSON string representation of the object
print(Extraction.to_json())

# convert the object into a dict
extraction_dict = extraction_instance.to_dict()
# create an instance of Extraction from a dict
extraction_from_dict = Extraction.from_dict(extraction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


