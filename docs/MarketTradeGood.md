# MarketTradeGood


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**TradeSymbol**](TradeSymbol.md) |  | 
**type** | **str** | The type of trade good (export, import, or exchange). | 
**trade_volume** | **int** | This is the maximum number of units that can be purchased or sold at this market in a single trade for this good. Trade volume also gives an indication of price volatility. A market with a low trade volume will have large price swings, while high trade volume will be more resilient to price changes. | 
**supply** | [**SupplyLevel**](SupplyLevel.md) |  | 
**activity** | [**ActivityLevel**](ActivityLevel.md) |  | [optional] 
**purchase_price** | **int** | The price at which this good can be purchased from the market. | 
**sell_price** | **int** | The price at which this good can be sold to the market. | 

## Example

```python
from openapi_client.models.market_trade_good import MarketTradeGood

# TODO update the JSON string below
json = "{}"
# create an instance of MarketTradeGood from a JSON string
market_trade_good_instance = MarketTradeGood.from_json(json)
# print the JSON string representation of the object
print(MarketTradeGood.to_json())

# convert the object into a dict
market_trade_good_dict = market_trade_good_instance.to_dict()
# create an instance of MarketTradeGood from a dict
market_trade_good_from_dict = MarketTradeGood.from_dict(market_trade_good_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


