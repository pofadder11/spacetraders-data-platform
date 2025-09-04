# NavigateShip200Response

The successful transit information including the route details and changes to ship fuel. The route includes the expected time of arrival.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**NavigateShip200ResponseData**](NavigateShip200ResponseData.md) |  | 

## Example

```python
from openapi_client.models.navigate_ship200_response import NavigateShip200Response

# TODO update the JSON string below
json = "{}"
# create an instance of NavigateShip200Response from a JSON string
navigate_ship200_response_instance = NavigateShip200Response.from_json(json)
# print the JSON string representation of the object
print(NavigateShip200Response.to_json())

# convert the object into a dict
navigate_ship200_response_dict = navigate_ship200_response_instance.to_dict()
# create an instance of NavigateShip200Response from a dict
navigate_ship200_response_from_dict = NavigateShip200Response.from_dict(navigate_ship200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


