# Shipyard

Shipyard details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the shipyard. The symbol is the same as the waypoint where the shipyard is located. | 
**ship_types** | [**List[ShipyardShipTypesInner]**](ShipyardShipTypesInner.md) | The list of ship types available for purchase at this shipyard. | 
**transactions** | [**List[ShipyardTransaction]**](ShipyardTransaction.md) | The list of recent transactions at this shipyard. | [optional] 
**ships** | [**List[ShipyardShip]**](ShipyardShip.md) | The ships that are currently available for purchase at the shipyard. | [optional] 
**modifications_fee** | **int** | The fee to modify a ship at this shipyard. This includes installing or removing modules and mounts on a ship. In the case of mounts, the fee is a flat rate per mount. In the case of modules, the fee is per slot the module occupies. | 

## Example

```python
from openapi_client.models.shipyard import Shipyard

# TODO update the JSON string below
json = "{}"
# create an instance of Shipyard from a JSON string
shipyard_instance = Shipyard.from_json(json)
# print the JSON string representation of the object
print(Shipyard.to_json())

# convert the object into a dict
shipyard_dict = shipyard_instance.to_dict()
# create an instance of Shipyard from a dict
shipyard_from_dict = Shipyard.from_dict(shipyard_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


