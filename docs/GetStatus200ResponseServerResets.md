# GetStatus200ResponseServerResets


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next** | **str** | The date and time when the game server will reset. | 
**frequency** | **str** | How often we intend to reset the game server. | 

## Example

```python
from openapi_client.models.get_status200_response_server_resets import GetStatus200ResponseServerResets

# TODO update the JSON string below
json = "{}"
# create an instance of GetStatus200ResponseServerResets from a JSON string
get_status200_response_server_resets_instance = GetStatus200ResponseServerResets.from_json(json)
# print the JSON string representation of the object
print(GetStatus200ResponseServerResets.to_json())

# convert the object into a dict
get_status200_response_server_resets_dict = get_status200_response_server_resets_instance.to_dict()
# create an instance of GetStatus200ResponseServerResets from a dict
get_status200_response_server_resets_from_dict = GetStatus200ResponseServerResets.from_dict(get_status200_response_server_resets_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


