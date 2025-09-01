# WaypointTrait


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | [**WaypointTraitSymbol**](WaypointTraitSymbol.md) |  | 
**name** | **str** | The name of the trait. | 
**description** | **str** | A description of the trait. | 

## Example

```python
from openapi_client.models.waypoint_trait import WaypointTrait

# TODO update the JSON string below
json = "{}"
# create an instance of WaypointTrait from a JSON string
waypoint_trait_instance = WaypointTrait.from_json(json)
# print the JSON string representation of the object
print(WaypointTrait.to_json())

# convert the object into a dict
waypoint_trait_dict = waypoint_trait_instance.to_dict()
# create an instance of WaypointTrait from a dict
waypoint_trait_from_dict = WaypointTrait.from_dict(waypoint_trait_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


