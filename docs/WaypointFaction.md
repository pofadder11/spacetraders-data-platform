# WaypointFaction

The faction that controls the waypoint.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**FactionSymbol**](FactionSymbol.md) |  | 

## Example

```python
from openapi_client.models.waypoint_faction import WaypointFaction

# TODO update the JSON string below
json = "{}"
# create an instance of WaypointFaction from a JSON string
waypoint_faction_instance = WaypointFaction.from_json(json)
# print the JSON string representation of the object
print(WaypointFaction.to_json())

# convert the object into a dict
waypoint_faction_dict = waypoint_faction_instance.to_dict()
# create an instance of WaypointFaction from a dict
waypoint_faction_from_dict = WaypointFaction.from_dict(waypoint_faction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


