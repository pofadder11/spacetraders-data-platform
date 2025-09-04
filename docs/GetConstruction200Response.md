# GetConstruction200Response

Successfully fetched construction site.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**Construction**](Construction.md) |  | 

## Example

```python
from openapi_client.models.get_construction200_response import GetConstruction200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetConstruction200Response from a JSON string
get_construction200_response_instance = GetConstruction200Response.from_json(json)
# print the JSON string representation of the object
print(GetConstruction200Response.to_json())

# convert the object into a dict
get_construction200_response_dict = get_construction200_response_instance.to_dict()
# create an instance of GetConstruction200Response from a dict
get_construction200_response_from_dict = GetConstruction200Response.from_dict(get_construction200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


