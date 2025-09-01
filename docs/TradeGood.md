# TradeGood

A good that can be traded for other goods or currency.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**TradeSymbol**](TradeSymbol.md) |  | 
**name** | **str** | The name of the good. | 
**description** | **str** | The description of the good. | 

## Example

```python
from openapi_client.models.trade_good import TradeGood

# TODO update the JSON string below
json = "{}"
# create an instance of TradeGood from a JSON string
trade_good_instance = TradeGood.from_json(json)
# print the JSON string representation of the object
print(TradeGood.to_json())

# convert the object into a dict
trade_good_dict = trade_good_instance.to_dict()
# create an instance of TradeGood from a dict
trade_good_from_dict = TradeGood.from_dict(trade_good_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


