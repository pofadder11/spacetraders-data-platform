# ShipFuelConsumed

An object that only shows up when an action has consumed fuel in the process. Shows the fuel consumption data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **int** | The amount of fuel consumed by the most recent transit or action. | 
**timestamp** | **datetime** | The time at which the fuel was consumed. | 

## Example

```python
from openapi_client.models.ship_fuel_consumed import ShipFuelConsumed

# TODO update the JSON string below
json = "{}"
# create an instance of ShipFuelConsumed from a JSON string
ship_fuel_consumed_instance = ShipFuelConsumed.from_json(json)
# print the JSON string representation of the object
print(ShipFuelConsumed.to_json())

# convert the object into a dict
ship_fuel_consumed_dict = ship_fuel_consumed_instance.to_dict()
# create an instance of ShipFuelConsumed from a dict
ship_fuel_consumed_from_dict = ShipFuelConsumed.from_dict(ship_fuel_consumed_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


