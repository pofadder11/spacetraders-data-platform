# AcceptContract200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contract** | [**Contract**](Contract.md) |  | 
**agent** | [**Agent**](Agent.md) |  | 

## Example

```python
from openapi_client.models.accept_contract200_response_data import AcceptContract200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of AcceptContract200ResponseData from a JSON string
accept_contract200_response_data_instance = AcceptContract200ResponseData.from_json(json)
# print the JSON string representation of the object
print(AcceptContract200ResponseData.to_json())

# convert the object into a dict
accept_contract200_response_data_dict = accept_contract200_response_data_instance.to_dict()
# create an instance of AcceptContract200ResponseData from a dict
accept_contract200_response_data_from_dict = AcceptContract200ResponseData.from_dict(accept_contract200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


