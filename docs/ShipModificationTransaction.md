# ShipModificationTransaction

Result of a transaction for a ship modification, such as installing a mount or a module.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waypoint_symbol** | **str** | The symbol of the waypoint where the transaction took place. | 
**ship_symbol** | **str** | The symbol of the ship that made the transaction. | 
**trade_symbol** | **str** | The symbol of the trade good. | 
**total_price** | **int** | The total price of the transaction. | 
**timestamp** | **datetime** | The timestamp of the transaction. | 

## Example

```python
from openapi_client.models.ship_modification_transaction import ShipModificationTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of ShipModificationTransaction from a JSON string
ship_modification_transaction_instance = ShipModificationTransaction.from_json(json)
# print the JSON string representation of the object
print(ShipModificationTransaction.to_json())

# convert the object into a dict
ship_modification_transaction_dict = ship_modification_transaction_instance.to_dict()
# create an instance of ShipModificationTransaction from a dict
ship_modification_transaction_from_dict = ShipModificationTransaction.from_dict(ship_modification_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


