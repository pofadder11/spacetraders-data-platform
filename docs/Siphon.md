# Siphon

Siphon details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_symbol** | **str** | Symbol of the ship that executed the siphon. | 
**var_yield** | [**SiphonYield**](SiphonYield.md) |  | 

## Example

```python
from openapi_client.models.siphon import Siphon

# TODO update the JSON string below
json = "{}"
# create an instance of Siphon from a JSON string
siphon_instance = Siphon.from_json(json)
# print the JSON string representation of the object
print(Siphon.to_json())

# convert the object into a dict
siphon_dict = siphon_instance.to_dict()
# create an instance of Siphon from a dict
siphon_from_dict = Siphon.from_dict(siphon_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


