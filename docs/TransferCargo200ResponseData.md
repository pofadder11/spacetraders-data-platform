# TransferCargo200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 
**target_cargo** | [**ShipCargo**](ShipCargo.md) |  | 

## Example

```python
from openapi_client.models.transfer_cargo200_response_data import TransferCargo200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of TransferCargo200ResponseData from a JSON string
transfer_cargo200_response_data_instance = TransferCargo200ResponseData.from_json(json)
# print the JSON string representation of the object
print(TransferCargo200ResponseData.to_json())

# convert the object into a dict
transfer_cargo200_response_data_dict = transfer_cargo200_response_data_instance.to_dict()
# create an instance of TransferCargo200ResponseData from a dict
transfer_cargo200_response_data_from_dict = TransferCargo200ResponseData.from_dict(transfer_cargo200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


