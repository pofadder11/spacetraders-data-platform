# GetMyAccount200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**GetMyAccount200ResponseData**](GetMyAccount200ResponseData.md) |  | 

## Example

```python
from openapi_client.models.get_my_account200_response import GetMyAccount200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetMyAccount200Response from a JSON string
get_my_account200_response_instance = GetMyAccount200Response.from_json(json)
# print the JSON string representation of the object
print(GetMyAccount200Response.to_json())

# convert the object into a dict
get_my_account200_response_dict = get_my_account200_response_instance.to_dict()
# create an instance of GetMyAccount200Response from a dict
get_my_account200_response_from_dict = GetMyAccount200Response.from_dict(get_my_account200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


