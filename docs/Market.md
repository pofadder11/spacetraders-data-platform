# Market

Market details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the market. The symbol is the same as the waypoint where the market is located. | 
**exports** | [**List[TradeGood]**](TradeGood.md) | The list of goods that are exported from this market. | 
**imports** | [**List[TradeGood]**](TradeGood.md) | The list of goods that are sought as imports in this market. | 
**exchange** | [**List[TradeGood]**](TradeGood.md) | The list of goods that are bought and sold between agents at this market. | 
**transactions** | [**List[MarketTransaction]**](MarketTransaction.md) | The list of recent transactions at this market. Visible only when a ship is present at the market. | [optional] 
**trade_goods** | [**List[MarketTradeGood]**](MarketTradeGood.md) | The list of goods that are traded at this market. Visible only when a ship is present at the market. | [optional] 

## Example

```python
from openapi_client.models.market import Market

# TODO update the JSON string below
json = "{}"
# create an instance of Market from a JSON string
market_instance = Market.from_json(json)
# print the JSON string representation of the object
print(Market.to_json())

# convert the object into a dict
market_dict = market_instance.to_dict()
# create an instance of Market from a dict
market_from_dict = Market.from_dict(market_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


