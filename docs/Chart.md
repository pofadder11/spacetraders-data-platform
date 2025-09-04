# Chart

The chart of a system or waypoint, which makes the location visible to other agents.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waypoint_symbol** | **str** | The symbol of the waypoint. | 
**submitted_by** | **str** | The agent that submitted the chart for this waypoint. | 
**submitted_on** | **datetime** | The time the chart for this waypoint was submitted. | 

## Example

```python
from openapi_client.models.chart import Chart

# TODO update the JSON string below
json = "{}"
# create an instance of Chart from a JSON string
chart_instance = Chart.from_json(json)
# print the JSON string representation of the object
print(Chart.to_json())

# convert the object into a dict
chart_dict = chart_instance.to_dict()
# create an instance of Chart from a dict
chart_from_dict = Chart.from_dict(chart_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


