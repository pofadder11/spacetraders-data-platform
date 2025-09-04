# ExtractResources201Response

Successfully extracted resources.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**ExtractResources201ResponseData**](ExtractResources201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.extract_resources201_response import ExtractResources201Response

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractResources201Response from a JSON string
extract_resources201_response_instance = ExtractResources201Response.from_json(json)
# print the JSON string representation of the object
print(ExtractResources201Response.to_json())

# convert the object into a dict
extract_resources201_response_dict = extract_resources201_response_instance.to_dict()
# create an instance of ExtractResources201Response from a dict
extract_resources201_response_from_dict = ExtractResources201Response.from_dict(extract_resources201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


