# ShipEngine

The engine determines how quickly a ship travels between waypoints.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the engine. | 
**name** | **str** | The name of the engine. | 
**condition** | **float** | The repairable condition of a component. A value of 0 indicates the component needs significant repairs, while a value of 1 indicates the component is in near perfect condition. As the condition of a component is repaired, the overall integrity of the component decreases. | 
**integrity** | **float** | The overall integrity of the component, which determines the performance of the component. A value of 0 indicates that the component is almost completely degraded, while a value of 1 indicates that the component is in near perfect condition. The integrity of the component is non-repairable, and represents permanent wear over time. | 
**description** | **str** | The description of the engine. | 
**speed** | **int** | The speed stat of this engine. The higher the speed, the faster a ship can travel from one point to another. Reduces the time of arrival when navigating the ship. | 
**requirements** | [**ShipRequirements**](ShipRequirements.md) |  | 
**quality** | **float** | The overall quality of the component, which determines the quality of the component. High quality components return more ships parts and ship plating when a ship is scrapped. But also require more of these parts to repair. This is transparent to the player, as the parts are bought from/sold to the marketplace. | 

## Example

```python
from openapi_client.models.ship_engine import ShipEngine

# TODO update the JSON string below
json = "{}"
# create an instance of ShipEngine from a JSON string
ship_engine_instance = ShipEngine.from_json(json)
# print the JSON string representation of the object
print(ShipEngine.to_json())

# convert the object into a dict
ship_engine_dict = ship_engine_instance.to_dict()
# create an instance of ShipEngine from a dict
ship_engine_from_dict = ShipEngine.from_dict(ship_engine_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


