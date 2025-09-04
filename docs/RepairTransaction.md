# RepairTransaction

Result of a repair transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waypoint_symbol** | **str** | The symbol of the waypoint. | 
**ship_symbol** | **str** | The symbol of the ship. | 
**total_price** | **int** | The total price of the transaction. | 
**timestamp** | **datetime** | The timestamp of the transaction. | 

## Example

```python
from openapi_client.models.repair_transaction import RepairTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of RepairTransaction from a JSON string
repair_transaction_instance = RepairTransaction.from_json(json)
# print the JSON string representation of the object
print(RepairTransaction.to_json())

# convert the object into a dict
repair_transaction_dict = repair_transaction_instance.to_dict()
# create an instance of RepairTransaction from a dict
repair_transaction_from_dict = RepairTransaction.from_dict(repair_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


