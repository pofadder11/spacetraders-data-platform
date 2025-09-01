# NavigateShipRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waypoint_symbol** | **str** | The symbol of the waypoint to navigate/warp to. | 

## Example

```python
from openapi_client.models.navigate_ship_request import NavigateShipRequest

# TODO update the JSON string below
json = "{}"
# create an instance of NavigateShipRequest from a JSON string
navigate_ship_request_instance = NavigateShipRequest.from_json(json)
# print the JSON string representation of the object
print(NavigateShipRequest.to_json())

# convert the object into a dict
navigate_ship_request_dict = navigate_ship_request_instance.to_dict()
# create an instance of NavigateShipRequest from a dict
navigate_ship_request_from_dict = NavigateShipRequest.from_dict(navigate_ship_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


