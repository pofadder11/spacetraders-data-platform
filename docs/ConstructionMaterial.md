# ConstructionMaterial

The details of the required construction materials for a given waypoint under construction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trade_symbol** | [**TradeSymbol**](TradeSymbol.md) |  | 
**required** | **int** | The number of units required. | 
**fulfilled** | **int** | The number of units fulfilled toward the required amount. | 

## Example

```python
from openapi_client.models.construction_material import ConstructionMaterial

# TODO update the JSON string below
json = "{}"
# create an instance of ConstructionMaterial from a JSON string
construction_material_instance = ConstructionMaterial.from_json(json)
# print the JSON string representation of the object
print(ConstructionMaterial.to_json())

# convert the object into a dict
construction_material_dict = construction_material_instance.to_dict()
# create an instance of ConstructionMaterial from a dict
construction_material_from_dict = ConstructionMaterial.from_dict(construction_material_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


