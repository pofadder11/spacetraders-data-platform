# CreateShipSystemScan201Response

Successfully scanned for nearby systems.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**CreateShipSystemScan201ResponseData**](CreateShipSystemScan201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.create_ship_system_scan201_response import CreateShipSystemScan201Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateShipSystemScan201Response from a JSON string
create_ship_system_scan201_response_instance = CreateShipSystemScan201Response.from_json(json)
# print the JSON string representation of the object
print(CreateShipSystemScan201Response.to_json())

# convert the object into a dict
create_ship_system_scan201_response_dict = create_ship_system_scan201_response_instance.to_dict()
# create an instance of CreateShipSystemScan201Response from a dict
create_ship_system_scan201_response_from_dict = CreateShipSystemScan201Response.from_dict(create_ship_system_scan201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


