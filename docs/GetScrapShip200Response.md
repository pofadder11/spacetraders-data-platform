# GetScrapShip200Response

Successfully retrieved the amount of value that will be returned when scrapping a ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**GetScrapShip200ResponseData**](GetScrapShip200ResponseData.md) |  | 

## Example

```python
from openapi_client.models.get_scrap_ship200_response import GetScrapShip200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetScrapShip200Response from a JSON string
get_scrap_ship200_response_instance = GetScrapShip200Response.from_json(json)
# print the JSON string representation of the object
print(GetScrapShip200Response.to_json())

# convert the object into a dict
get_scrap_ship200_response_dict = get_scrap_ship200_response_instance.to_dict()
# create an instance of GetScrapShip200Response from a dict
get_scrap_ship200_response_from_dict = GetScrapShip200Response.from_dict(get_scrap_ship200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


