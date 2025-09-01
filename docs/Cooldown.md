# Cooldown

A cooldown is a period of time in which a ship cannot perform certain actions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_symbol** | **str** | The symbol of the ship that is on cooldown | 
**total_seconds** | **int** | The total duration of the cooldown in seconds | 
**remaining_seconds** | **int** | The remaining duration of the cooldown in seconds | 
**expiration** | **datetime** | The date and time when the cooldown expires in ISO 8601 format | [optional] 

## Example

```python
from openapi_client.models.cooldown import Cooldown

# TODO update the JSON string below
json = "{}"
# create an instance of Cooldown from a JSON string
cooldown_instance = Cooldown.from_json(json)
# print the JSON string representation of the object
print(Cooldown.to_json())

# convert the object into a dict
cooldown_dict = cooldown_instance.to_dict()
# create an instance of Cooldown from a dict
cooldown_from_dict = Cooldown.from_dict(cooldown_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


