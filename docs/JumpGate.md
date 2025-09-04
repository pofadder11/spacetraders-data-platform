# JumpGate

Details of a jump gate waypoint.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The symbol of the waypoint. | 
**connections** | **List[str]** | All the gates that are connected to this waypoint. | 

## Example

```python
from openapi_client.models.jump_gate import JumpGate

# TODO update the JSON string below
json = "{}"
# create an instance of JumpGate from a JSON string
jump_gate_instance = JumpGate.from_json(json)
# print the JSON string representation of the object
print(JumpGate.to_json())

# convert the object into a dict
jump_gate_dict = jump_gate_instance.to_dict()
# create an instance of JumpGate from a dict
jump_gate_from_dict = JumpGate.from_dict(jump_gate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


