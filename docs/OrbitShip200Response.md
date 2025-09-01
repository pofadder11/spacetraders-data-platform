# OrbitShip200Response

The ship has successfully moved into orbit at its current location.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**DockShip200ResponseData**](DockShip200ResponseData.md) |  | 

## Example

```python
from openapi_client.models.orbit_ship200_response import OrbitShip200Response

# TODO update the JSON string below
json = "{}"
# create an instance of OrbitShip200Response from a JSON string
orbit_ship200_response_instance = OrbitShip200Response.from_json(json)
# print the JSON string representation of the object
print(OrbitShip200Response.to_json())

# convert the object into a dict
orbit_ship200_response_dict = orbit_ship200_response_instance.to_dict()
# create an instance of OrbitShip200Response from a dict
orbit_ship200_response_from_dict = OrbitShip200Response.from_dict(orbit_ship200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


