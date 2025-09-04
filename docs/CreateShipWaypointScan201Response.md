# CreateShipWaypointScan201Response

Successfully scanned for nearby waypoints.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**CreateShipWaypointScan201ResponseData**](CreateShipWaypointScan201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.create_ship_waypoint_scan201_response import CreateShipWaypointScan201Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateShipWaypointScan201Response from a JSON string
create_ship_waypoint_scan201_response_instance = CreateShipWaypointScan201Response.from_json(json)
# print the JSON string representation of the object
print(CreateShipWaypointScan201Response.to_json())

# convert the object into a dict
create_ship_waypoint_scan201_response_dict = create_ship_waypoint_scan201_response_instance.to_dict()
# create an instance of CreateShipWaypointScan201Response from a dict
create_ship_waypoint_scan201_response_from_dict = CreateShipWaypointScan201Response.from_dict(create_ship_waypoint_scan201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


