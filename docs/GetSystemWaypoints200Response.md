# GetSystemWaypoints200Response

Successfully listed waypoints.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[Waypoint]**](Waypoint.md) |  | 
**meta** | [**Meta**](Meta.md) |  | 

## Example

```python
from openapi_client.models.get_system_waypoints200_response import GetSystemWaypoints200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetSystemWaypoints200Response from a JSON string
get_system_waypoints200_response_instance = GetSystemWaypoints200Response.from_json(json)
# print the JSON string representation of the object
print(GetSystemWaypoints200Response.to_json())

# convert the object into a dict
get_system_waypoints200_response_dict = get_system_waypoints200_response_instance.to_dict()
# create an instance of GetSystemWaypoints200Response from a dict
get_system_waypoints200_response_from_dict = GetSystemWaypoints200Response.from_dict(get_system_waypoints200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


