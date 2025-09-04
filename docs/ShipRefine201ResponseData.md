# ShipRefine201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 
**cooldown** | [**Cooldown**](Cooldown.md) |  | 
**produced** | [**List[ShipRefine201ResponseDataProducedInner]**](ShipRefine201ResponseDataProducedInner.md) | Goods that were produced by this refining process. | 
**consumed** | [**List[ShipRefine201ResponseDataProducedInner]**](ShipRefine201ResponseDataProducedInner.md) | Goods that were consumed during this refining process. | 

## Example

```python
from openapi_client.models.ship_refine201_response_data import ShipRefine201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of ShipRefine201ResponseData from a JSON string
ship_refine201_response_data_instance = ShipRefine201ResponseData.from_json(json)
# print the JSON string representation of the object
print(ShipRefine201ResponseData.to_json())

# convert the object into a dict
ship_refine201_response_data_dict = ship_refine201_response_data_instance.to_dict()
# create an instance of ShipRefine201ResponseData from a dict
ship_refine201_response_data_from_dict = ShipRefine201ResponseData.from_dict(ship_refine201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


