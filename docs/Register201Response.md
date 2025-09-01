# Register201Response

Successfully registered.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**Register201ResponseData**](Register201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.register201_response import Register201Response

# TODO update the JSON string below
json = "{}"
# create an instance of Register201Response from a JSON string
register201_response_instance = Register201Response.from_json(json)
# print the JSON string representation of the object
print(Register201Response.to_json())

# convert the object into a dict
register201_response_dict = register201_response_instance.to_dict()
# create an instance of Register201Response from a dict
register201_response_from_dict = Register201Response.from_dict(register201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


