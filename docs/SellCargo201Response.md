# SellCargo201Response

Cargo was successfully sold.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**PurchaseCargo201ResponseData**](PurchaseCargo201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.sell_cargo201_response import SellCargo201Response

# TODO update the JSON string below
json = "{}"
# create an instance of SellCargo201Response from a JSON string
sell_cargo201_response_instance = SellCargo201Response.from_json(json)
# print the JSON string representation of the object
print(SellCargo201Response.to_json())

# convert the object into a dict
sell_cargo201_response_dict = sell_cargo201_response_instance.to_dict()
# create an instance of SellCargo201Response from a dict
sell_cargo201_response_from_dict = SellCargo201Response.from_dict(sell_cargo201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


