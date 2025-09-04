# CreateChart201ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**chart** | [**Chart**](Chart.md) |  | 
**waypoint** | [**Waypoint**](Waypoint.md) |  | 
**transaction** | [**ChartTransaction**](ChartTransaction.md) |  | 
**agent** | [**Agent**](Agent.md) |  | 

## Example

```python
from openapi_client.models.create_chart201_response_data import CreateChart201ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of CreateChart201ResponseData from a JSON string
create_chart201_response_data_instance = CreateChart201ResponseData.from_json(json)
# print the JSON string representation of the object
print(CreateChart201ResponseData.to_json())

# convert the object into a dict
create_chart201_response_data_dict = create_chart201_response_data_instance.to_dict()
# create an instance of CreateChart201ResponseData from a dict
create_chart201_response_data_from_dict = CreateChart201ResponseData.from_dict(create_chart201_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


