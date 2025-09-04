# InstallMountRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the mount to install. | 

## Example

```python
from openapi_client.models.install_mount_request import InstallMountRequest

# TODO update the JSON string below
json = "{}"
# create an instance of InstallMountRequest from a JSON string
install_mount_request_instance = InstallMountRequest.from_json(json)
# print the JSON string representation of the object
print(InstallMountRequest.to_json())

# convert the object into a dict
install_mount_request_dict = install_mount_request_instance.to_dict()
# create an instance of InstallMountRequest from a dict
install_mount_request_from_dict = InstallMountRequest.from_dict(install_mount_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


