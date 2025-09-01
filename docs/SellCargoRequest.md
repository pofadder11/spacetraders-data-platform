# SellCargoRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**TradeSymbol**](TradeSymbol.md) |  | 
**units** | **int** | Amounts of units to sell of the selected good. | 

## Example

```python
from openapi_client.models.sell_cargo_request import SellCargoRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SellCargoRequest from a JSON string
sell_cargo_request_instance = SellCargoRequest.from_json(json)
# print the JSON string representation of the object
print(SellCargoRequest.to_json())

# convert the object into a dict
sell_cargo_request_dict = sell_cargo_request_instance.to_dict()
# create an instance of SellCargoRequest from a dict
sell_cargo_request_from_dict = SellCargoRequest.from_dict(sell_cargo_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


