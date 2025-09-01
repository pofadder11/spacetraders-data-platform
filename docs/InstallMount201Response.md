# InstallMount201Response

Successfully installed the mount.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**InstallMount201ResponseData**](InstallMount201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.install_mount201_response import InstallMount201Response

# TODO update the JSON string below
json = "{}"
# create an instance of InstallMount201Response from a JSON string
install_mount201_response_instance = InstallMount201Response.from_json(json)
# print the JSON string representation of the object
print(InstallMount201Response.to_json())

# convert the object into a dict
install_mount201_response_dict = install_mount201_response_instance.to_dict()
# create an instance of InstallMount201Response from a dict
install_mount201_response_from_dict = InstallMount201Response.from_dict(install_mount201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


