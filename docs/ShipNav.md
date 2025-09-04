# ShipNav

The navigation information of the ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**system_symbol** | **str** | The symbol of the system. | 
**waypoint_symbol** | **str** | The symbol of the waypoint. | 
**route** | [**ShipNavRoute**](ShipNavRoute.md) |  | 
**status** | [**ShipNavStatus**](ShipNavStatus.md) |  | 
**flight_mode** | [**ShipNavFlightMode**](ShipNavFlightMode.md) |  | [default to ShipNavFlightMode.CRUISE]

## Example

```python
from openapi_client.models.ship_nav import ShipNav

# TODO update the JSON string below
json = "{}"
# create an instance of ShipNav from a JSON string
ship_nav_instance = ShipNav.from_json(json)
# print the JSON string representation of the object
print(ShipNav.to_json())

# convert the object into a dict
ship_nav_dict = ship_nav_instance.to_dict()
# create an instance of ShipNav from a dict
ship_nav_from_dict = ShipNav.from_dict(ship_nav_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


