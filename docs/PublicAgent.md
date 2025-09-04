# PublicAgent

Public agent details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | Symbol of the agent. | 
**headquarters** | **str** | The headquarters of the agent. | 
**credits** | **int** | The number of credits the agent has available. Credits can be negative if funds have been overdrawn. | 
**starting_faction** | **str** | The faction the agent started with. | 
**ship_count** | **int** | How many ships are owned by the agent. | 

## Example

```python
from openapi_client.models.public_agent import PublicAgent

# TODO update the JSON string below
json = "{}"
# create an instance of PublicAgent from a JSON string
public_agent_instance = PublicAgent.from_json(json)
# print the JSON string representation of the object
print(PublicAgent.to_json())

# convert the object into a dict
public_agent_dict = public_agent_instance.to_dict()
# create an instance of PublicAgent from a dict
public_agent_from_dict = PublicAgent.from_dict(public_agent_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


