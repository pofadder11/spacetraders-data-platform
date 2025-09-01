# ShipyardTransaction

Results of a transaction with a shipyard.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waypoint_symbol** | **str** | The symbol of the waypoint. | 
**ship_symbol** | **str** | The symbol of the ship type (e.g. SHIP_MINING_DRONE) that was the subject of the transaction. Contrary to what the name implies, this is NOT the symbol of the ship that was purchased. | 
**ship_type** | **str** | The symbol of the ship type (e.g. SHIP_MINING_DRONE) that was the subject of the transaction. | 
**price** | **int** | The price of the transaction. | 
**agent_symbol** | **str** | The symbol of the agent that made the transaction. | 
**timestamp** | **datetime** | The timestamp of the transaction. | 

## Example

```python
from openapi_client.models.shipyard_transaction import ShipyardTransaction

# TODO update the JSON string below
json = "{}"
# create an instance of ShipyardTransaction from a JSON string
shipyard_transaction_instance = ShipyardTransaction.from_json(json)
# print the JSON string representation of the object
print(ShipyardTransaction.to_json())

# convert the object into a dict
shipyard_transaction_dict = shipyard_transaction_instance.to_dict()
# create an instance of ShipyardTransaction from a dict
shipyard_transaction_from_dict = ShipyardTransaction.from_dict(shipyard_transaction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


