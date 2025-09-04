# ShipNavRoute

The routing information for the ship's most recent transit or current location.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**destination** | [**ShipNavRouteWaypoint**](ShipNavRouteWaypoint.md) |  | 
**origin** | [**ShipNavRouteWaypoint**](ShipNavRouteWaypoint.md) |  | 
**departure_time** | **datetime** | The date time of the ship&#39;s departure. | 
**arrival** | **datetime** | The date time of the ship&#39;s arrival. If the ship is in-transit, this is the expected time of arrival. | 

## Example

```python
from openapi_client.models.ship_nav_route import ShipNavRoute

# TODO update the JSON string below
json = "{}"
# create an instance of ShipNavRoute from a JSON string
ship_nav_route_instance = ShipNavRoute.from_json(json)
# print the JSON string representation of the object
print(ShipNavRoute.to_json())

# convert the object into a dict
ship_nav_route_dict = ship_nav_route_instance.to_dict()
# create an instance of ShipNavRoute from a dict
ship_nav_route_from_dict = ShipNavRoute.from_dict(ship_nav_route_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


