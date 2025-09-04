# ShipCargo

Ship cargo details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**capacity** | **int** | The max number of items that can be stored in the cargo hold. | 
**units** | **int** | The number of items currently stored in the cargo hold. | 
**inventory** | [**List[ShipCargoItem]**](ShipCargoItem.md) | The items currently in the cargo hold. | 

## Example

```python
from openapi_client.models.ship_cargo import ShipCargo

# TODO update the JSON string below
json = "{}"
# create an instance of ShipCargo from a JSON string
ship_cargo_instance = ShipCargo.from_json(json)
# print the JSON string representation of the object
print(ShipCargo.to_json())

# convert the object into a dict
ship_cargo_dict = ship_cargo_instance.to_dict()
# create an instance of ShipCargo from a dict
ship_cargo_from_dict = ShipCargo.from_dict(ship_cargo_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


