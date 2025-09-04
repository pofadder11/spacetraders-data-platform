# GetFactions200Response

Successfully fetched factions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[Faction]**](Faction.md) |  | 
**meta** | [**Meta**](Meta.md) |  | 

## Example

```python
from openapi_client.models.get_factions200_response import GetFactions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetFactions200Response from a JSON string
get_factions200_response_instance = GetFactions200Response.from_json(json)
# print the JSON string representation of the object
print(GetFactions200Response.to_json())

# convert the object into a dict
get_factions200_response_dict = get_factions200_response_instance.to_dict()
# create an instance of GetFactions200Response from a dict
get_factions200_response_from_dict = GetFactions200Response.from_dict(get_factions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


