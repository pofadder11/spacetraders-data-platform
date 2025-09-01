# CreateChart201Response

Successfully charted waypoint.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**CreateChart201ResponseData**](CreateChart201ResponseData.md) |  | 

## Example

```python
from openapi_client.models.create_chart201_response import CreateChart201Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateChart201Response from a JSON string
create_chart201_response_instance = CreateChart201Response.from_json(json)
# print the JSON string representation of the object
print(CreateChart201Response.to_json())

# convert the object into a dict
create_chart201_response_dict = create_chart201_response_instance.to_dict()
# create an instance of CreateChart201Response from a dict
create_chart201_response_from_dict = CreateChart201Response.from_dict(create_chart201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


