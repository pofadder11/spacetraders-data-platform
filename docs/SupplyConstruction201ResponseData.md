# SupplyConstruction201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**construction** | [**Construction**](Construction.md) |  | 
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 

## Example

```python
from openapi_client.models.supply_construction201_response_data import SupplyConstruction201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of SupplyConstruction201ResponseData from a JSON string
supply_construction201_response_data_instance = SupplyConstruction201ResponseData.from_json(json)
# print the JSON string representation of the object
print(SupplyConstruction201ResponseData.to_json())

# convert the object into a dict
supply_construction201_response_data_dict = supply_construction201_response_data_instance.to_dict()
# create an instance of SupplyConstruction201ResponseData from a dict
supply_construction201_response_data_from_dict = SupplyConstruction201ResponseData.from_dict(supply_construction201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


