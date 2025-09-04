# ContractTerms

The terms to fulfill the contract.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**deadline** | **datetime** | The deadline for the contract. | 
**payment** | [**ContractPayment**](ContractPayment.md) |  | 
**deliver** | [**List[ContractDeliverGood]**](ContractDeliverGood.md) | The cargo that needs to be delivered to fulfill the contract. | [optional] 

## Example

```python
from openapi_client.models.contract_terms import ContractTerms

# TODO update the JSON string below
json = "{}"
# create an instance of ContractTerms from a JSON string
contract_terms_instance = ContractTerms.from_json(json)
# print the JSON string representation of the object
print(ContractTerms.to_json())

# convert the object into a dict
contract_terms_dict = contract_terms_instance.to_dict()
# create an instance of ContractTerms from a dict
contract_terms_from_dict = ContractTerms.from_dict(contract_terms_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


