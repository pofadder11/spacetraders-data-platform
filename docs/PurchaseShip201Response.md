# PurchaseShip201Response

Purchased ship successfully.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**PurchaseShip201ResponseData**](PurchaseShip201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.purchase_ship201_response import PurchaseShip201Response

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseShip201Response from a JSON string
purchase_ship201_response_instance = PurchaseShip201Response.from_json(json)
# print the JSON string representation of the object
print(PurchaseShip201Response.to_json())

# convert the object into a dict
purchase_ship201_response_dict = purchase_ship201_response_instance.to_dict()
# create an instance of PurchaseShip201Response from a dict
purchase_ship201_response_from_dict = PurchaseShip201Response.from_dict(purchase_ship201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


