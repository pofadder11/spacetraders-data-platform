# CreateShipWaypointScan201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cooldown** | [**Cooldown**](Cooldown.md) |  | 
**waypoints** | [**List[ScannedWaypoint]**](ScannedWaypoint.md) | List of scanned waypoints. | 

## Example

```python
from openapi_client.models.create_ship_waypoint_scan201_response_data import CreateShipWaypointScan201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of CreateShipWaypointScan201ResponseData from a JSON string
create_ship_waypoint_scan201_response_data_instance = CreateShipWaypointScan201ResponseData.from_json(json)
# print the JSON string representation of the object
print(CreateShipWaypointScan201ResponseData.to_json())

# convert the object into a dict
create_ship_waypoint_scan201_response_data_dict = create_ship_waypoint_scan201_response_data_instance.to_dict()
# create an instance of CreateShipWaypointScan201ResponseData from a dict
create_ship_waypoint_scan201_response_data_from_dict = CreateShipWaypointScan201ResponseData.from_dict(create_ship_waypoint_scan201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


