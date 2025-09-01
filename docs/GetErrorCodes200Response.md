# GetErrorCodes200Response

Fetched error codes successfully.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error_codes** | [**List[GetErrorCodes200ResponseErrorCodesInner]**](GetErrorCodes200ResponseErrorCodesInner.md) |  | 

## Example

```python
from openapi_client.models.get_error_codes200_response import GetErrorCodes200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetErrorCodes200Response from a JSON string
get_error_codes200_response_instance = GetErrorCodes200Response.from_json(json)
# print the JSON string representation of the object
print(GetErrorCodes200Response.to_json())

# convert the object into a dict
get_error_codes200_response_dict = get_error_codes200_response_instance.to_dict()
# create an instance of GetErrorCodes200Response from a dict
get_error_codes200_response_from_dict = GetErrorCodes200Response.from_dict(get_error_codes200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


