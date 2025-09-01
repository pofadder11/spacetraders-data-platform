# WaypointOrbital

An orbital is another waypoint that orbits a parent waypoint.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the orbiting waypoint. | 

## Example

```python
from openapi_client.models.waypoint_orbital import WaypointOrbital

# TODO update the JSON string below
json = "{}"
# create an instance of WaypointOrbital from a JSON string
waypoint_orbital_instance = WaypointOrbital.from_json(json)
# print the JSON string representation of the object
print(WaypointOrbital.to_json())

# convert the object into a dict
waypoint_orbital_dict = waypoint_orbital_instance.to_dict()
# create an instance of WaypointOrbital from a dict
waypoint_orbital_from_dict = WaypointOrbital.from_dict(waypoint_orbital_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


