# SystemWaypoint

Waypoint details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the waypoint. | 
**type** | [**WaypointType**](WaypointType.md) |  | 
**x** | **int** | Relative position of the waypoint on the system&#39;s x axis. This is not an absolute position in the universe. | 
**y** | **int** | Relative position of the waypoint on the system&#39;s y axis. This is not an absolute position in the universe. | 
**orbitals** | [**List[WaypointOrbital]**](WaypointOrbital.md) | Waypoints that orbit this waypoint. | 
**orbits** | **str** | The symbol of the parent waypoint, if this waypoint is in orbit around another waypoint. Otherwise this value is undefined. | [optional] 

## Example

```python
from openapi_client.models.system_waypoint import SystemWaypoint

# TODO update the JSON string below
json = "{}"
# create an instance of SystemWaypoint from a JSON string
system_waypoint_instance = SystemWaypoint.from_json(json)
# print the JSON string representation of the object
print(SystemWaypoint.to_json())

# convert the object into a dict
system_waypoint_dict = system_waypoint_instance.to_dict()
# create an instance of SystemWaypoint from a dict
system_waypoint_from_dict = SystemWaypoint.from_dict(system_waypoint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


