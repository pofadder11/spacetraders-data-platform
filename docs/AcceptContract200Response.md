# AcceptContract200Response

Successfully accepted contract.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**AcceptContract200ResponseData**](AcceptContract200ResponseData.md) |  | 

## Example

```python
from openapi_client.models.accept_contract200_response import AcceptContract200Response

# TODO update the JSON string below
json = "{}"
# create an instance of AcceptContract200Response from a JSON string
accept_contract200_response_instance = AcceptContract200Response.from_json(json)
# print the JSON string representation of the object
print(AcceptContract200Response.to_json())

# convert the object into a dict
accept_contract200_response_dict = accept_contract200_response_instance.to_dict()
# create an instance of AcceptContract200Response from a dict
accept_contract200_response_from_dict = AcceptContract200Response.from_dict(accept_contract200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


