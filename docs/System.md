# System

System details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**constellation** | **str** | The constellation that the system is part of. | [optional] 
**symbol** | **str** | The symbol of the system. | 
**sector_symbol** | **str** | The symbol of the sector. | 
**type** | [**SystemType**](SystemType.md) |  | 
**x** | **int** | Relative position of the system in the sector in the x axis. | 
**y** | **int** | Relative position of the system in the sector in the y axis. | 
**waypoints** | [**List[SystemWaypoint]**](SystemWaypoint.md) | Waypoints in this system. | 
**factions** | [**List[SystemFaction]**](SystemFaction.md) | Factions that control this system. | 
**name** | **str** | The name of the system. | [optional] 

## Example

```python
from openapi_client.models.system import System

# TODO update the JSON string below
json = "{}"
# create an instance of System from a JSON string
system_instance = System.from_json(json)
# print the JSON string representation of the object
print(System.to_json())

# convert the object into a dict
system_dict = system_instance.to_dict()
# create an instance of System from a dict
system_from_dict = System.from_dict(system_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


