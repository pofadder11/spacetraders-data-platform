# PurchaseCargo201Response

Purchased goods successfully.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**PurchaseCargo201ResponseData**](PurchaseCargo201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.purchase_cargo201_response import PurchaseCargo201Response

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseCargo201Response from a JSON string
purchase_cargo201_response_instance = PurchaseCargo201Response.from_json(json)
# print the JSON string representation of the object
print(PurchaseCargo201Response.to_json())

# convert the object into a dict
purchase_cargo201_response_dict = purchase_cargo201_response_instance.to_dict()
# create an instance of PurchaseCargo201Response from a dict
purchase_cargo201_response_from_dict = PurchaseCargo201Response.from_dict(purchase_cargo201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


