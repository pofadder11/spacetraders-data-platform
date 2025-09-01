# CreateShipShipScan201Response

Successfully scanned for nearby ships.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**CreateShipShipScan201ResponseData**](CreateShipShipScan201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.create_ship_ship_scan201_response import CreateShipShipScan201Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateShipShipScan201Response from a JSON string
create_ship_ship_scan201_response_instance = CreateShipShipScan201Response.from_json(json)
# print the JSON string representation of the object
print(CreateShipShipScan201Response.to_json())

# convert the object into a dict
create_ship_ship_scan201_response_dict = create_ship_ship_scan201_response_instance.to_dict()
# create an instance of CreateShipShipScan201Response from a dict
create_ship_ship_scan201_response_from_dict = CreateShipShipScan201Response.from_dict(create_ship_ship_scan201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


