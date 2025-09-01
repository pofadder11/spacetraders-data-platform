# GetShipCooldown200Response

Successfully fetched ship's cooldown.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**Cooldown**](Cooldown.md) |  | 

## Example

```python
from openapi_client.models.get_ship_cooldown200_response import GetShipCooldown200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipCooldown200Response from a JSON string
get_ship_cooldown200_response_instance = GetShipCooldown200Response.from_json(json)
# print the JSON string representation of the object
print(GetShipCooldown200Response.to_json())

# convert the object into a dict
get_ship_cooldown200_response_dict = get_ship_cooldown200_response_instance.to_dict()
# create an instance of GetShipCooldown200Response from a dict
get_ship_cooldown200_response_from_dict = GetShipCooldown200Response.from_dict(get_ship_cooldown200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


