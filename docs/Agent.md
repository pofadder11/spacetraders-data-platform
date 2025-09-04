# Agent

Agent details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_id** | **str** | Account ID that is tied to this agent. Only included on your own agent. | 
**symbol** | **str** | Symbol of the agent. | 
**headquarters** | **str** | The headquarters of the agent. | 
**credits** | **int** | The number of credits the agent has available. Credits can be negative if funds have been overdrawn. | 
**starting_faction** | **str** | The faction the agent started with. | 
**ship_count** | **int** | How many ships are owned by the agent. | 

## Example

```python
from openapi_client.models.agent import Agent

# TODO update the JSON string below
json = "{}"
# create an instance of Agent from a JSON string
agent_instance = Agent.from_json(json)
# print the JSON string representation of the object
print(Agent.to_json())

# convert the object into a dict
agent_dict = agent_instance.to_dict()
# create an instance of Agent from a dict
agent_from_dict = Agent.from_dict(agent_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


