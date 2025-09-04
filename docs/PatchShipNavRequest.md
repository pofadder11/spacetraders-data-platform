# PatchShipNavRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**flight_mode** | [**ShipNavFlightMode**](ShipNavFlightMode.md) |  | [optional] [default to ShipNavFlightMode.CRUISE]

## Example

```python
from openapi_client.models.patch_ship_nav_request import PatchShipNavRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchShipNavRequest from a JSON string
patch_ship_nav_request_instance = PatchShipNavRequest.from_json(json)
# print the JSON string representation of the object
print(PatchShipNavRequest.to_json())

# convert the object into a dict
patch_ship_nav_request_dict = patch_ship_nav_request_instance.to_dict()
# create an instance of PatchShipNavRequest from a dict
patch_ship_nav_request_from_dict = PatchShipNavRequest.from_dict(patch_ship_nav_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


