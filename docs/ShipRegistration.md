# ShipRegistration

The public registration information of the ship

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The agent&#39;s registered name of the ship | 
**faction_symbol** | **str** | The symbol of the faction the ship is registered with | 
**role** | [**ShipRole**](ShipRole.md) |  | 

## Example

```python
from openapi_client.models.ship_registration import ShipRegistration

# TODO update the JSON string below
json = "{}"
# create an instance of ShipRegistration from a JSON string
ship_registration_instance = ShipRegistration.from_json(json)
# print the JSON string representation of the object
print(ShipRegistration.to_json())

# convert the object into a dict
ship_registration_dict = ship_registration_instance.to_dict()
# create an instance of ShipRegistration from a dict
ship_registration_from_dict = ShipRegistration.from_dict(ship_registration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


