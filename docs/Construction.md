# Construction

The construction details of a waypoint.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the waypoint. | 
**materials** | [**List[ConstructionMaterial]**](ConstructionMaterial.md) | The materials required to construct the waypoint. | 
**is_complete** | **bool** | Whether the waypoint has been constructed. | 

## Example

```python
from openapi_client.models.construction import Construction

# TODO update the JSON string below
json = "{}"
# create an instance of Construction from a JSON string
construction_instance = Construction.from_json(json)
# print the JSON string representation of the object
print(Construction.to_json())

# convert the object into a dict
construction_dict = construction_instance.to_dict()
# create an instance of Construction from a dict
construction_from_dict = Construction.from_dict(construction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


