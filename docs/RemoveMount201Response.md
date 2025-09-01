# RemoveMount201Response

Successfully removed the mount.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**RemoveMount201ResponseData**](RemoveMount201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.remove_mount201_response import RemoveMount201Response

# TODO update the JSON string below
json = "{}"
# create an instance of RemoveMount201Response from a JSON string
remove_mount201_response_instance = RemoveMount201Response.from_json(json)
# print the JSON string representation of the object
print(RemoveMount201Response.to_json())

# convert the object into a dict
remove_mount201_response_dict = remove_mount201_response_instance.to_dict()
# create an instance of RemoveMount201Response from a dict
remove_mount201_response_from_dict = RemoveMount201Response.from_dict(remove_mount201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


