# Ship

Ship details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The globally unique identifier of the ship in the following format: &#x60;[AGENT_SYMBOL]-[HEX_ID]&#x60; | 
**registration** | [**ShipRegistration**](ShipRegistration.md) |  | 
**nav** | [**ShipNav**](ShipNav.md) |  | 
**crew** | [**ShipCrew**](ShipCrew.md) |  | 
**frame** | [**ShipFrame**](ShipFrame.md) |  | 
**reactor** | [**ShipReactor**](ShipReactor.md) |  | 
**engine** | [**ShipEngine**](ShipEngine.md) |  | 
**modules** | [**List[ShipModule]**](ShipModule.md) | Modules installed in this ship. | 
**mounts** | [**List[ShipMount]**](ShipMount.md) | Mounts installed in this ship. | 
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 
**fuel** | [**ShipFuel**](ShipFuel.md) |  | 
**cooldown** | [**Cooldown**](Cooldown.md) |  | 

## Example

```python
from openapi_client.models.ship import Ship

# TODO update the JSON string below
json = "{}"
# create an instance of Ship from a JSON string
ship_instance = Ship.from_json(json)
# print the JSON string representation of the object
print(Ship.to_json())

# convert the object into a dict
ship_dict = ship_instance.to_dict()
# create an instance of Ship from a dict
ship_from_dict = Ship.from_dict(ship_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


