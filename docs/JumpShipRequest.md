# JumpShipRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waypoint_symbol** | **str** | The symbol of the waypoint to jump to. The destination must be a connected waypoint. | 

## Example

```python
from openapi_client.models.jump_ship_request import JumpShipRequest

# TODO update the JSON string below
json = "{}"
# create an instance of JumpShipRequest from a JSON string
jump_ship_request_instance = JumpShipRequest.from_json(json)
# print the JSON string representation of the object
print(JumpShipRequest.to_json())

# convert the object into a dict
jump_ship_request_dict = jump_ship_request_instance.to_dict()
# create an instance of JumpShipRequest from a dict
jump_ship_request_from_dict = JumpShipRequest.from_dict(jump_ship_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


