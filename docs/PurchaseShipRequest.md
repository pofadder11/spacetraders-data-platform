# PurchaseShipRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_type** | [**ShipType**](ShipType.md) |  | 
**waypoint_symbol** | **str** | The symbol of the waypoint you want to purchase the ship at. | 

## Example

```python
from openapi_client.models.purchase_ship_request import PurchaseShipRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseShipRequest from a JSON string
purchase_ship_request_instance = PurchaseShipRequest.from_json(json)
# print the JSON string representation of the object
print(PurchaseShipRequest.to_json())

# convert the object into a dict
purchase_ship_request_dict = purchase_ship_request_instance.to_dict()
# create an instance of PurchaseShipRequest from a dict
purchase_ship_request_from_dict = PurchaseShipRequest.from_dict(purchase_ship_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


