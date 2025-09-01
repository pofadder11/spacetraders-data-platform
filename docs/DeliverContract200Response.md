# DeliverContract200Response

Successfully delivered cargo to contract.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**DeliverContract200ResponseData**](DeliverContract200ResponseData.md) |  | 

## Example

```python
from openapi_client.models.deliver_contract200_response import DeliverContract200Response

# TODO update the JSON string below
json = "{}"
# create an instance of DeliverContract200Response from a JSON string
deliver_contract200_response_instance = DeliverContract200Response.from_json(json)
# print the JSON string representation of the object
print(DeliverContract200Response.to_json())

# convert the object into a dict
deliver_contract200_response_dict = deliver_contract200_response_instance.to_dict()
# create an instance of DeliverContract200Response from a dict
deliver_contract200_response_from_dict = DeliverContract200Response.from_dict(deliver_contract200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


