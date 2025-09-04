# GetMyShip200Response

Successfully fetched ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**Ship**](Ship.md) |  | 

## Example

```python
from openapi_client.models.get_my_ship200_response import GetMyShip200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetMyShip200Response from a JSON string
get_my_ship200_response_instance = GetMyShip200Response.from_json(json)
# print the JSON string representation of the object
print(GetMyShip200Response.to_json())

# convert the object into a dict
get_my_ship200_response_dict = get_my_ship200_response_instance.to_dict()
# create an instance of GetMyShip200Response from a dict
get_my_ship200_response_from_dict = GetMyShip200Response.from_dict(get_my_ship200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


