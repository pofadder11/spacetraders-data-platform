# PurchaseShip201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship** | [**Ship**](Ship.md) |  | 
**agent** | [**Agent**](Agent.md) |  | 
**transaction** | [**ShipyardTransaction**](ShipyardTransaction.md) |  | 

## Example

```python
from openapi_client.models.purchase_ship201_response_data import PurchaseShip201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseShip201ResponseData from a JSON string
purchase_ship201_response_data_instance = PurchaseShip201ResponseData.from_json(json)
# print the JSON string representation of the object
print(PurchaseShip201ResponseData.to_json())

# convert the object into a dict
purchase_ship201_response_data_dict = purchase_ship201_response_data_instance.to_dict()
# create an instance of PurchaseShip201ResponseData from a dict
purchase_ship201_response_data_from_dict = PurchaseShip201ResponseData.from_dict(purchase_ship201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


