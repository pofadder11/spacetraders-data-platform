# GetMounts200Response

Successfully retrieved ship mounts.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[ShipMount]**](ShipMount.md) |  | 

## Example

```python
from openapi_client.models.get_mounts200_response import GetMounts200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetMounts200Response from a JSON string
get_mounts200_response_instance = GetMounts200Response.from_json(json)
# print the JSON string representation of the object
print(GetMounts200Response.to_json())

# convert the object into a dict
get_mounts200_response_dict = get_mounts200_response_instance.to_dict()
# create an instance of GetMounts200Response from a dict
get_mounts200_response_from_dict = GetMounts200Response.from_dict(get_mounts200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


