# GetStatus200Response

Fetched status successfully.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | The current status of the game server. | 
**version** | **str** | The current version of the API. | 
**reset_date** | **str** | The date when the game server was last reset. | 
**description** | **str** |  | 
**stats** | [**GetStatus200ResponseStats**](GetStatus200ResponseStats.md) |  | 
**health** | [**GetStatus200ResponseHealth**](GetStatus200ResponseHealth.md) |  | 
**leaderboards** | [**GetStatus200ResponseLeaderboards**](GetStatus200ResponseLeaderboards.md) |  | 
**server_resets** | [**GetStatus200ResponseServerResets**](GetStatus200ResponseServerResets.md) |  | 
**announcements** | [**List[GetStatus200ResponseAnnouncementsInner]**](GetStatus200ResponseAnnouncementsInner.md) |  | 
**links** | [**List[GetStatus200ResponseLinksInner]**](GetStatus200ResponseLinksInner.md) |  | 

## Example

```python
from openapi_client.models.get_status200_response import GetStatus200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetStatus200Response from a JSON string
get_status200_response_instance = GetStatus200Response.from_json(json)
# print the JSON string representation of the object
print(GetStatus200Response.to_json())

# convert the object into a dict
get_status200_response_dict = get_status200_response_instance.to_dict()
# create an instance of GetStatus200Response from a dict
get_status200_response_from_dict = GetStatus200Response.from_dict(get_status200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


