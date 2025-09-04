# ChartTransaction

Result of a chart transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waypoint_symbol** | **str** | The symbol of the waypoint. | 
**ship_symbol** | **str** | The symbol of the ship. | 
**total_price** | **int** | The total price of the transaction. | 
**timestamp** | **datetime** | The timestamp of the transaction. | 

## Example

```python
from openapi_client.models.chart_transaction import ChartTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of ChartTransaction from a JSON string
chart_transaction_instance = ChartTransaction.from_json(json)
# print the JSON string representation of the object
print(ChartTransaction.to_json())

# convert the object into a dict
chart_transaction_dict = chart_transaction_instance.to_dict()
# create an instance of ChartTransaction from a dict
chart_transaction_from_dict = ChartTransaction.from_dict(chart_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


