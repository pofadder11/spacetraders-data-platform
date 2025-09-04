# GetStatus200ResponseHealth


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**last_market_update** | **str** | The date/time when the market was last updated. | [optional] 

## Example

```python
from openapi_client.models.get_status200_response_health import GetStatus200ResponseHealth

# TODO update the JSON string below
json = "{}"
# create an instance of GetStatus200ResponseHealth from a JSON string
get_status200_response_health_instance = GetStatus200ResponseHealth.from_json(json)
# print the JSON string representation of the object
print(GetStatus200ResponseHealth.to_json())

# convert the object into a dict
get_status200_response_health_dict = get_status200_response_health_instance.to_dict()
# create an instance of GetStatus200ResponseHealth from a dict
get_status200_response_health_from_dict = GetStatus200ResponseHealth.from_dict(get_status200_response_health_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


