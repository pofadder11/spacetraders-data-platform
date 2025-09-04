# GetRepairShip200Response

Successfully retrieved the cost of repairing a ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**GetRepairShip200ResponseData**](GetRepairShip200ResponseData.md) |  | 

## Example

```python
from openapi_client.models.get_repair_ship200_response import GetRepairShip200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetRepairShip200Response from a JSON string
get_repair_ship200_response_instance = GetRepairShip200Response.from_json(json)
# print the JSON string representation of the object
print(GetRepairShip200Response.to_json())

# convert the object into a dict
get_repair_ship200_response_dict = get_repair_ship200_response_instance.to_dict()
# create an instance of GetRepairShip200Response from a dict
get_repair_ship200_response_from_dict = GetRepairShip200Response.from_dict(get_repair_ship200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


