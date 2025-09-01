# Faction

Faction details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**FactionSymbol**](FactionSymbol.md) |  | 
**name** | **str** | Name of the faction. | 
**description** | **str** | Description of the faction. | 
**headquarters** | **str** | The waypoint in which the faction&#39;s HQ is located in. | [optional] 
**traits** | [**List[FactionTrait]**](FactionTrait.md) | List of traits that define this faction. | 
**is_recruiting** | **bool** | Whether or not the faction is currently recruiting new agents. | 

## Example

```python
from openapi_client.models.faction import Faction

# TODO update the JSON string below
json = "{}"
# create an instance of Faction from a JSON string
faction_instance = Faction.from_json(json)
# print the JSON string representation of the object
print(Faction.to_json())

# convert the object into a dict
faction_dict = faction_instance.to_dict()
# create an instance of Faction from a dict
faction_from_dict = Faction.from_dict(faction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


