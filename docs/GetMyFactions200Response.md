# GetMyFactions200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[GetMyFactions200ResponseDataInner]**](GetMyFactions200ResponseDataInner.md) |  | 
**meta** | [**Meta**](Meta.md) |  | 

## Example

```python
from openapi_client.models.get_my_factions200_response import GetMyFactions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetMyFactions200Response from a JSON string
get_my_factions200_response_instance = GetMyFactions200Response.from_json(json)
# print the JSON string representation of the object
print(GetMyFactions200Response.to_json())

# convert the object into a dict
get_my_factions200_response_dict = get_my_factions200_response_instance.to_dict()
# create an instance of GetMyFactions200Response from a dict
get_my_factions200_response_from_dict = GetMyFactions200Response.from_dict(get_my_factions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


