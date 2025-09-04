# GetWaypoint200Response

Successfully fetched waypoint details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**Waypoint**](Waypoint.md) |  | 

## Example

```python
from openapi_client.models.get_waypoint200_response import GetWaypoint200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetWaypoint200Response from a JSON string
get_waypoint200_response_instance = GetWaypoint200Response.from_json(json)
# print the JSON string representation of the object
print(GetWaypoint200Response.to_json())

# convert the object into a dict
get_waypoint200_response_dict = get_waypoint200_response_instance.to_dict()
# create an instance of GetWaypoint200Response from a dict
get_waypoint200_response_from_dict = GetWaypoint200Response.from_dict(get_waypoint200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


