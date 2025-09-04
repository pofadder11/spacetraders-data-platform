# GetMyShips200Response

Successfully listed ships.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[Ship]**](Ship.md) |  | 
**meta** | [**Meta**](Meta.md) |  | 

## Example

```python
from openapi_client.models.get_my_ships200_response import GetMyShips200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetMyShips200Response from a JSON string
get_my_ships200_response_instance = GetMyShips200Response.from_json(json)
# print the JSON string representation of the object
print(GetMyShips200Response.to_json())

# convert the object into a dict
get_my_ships200_response_dict = get_my_ships200_response_instance.to_dict()
# create an instance of GetMyShips200Response from a dict
get_my_ships200_response_from_dict = GetMyShips200Response.from_dict(get_my_ships200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


