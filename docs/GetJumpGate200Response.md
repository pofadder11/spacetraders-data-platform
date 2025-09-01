# GetJumpGate200Response

Jump gate details retrieved successfully.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JumpGate**](JumpGate.md) |  | 

## Example

```python
from openapi_client.models.get_jump_gate200_response import GetJumpGate200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetJumpGate200Response from a JSON string
get_jump_gate200_response_instance = GetJumpGate200Response.from_json(json)
# print the JSON string representation of the object
print(GetJumpGate200Response.to_json())

# convert the object into a dict
get_jump_gate200_response_dict = get_jump_gate200_response_instance.to_dict()
# create an instance of GetJumpGate200Response from a dict
get_jump_gate200_response_from_dict = GetJumpGate200Response.from_dict(get_jump_gate200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


