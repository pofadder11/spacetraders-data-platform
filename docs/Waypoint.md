# Waypoint

A waypoint is a location that ships can travel to such as a Planet, Moon or Space Station.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the waypoint. | 
**type** | [**WaypointType**](WaypointType.md) |  | 
**system_symbol** | **str** | The symbol of the system. | 
**x** | **int** | Relative position of the waypoint on the system&#39;s x axis. This is not an absolute position in the universe. | 
**y** | **int** | Relative position of the waypoint on the system&#39;s y axis. This is not an absolute position in the universe. | 
**orbitals** | [**List[WaypointOrbital]**](WaypointOrbital.md) | Waypoints that orbit this waypoint. | 
**orbits** | **str** | The symbol of the parent waypoint, if this waypoint is in orbit around another waypoint. Otherwise this value is undefined. | [optional] 
**faction** | [**WaypointFaction**](WaypointFaction.md) |  | [optional] 
**traits** | [**List[WaypointTrait]**](WaypointTrait.md) | The traits of the waypoint. | 
**modifiers** | [**List[WaypointModifier]**](WaypointModifier.md) | The modifiers of the waypoint. | [optional] 
**chart** | [**Chart**](Chart.md) |  | [optional] 
**is_under_construction** | **bool** | True if the waypoint is under construction. | 

## Example

```python
from openapi_client.models.waypoint import Waypoint

# TODO update the JSON string below
json = "{}"
# create an instance of Waypoint from a JSON string
waypoint_instance = Waypoint.from_json(json)
# print the JSON string representation of the object
print(Waypoint.to_json())

# convert the object into a dict
waypoint_dict = waypoint_instance.to_dict()
# create an instance of Waypoint from a dict
waypoint_from_dict = Waypoint.from_dict(waypoint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


