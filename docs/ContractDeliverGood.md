# ContractDeliverGood

The details of a delivery contract. Includes the type of good, units needed, and the destination.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trade_symbol** | **str** | The symbol of the trade good to deliver. | 
**destination_symbol** | **str** | The destination where goods need to be delivered. | 
**units_required** | **int** | The number of units that need to be delivered on this contract. | 
**units_fulfilled** | **int** | The number of units fulfilled on this contract. | 

## Example

```python
from openapi_client.models.contract_deliver_good import ContractDeliverGood

# TODO update the JSON string below
json = "{}"
# create an instance of ContractDeliverGood from a JSON string
contract_deliver_good_instance = ContractDeliverGood.from_json(json)
# print the JSON string representation of the object
print(ContractDeliverGood.to_json())

# convert the object into a dict
contract_deliver_good_dict = contract_deliver_good_instance.to_dict()
# create an instance of ContractDeliverGood from a dict
contract_deliver_good_from_dict = ContractDeliverGood.from_dict(contract_deliver_good_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


