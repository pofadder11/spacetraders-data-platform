# MarketTransaction

Result of a transaction with a market.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waypoint_symbol** | **str** | The symbol of the waypoint. | 
**ship_symbol** | **str** | The symbol of the ship that made the transaction. | 
**trade_symbol** | **str** | The symbol of the trade good. | 
**type** | **str** | The type of transaction. | 
**units** | **int** | The number of units of the transaction. | 
**price_per_unit** | **int** | The price per unit of the transaction. | 
**total_price** | **int** | The total price of the transaction. | 
**timestamp** | **datetime** | The timestamp of the transaction. | 

## Example

```python
from openapi_client.models.market_transaction import MarketTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of MarketTransaction from a JSON string
market_transaction_instance = MarketTransaction.from_json(json)
# print the JSON string representation of the object
print(MarketTransaction.to_json())

# convert the object into a dict
market_transaction_dict = market_transaction_instance.to_dict()
# create an instance of MarketTransaction from a dict
market_transaction_from_dict = MarketTransaction.from_dict(market_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


