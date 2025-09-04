# ContractPayment

Payments for the contract.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**on_accepted** | **int** | The amount of credits received up front for accepting the contract. | 
**on_fulfilled** | **int** | The amount of credits received when the contract is fulfilled. | 

## Example

```python
from openapi_client.models.contract_payment import ContractPayment

# TODO update the JSON string below
json = "{}"
# create an instance of ContractPayment from a JSON string
contract_payment_instance = ContractPayment.from_json(json)
# print the JSON string representation of the object
print(ContractPayment.to_json())

# convert the object into a dict
contract_payment_dict = contract_payment_instance.to_dict()
# create an instance of ContractPayment from a dict
contract_payment_from_dict = ContractPayment.from_dict(contract_payment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


