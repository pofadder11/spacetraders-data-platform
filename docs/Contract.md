# Contract

Contract details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | ID of the contract. | 
**faction_symbol** | **str** | The symbol of the faction that this contract is for. | 
**type** | **str** | Type of contract. | 
**terms** | [**ContractTerms**](ContractTerms.md) |  | 
**accepted** | **bool** | Whether the contract has been accepted by the agent | [default to False]
**fulfilled** | **bool** | Whether the contract has been fulfilled | [default to False]
**expiration** | **datetime** | Deprecated in favor of deadlineToAccept | 
**deadline_to_accept** | **datetime** | The time at which the contract is no longer available to be accepted | [optional] 

## Example

```python
from openapi_client.models.contract import Contract

# TODO update the JSON string below
json = "{}"
# create an instance of Contract from a JSON string
contract_instance = Contract.from_json(json)
# print the JSON string representation of the object
print(Contract.to_json())

# convert the object into a dict
contract_dict = contract_instance.to_dict()
# create an instance of Contract from a dict
contract_from_dict = Contract.from_dict(contract_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


