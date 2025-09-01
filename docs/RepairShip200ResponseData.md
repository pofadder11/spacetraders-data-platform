# RepairShip200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent** | [**Agent**](Agent.md) |  | 
**ship** | [**Ship**](Ship.md) |  | 
**transaction** | [**RepairTransaction**](RepairTransaction.md) |  | 

## Example

```python
from openapi_client.models.repair_ship200_response_data import RepairShip200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of RepairShip200ResponseData from a JSON string
repair_ship200_response_data_instance = RepairShip200ResponseData.from_json(json)
# print the JSON string representation of the object
print(RepairShip200ResponseData.to_json())

# convert the object into a dict
repair_ship200_response_data_dict = repair_ship200_response_data_instance.to_dict()
# create an instance of RepairShip200ResponseData from a dict
repair_ship200_response_data_from_dict = RepairShip200ResponseData.from_dict(repair_ship200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


