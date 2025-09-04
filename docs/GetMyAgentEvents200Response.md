# GetMyAgentEvents200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[AgentEvent]**](AgentEvent.md) |  | 

## Example

```python
from openapi_client.models.get_my_agent_events200_response import GetMyAgentEvents200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetMyAgentEvents200Response from a JSON string
get_my_agent_events200_response_instance = GetMyAgentEvents200Response.from_json(json)
# print the JSON string representation of the object
print(GetMyAgentEvents200Response.to_json())

# convert the object into a dict
get_my_agent_events200_response_dict = get_my_agent_events200_response_instance.to_dict()
# create an instance of GetMyAgentEvents200Response from a dict
get_my_agent_events200_response_from_dict = GetMyAgentEvents200Response.from_dict(get_my_agent_events200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


