# TransferCargoRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trade_symbol** | [**TradeSymbol**](TradeSymbol.md) |  | 
**units** | **int** | Amount of units to transfer. | 
**ship_symbol** | **str** | The symbol of the ship to transfer to. | 

## Example

```python
from openapi_client.models.transfer_cargo_request import TransferCargoRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TransferCargoRequest from a JSON string
transfer_cargo_request_instance = TransferCargoRequest.from_json(json)
# print the JSON string representation of the object
print(TransferCargoRequest.to_json())

# convert the object into a dict
transfer_cargo_request_dict = transfer_cargo_request_instance.to_dict()
# create an instance of TransferCargoRequest from a dict
transfer_cargo_request_from_dict = TransferCargoRequest.from_dict(transfer_cargo_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


