# PurchaseCargo201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 
**transaction** | [**MarketTransaction**](MarketTransaction.md) |  | 
**agent** | [**Agent**](Agent.md) |  | 

## Example

```python
from openapi_client.models.purchase_cargo201_response_data import PurchaseCargo201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseCargo201ResponseData from a JSON string
purchase_cargo201_response_data_instance = PurchaseCargo201ResponseData.from_json(json)
# print the JSON string representation of the object
print(PurchaseCargo201ResponseData.to_json())

# convert the object into a dict
purchase_cargo201_response_data_dict = purchase_cargo201_response_data_instance.to_dict()
# create an instance of PurchaseCargo201ResponseData from a dict
purchase_cargo201_response_data_from_dict = PurchaseCargo201ResponseData.from_dict(purchase_cargo201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


