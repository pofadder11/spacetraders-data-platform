# ShipModule

A module can be installed in a ship and provides a set of capabilities such as storage space or quarters for crew. Module installations are permanent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the module. | 
**name** | **str** | Name of this module. | 
**description** | **str** | Description of this module. | 
**capacity** | **int** | Modules that provide capacity, such as cargo hold or crew quarters will show this value to denote how much of a bonus the module grants. | [optional] 
**range** | **int** | Modules that have a range will such as a sensor array show this value to denote how far can the module reach with its capabilities. | [optional] 
**requirements** | [**ShipRequirements**](ShipRequirements.md) |  | 

## Example

```python
from openapi_client.models.ship_module import ShipModule

# TODO update the JSON string below
json = "{}"
# create an instance of ShipModule from a JSON string
ship_module_instance = ShipModule.from_json(json)
# print the JSON string representation of the object
print(ShipModule.to_json())

# convert the object into a dict
ship_module_dict = ship_module_instance.to_dict()
# create an instance of ShipModule from a dict
ship_module_from_dict = ShipModule.from_dict(ship_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


