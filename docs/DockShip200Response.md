# DockShip200Response

The ship has successfully docked at its current location.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**DockShip200ResponseData**](DockShip200ResponseData.md) |  | 

## Example

```python
from openapi_client.models.dock_ship200_response import DockShip200Response

# TODO update the JSON string below
json = "{}"
# create an instance of DockShip200Response from a JSON string
dock_ship200_response_instance = DockShip200Response.from_json(json)
# print the JSON string representation of the object
print(DockShip200Response.to_json())

# convert the object into a dict
dock_ship200_response_dict = dock_ship200_response_instance.to_dict()
# create an instance of DockShip200Response from a dict
dock_ship200_response_from_dict = DockShip200Response.from_dict(dock_ship200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


