# ShipNavRouteWaypoint

The destination or departure of a ships nav route.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the waypoint. | 
**type** | [**WaypointType**](WaypointType.md) |  | 
**system_symbol** | **str** | The symbol of the system. | 
**x** | **int** | Position in the universe in the x axis. | 
**y** | **int** | Position in the universe in the y axis. | 

## Example

```python
from openapi_client.models.ship_nav_route_waypoint import ShipNavRouteWaypoint

# TODO update the JSON string below
json = "{}"
# create an instance of ShipNavRouteWaypoint from a JSON string
ship_nav_route_waypoint_instance = ShipNavRouteWaypoint.from_json(json)
# print the JSON string representation of the object
print(ShipNavRouteWaypoint.to_json())

# convert the object into a dict
ship_nav_route_waypoint_dict = ship_nav_route_waypoint_instance.to_dict()
# create an instance of ShipNavRouteWaypoint from a dict
ship_nav_route_waypoint_from_dict = ShipNavRouteWaypoint.from_dict(ship_nav_route_waypoint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


