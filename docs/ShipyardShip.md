# ShipyardShip

Ship details available at a shipyard.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**ShipType**](ShipType.md) |  | 
**name** | **str** | Name of the ship. | 
**description** | **str** | Description of the ship. | 
**activity** | [**ActivityLevel**](ActivityLevel.md) |  | [optional] 
**supply** | [**SupplyLevel**](SupplyLevel.md) |  | 
**purchase_price** | **int** | The purchase price of the ship. | 
**frame** | [**ShipFrame**](ShipFrame.md) |  | 
**reactor** | [**ShipReactor**](ShipReactor.md) |  | 
**engine** | [**ShipEngine**](ShipEngine.md) |  | 
**modules** | [**List[ShipModule]**](ShipModule.md) | Modules installed in this ship. | 
**mounts** | [**List[ShipMount]**](ShipMount.md) | Mounts installed in this ship. | 
**crew** | [**ShipyardShipCrew**](ShipyardShipCrew.md) |  | 

## Example

```python
from openapi_client.models.shipyard_ship import ShipyardShip

# TODO update the JSON string below
json = "{}"
# create an instance of ShipyardShip from a JSON string
shipyard_ship_instance = ShipyardShip.from_json(json)
# print the JSON string representation of the object
print(ShipyardShip.to_json())

# convert the object into a dict
shipyard_ship_dict = shipyard_ship_instance.to_dict()
# create an instance of ShipyardShip from a dict
shipyard_ship_from_dict = ShipyardShip.from_dict(shipyard_ship_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


