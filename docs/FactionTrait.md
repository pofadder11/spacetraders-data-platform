# FactionTrait


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**FactionTraitSymbol**](FactionTraitSymbol.md) |  | 
**name** | **str** | The name of the trait. | 
**description** | **str** | A description of the trait. | 

## Example

```python
from openapi_client.models.faction_trait import FactionTrait

# TODO update the JSON string below
json = "{}"
# create an instance of FactionTrait from a JSON string
faction_trait_instance = FactionTrait.from_json(json)
# print the JSON string representation of the object
print(FactionTrait.to_json())

# convert the object into a dict
faction_trait_dict = faction_trait_instance.to_dict()
# create an instance of FactionTrait from a dict
faction_trait_from_dict = FactionTrait.from_dict(faction_trait_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


