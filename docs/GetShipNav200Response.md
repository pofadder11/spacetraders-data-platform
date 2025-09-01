# GetShipNav200Response

The current nav status of the ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**ShipNav**](ShipNav.md) |  | 

## Example

```python
from openapi_client.models.get_ship_nav200_response import GetShipNav200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipNav200Response from a JSON string
get_ship_nav200_response_instance = GetShipNav200Response.from_json(json)
# print the JSON string representation of the object
print(GetShipNav200Response.to_json())

# convert the object into a dict
get_ship_nav200_response_dict = get_ship_nav200_response_instance.to_dict()
# create an instance of GetShipNav200Response from a dict
get_ship_nav200_response_from_dict = GetShipNav200Response.from_dict(get_ship_nav200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


