# NegotiateContract201Response

Successfully negotiated a new contract.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**NegotiateContract201ResponseData**](NegotiateContract201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.negotiate_contract201_response import NegotiateContract201Response

# TODO update the JSON string below
json = "{}"
# create an instance of NegotiateContract201Response from a JSON string
negotiate_contract201_response_instance = NegotiateContract201Response.from_json(json)
# print the JSON string representation of the object
print(NegotiateContract201Response.to_json())

# convert the object into a dict
negotiate_contract201_response_dict = negotiate_contract201_response_instance.to_dict()
# create an instance of NegotiateContract201Response from a dict
negotiate_contract201_response_from_dict = NegotiateContract201Response.from_dict(negotiate_contract201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


