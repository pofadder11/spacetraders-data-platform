# ShipCargoItem

The type of cargo item and the number of units.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**TradeSymbol**](TradeSymbol.md) |  | 
**name** | **str** | The name of the cargo item type. | 
**description** | **str** | The description of the cargo item type. | 
**units** | **int** | The number of units of the cargo item. | 

## Example

```python
from openapi_client.models.ship_cargo_item import ShipCargoItem

# TODO update the JSON string below
json = "{}"
# create an instance of ShipCargoItem from a JSON string
ship_cargo_item_instance = ShipCargoItem.from_json(json)
# print the JSON string representation of the object
print(ShipCargoItem.to_json())

# convert the object into a dict
ship_cargo_item_dict = ship_cargo_item_instance.to_dict()
# create an instance of ShipCargoItem from a dict
ship_cargo_item_from_dict = ShipCargoItem.from_dict(ship_cargo_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


