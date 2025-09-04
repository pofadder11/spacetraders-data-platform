# RemoveMountRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the mount to remove. | 

## Example

```python
from openapi_client.models.remove_mount_request import RemoveMountRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RemoveMountRequest from a JSON string
remove_mount_request_instance = RemoveMountRequest.from_json(json)
# print the JSON string representation of the object
print(RemoveMountRequest.to_json())

# convert the object into a dict
remove_mount_request_dict = remove_mount_request_instance.to_dict()
# create an instance of RemoveMountRequest from a dict
remove_mount_request_from_dict = RemoveMountRequest.from_dict(remove_mount_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


