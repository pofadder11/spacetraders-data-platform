# CreateShipShipScan201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cooldown** | [**Cooldown**](Cooldown.md) |  | 
**ships** | [**List[ScannedShip]**](ScannedShip.md) | List of scanned ships. | 

## Example

```python
from openapi_client.models.create_ship_ship_scan201_response_data import CreateShipShipScan201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of CreateShipShipScan201ResponseData from a JSON string
create_ship_ship_scan201_response_data_instance = CreateShipShipScan201ResponseData.from_json(json)
# print the JSON string representation of the object
print(CreateShipShipScan201ResponseData.to_json())

# convert the object into a dict
create_ship_ship_scan201_response_data_dict = create_ship_ship_scan201_response_data_instance.to_dict()
# create an instance of CreateShipShipScan201ResponseData from a dict
create_ship_ship_scan201_response_data_from_dict = CreateShipShipScan201ResponseData.from_dict(create_ship_ship_scan201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


