# RemoveShipModule201Response

Successfully removed the module from the ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**InstallShipModule201ResponseData**](InstallShipModule201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.remove_ship_module201_response import RemoveShipModule201Response

# TODO update the JSON string below
json = "{}"
# create an instance of RemoveShipModule201Response from a JSON string
remove_ship_module201_response_instance = RemoveShipModule201Response.from_json(json)
# print the JSON string representation of the object
print(RemoveShipModule201Response.to_json())

# convert the object into a dict
remove_ship_module201_response_dict = remove_ship_module201_response_instance.to_dict()
# create an instance of RemoveShipModule201Response from a dict
remove_ship_module201_response_from_dict = RemoveShipModule201Response.from_dict(remove_ship_module201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


