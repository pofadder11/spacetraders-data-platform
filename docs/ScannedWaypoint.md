# ScannedWaypoint

A waypoint that was scanned by a ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the waypoint. | 
**type** | [**WaypointType**](WaypointType.md) |  | 
**system_symbol** | **str** | The symbol of the system. | 
**x** | **int** | Position in the universe in the x axis. | 
**y** | **int** | Position in the universe in the y axis. | 
**orbitals** | [**List[WaypointOrbital]**](WaypointOrbital.md) | List of waypoints that orbit this waypoint. | 
**faction** | [**WaypointFaction**](WaypointFaction.md) |  | [optional] 
**traits** | [**List[WaypointTrait]**](WaypointTrait.md) | The traits of the waypoint. | 
**chart** | [**Chart**](Chart.md) |  | [optional] 

## Example

```python
from openapi_client.models.scanned_waypoint import ScannedWaypoint

# TODO update the JSON string below
json = "{}"
# create an instance of ScannedWaypoint from a JSON string
scanned_waypoint_instance = ScannedWaypoint.from_json(json)
# print the JSON string representation of the object
print(ScannedWaypoint.to_json())

# convert the object into a dict
scanned_waypoint_dict = scanned_waypoint_instance.to_dict()
# create an instance of ScannedWaypoint from a dict
scanned_waypoint_from_dict = ScannedWaypoint.from_dict(scanned_waypoint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


