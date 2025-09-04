# GetMyAccount200ResponseDataAccount


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**email** | **str** |  | 
**token** | **str** |  | [optional] 
**created_at** | **datetime** |  | 

## Example

```python
from openapi_client.models.get_my_account200_response_data_account import GetMyAccount200ResponseDataAccount

# TODO update the JSON string below
json = "{}"
# create an instance of GetMyAccount200ResponseDataAccount from a JSON string
get_my_account200_response_data_account_instance = GetMyAccount200ResponseDataAccount.from_json(json)
# print the JSON string representation of the object
print(GetMyAccount200ResponseDataAccount.to_json())

# convert the object into a dict
get_my_account200_response_data_account_dict = get_my_account200_response_data_account_instance.to_dict()
# create an instance of GetMyAccount200ResponseDataAccount from a dict
get_my_account200_response_data_account_from_dict = GetMyAccount200ResponseDataAccount.from_dict(get_my_account200_response_data_account_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


