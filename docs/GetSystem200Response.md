# GetSystem200Response

Successfully fetched the system.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**System**](System.md) |  | 

## Example

```python
from openapi_client.models.get_system200_response import GetSystem200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetSystem200Response from a JSON string
get_system200_response_instance = GetSystem200Response.from_json(json)
# print the JSON string representation of the object
print(GetSystem200Response.to_json())

# convert the object into a dict
get_system200_response_dict = get_system200_response_instance.to_dict()
# create an instance of GetSystem200Response from a dict
get_system200_response_from_dict = GetSystem200Response.from_dict(get_system200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


