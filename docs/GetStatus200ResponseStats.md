# GetStatus200ResponseStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accounts** | **int** | Total number of accounts registered on the game server. | [optional] 
**agents** | **int** | Number of registered agents in the game. | 
**ships** | **int** | Total number of ships in the game. | 
**systems** | **int** | Total number of systems in the game. | 
**waypoints** | **int** | Total number of waypoints in the game. | 

## Example

```python
from openapi_client.models.get_status200_response_stats import GetStatus200ResponseStats

# TODO update the JSON string below
json = "{}"
# create an instance of GetStatus200ResponseStats from a JSON string
get_status200_response_stats_instance = GetStatus200ResponseStats.from_json(json)
# print the JSON string representation of the object
print(GetStatus200ResponseStats.to_json())

# convert the object into a dict
get_status200_response_stats_dict = get_status200_response_stats_instance.to_dict()
# create an instance of GetStatus200ResponseStats from a dict
get_status200_response_stats_from_dict = GetStatus200ResponseStats.from_dict(get_status200_response_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


