# RefuelShip200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent** | [**Agent**](Agent.md) |  | 
**fuel** | [**ShipFuel**](ShipFuel.md) |  | 
**cargo** | [**ShipCargo**](ShipCargo.md) |  | [optional] 
**transaction** | [**MarketTransaction**](MarketTransaction.md) |  | 

## Example

```python
from openapi_client.models.refuel_ship200_response_data import RefuelShip200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of RefuelShip200ResponseData from a JSON string
refuel_ship200_response_data_instance = RefuelShip200ResponseData.from_json(json)
# print the JSON string representation of the object
print(RefuelShip200ResponseData.to_json())

# convert the object into a dict
refuel_ship200_response_data_dict = refuel_ship200_response_data_instance.to_dict()
# create an instance of RefuelShip200ResponseData from a dict
refuel_ship200_response_data_from_dict = RefuelShip200ResponseData.from_dict(refuel_ship200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


