# ShipRefine201ResponseDataProducedInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trade_symbol** | [**TradeSymbol**](TradeSymbol.md) | Symbol of the good. | 
**units** | **int** | Amount of units of the good. | 

## Example

```python
from openapi_client.models.ship_refine201_response_data_produced_inner import ShipRefine201ResponseDataProducedInner

# TODO update the JSON string below
json = "{}"
# create an instance of ShipRefine201ResponseDataProducedInner from a JSON string
ship_refine201_response_data_produced_inner_instance = ShipRefine201ResponseDataProducedInner.from_json(json)
# print the JSON string representation of the object
print(ShipRefine201ResponseDataProducedInner.to_json())

# convert the object into a dict
ship_refine201_response_data_produced_inner_dict = ship_refine201_response_data_produced_inner_instance.to_dict()
# create an instance of ShipRefine201ResponseDataProducedInner from a dict
ship_refine201_response_data_produced_inner_from_dict = ShipRefine201ResponseDataProducedInner.from_dict(ship_refine201_response_data_produced_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


