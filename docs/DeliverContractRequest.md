# DeliverContractRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_symbol** | **str** | Symbol of a ship located in the destination to deliver a contract and that has a good to deliver in its cargo. | 
**trade_symbol** | **str** | The symbol of the good to deliver. | 
**units** | **int** | Amount of units to deliver. | 

## Example

```python
from openapi_client.models.deliver_contract_request import DeliverContractRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DeliverContractRequest from a JSON string
deliver_contract_request_instance = DeliverContractRequest.from_json(json)
# print the JSON string representation of the object
print(DeliverContractRequest.to_json())

# convert the object into a dict
deliver_contract_request_dict = deliver_contract_request_instance.to_dict()
# create an instance of DeliverContractRequest from a dict
deliver_contract_request_from_dict = DeliverContractRequest.from_dict(deliver_contract_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


