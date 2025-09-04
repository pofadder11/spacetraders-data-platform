# ShipReactor

The reactor of the ship. The reactor is responsible for powering the ship's systems and weapons.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | Symbol of the reactor. | 
**name** | **str** | Name of the reactor. | 
**condition** | **float** | The repairable condition of a component. A value of 0 indicates the component needs significant repairs, while a value of 1 indicates the component is in near perfect condition. As the condition of a component is repaired, the overall integrity of the component decreases. | 
**integrity** | **float** | The overall integrity of the component, which determines the performance of the component. A value of 0 indicates that the component is almost completely degraded, while a value of 1 indicates that the component is in near perfect condition. The integrity of the component is non-repairable, and represents permanent wear over time. | 
**description** | **str** | Description of the reactor. | 
**power_output** | **int** | The amount of power provided by this reactor. The more power a reactor provides to the ship, the lower the cooldown it gets when using a module or mount that taxes the ship&#39;s power. | 
**requirements** | [**ShipRequirements**](ShipRequirements.md) |  | 
**quality** | **float** | The overall quality of the component, which determines the quality of the component. High quality components return more ships parts and ship plating when a ship is scrapped. But also require more of these parts to repair. This is transparent to the player, as the parts are bought from/sold to the marketplace. | 

## Example

```python
from openapi_client.models.ship_reactor import ShipReactor

# TODO update the JSON string below
json = "{}"
# create an instance of ShipReactor from a JSON string
ship_reactor_instance = ShipReactor.from_json(json)
# print the JSON string representation of the object
print(ShipReactor.to_json())

# convert the object into a dict
ship_reactor_dict = ship_reactor_instance.to_dict()
# create an instance of ShipReactor from a dict
ship_reactor_from_dict = ShipReactor.from_dict(ship_reactor_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


