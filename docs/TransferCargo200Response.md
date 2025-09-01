# TransferCargo200Response

Cargo transferred successfully.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**TransferCargo200ResponseData**](TransferCargo200ResponseData.md) |  | 

## Example

```python
from openapi_client.models.transfer_cargo200_response import TransferCargo200Response

# TODO update the JSON string below
json = "{}"
# create an instance of TransferCargo200Response from a JSON string
transfer_cargo200_response_instance = TransferCargo200Response.from_json(json)
# print the JSON string representation of the object
print(TransferCargo200Response.to_json())

# convert the object into a dict
transfer_cargo200_response_dict = transfer_cargo200_response_instance.to_dict()
# create an instance of TransferCargo200Response from a dict
transfer_cargo200_response_from_dict = TransferCargo200Response.from_dict(transfer_cargo200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


