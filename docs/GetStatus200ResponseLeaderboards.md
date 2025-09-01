# GetStatus200ResponseLeaderboards


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**most_credits** | [**List[GetStatus200ResponseLeaderboardsMostCreditsInner]**](GetStatus200ResponseLeaderboardsMostCreditsInner.md) | Top agents with the most credits. | 
**most_submitted_charts** | [**List[GetStatus200ResponseLeaderboardsMostSubmittedChartsInner]**](GetStatus200ResponseLeaderboardsMostSubmittedChartsInner.md) | Top agents with the most charted submitted. | 

## Example

```python
from openapi_client.models.get_status200_response_leaderboards import GetStatus200ResponseLeaderboards

# TODO update the JSON string below
json = "{}"
# create an instance of GetStatus200ResponseLeaderboards from a JSON string
get_status200_response_leaderboards_instance = GetStatus200ResponseLeaderboards.from_json(json)
# print the JSON string representation of the object
print(GetStatus200ResponseLeaderboards.to_json())

# convert the object into a dict
get_status200_response_leaderboards_dict = get_status200_response_leaderboards_instance.to_dict()
# create an instance of GetStatus200ResponseLeaderboards from a dict
get_status200_response_leaderboards_from_dict = GetStatus200ResponseLeaderboards.from_dict(get_status200_response_leaderboards_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


