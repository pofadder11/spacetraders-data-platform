# ShipConditionEvent

An event that represents damage or wear to a ship's reactor, frame, or engine, reducing the condition of the ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the event that occurred. | 
**component** | **str** |  | 
**name** | **str** | The name of the event. | 
**description** | **str** | A description of the event. | 

## Example

```python
from openapi_client.models.ship_condition_event import ShipConditionEvent

# TODO update the JSON string below
json = "{}"
# create an instance of ShipConditionEvent from a JSON string
ship_condition_event_instance = ShipConditionEvent.from_json(json)
# print the JSON string representation of the object
print(ShipConditionEvent.to_json())

# convert the object into a dict
ship_condition_event_dict = ship_condition_event_instance.to_dict()
# create an instance of ShipConditionEvent from a dict
ship_condition_event_from_dict = ShipConditionEvent.from_dict(ship_condition_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


