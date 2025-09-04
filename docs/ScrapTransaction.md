# ScrapTransaction

Result of a scrap transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waypoint_symbol** | **str** | The symbol of the waypoint. | 
**ship_symbol** | **str** | The symbol of the ship. | 
**total_price** | **int** | The total price of the transaction. | 
**timestamp** | **datetime** | The timestamp of the transaction. | 

## Example

```python
from openapi_client.models.scrap_transaction import ScrapTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of ScrapTransaction from a JSON string
scrap_transaction_instance = ScrapTransaction.from_json(json)
# print the JSON string representation of the object
print(ScrapTransaction.to_json())

# convert the object into a dict
scrap_transaction_dict = scrap_transaction_instance.to_dict()
# create an instance of ScrapTransaction from a dict
scrap_transaction_from_dict = ScrapTransaction.from_dict(scrap_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


