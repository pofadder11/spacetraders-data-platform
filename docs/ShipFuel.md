# ShipFuel

Details of the ship's fuel tanks including how much fuel was consumed during the last transit or action.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**current** | **int** | The current amount of fuel in the ship&#39;s tanks. | 
**capacity** | **int** | The maximum amount of fuel the ship&#39;s tanks can hold. | 
**consumed** | [**ShipFuelConsumed**](ShipFuelConsumed.md) |  | [optional] 

## Example

```python
from openapi_client.models.ship_fuel import ShipFuel

# TODO update the JSON string below
json = "{}"
# create an instance of ShipFuel from a JSON string
ship_fuel_instance = ShipFuel.from_json(json)
# print the JSON string representation of the object
print(ShipFuel.to_json())

# convert the object into a dict
ship_fuel_dict = ship_fuel_instance.to_dict()
# create an instance of ShipFuel from a dict
ship_fuel_from_dict = ShipFuel.from_dict(ship_fuel_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


