# JumpShip200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**nav** | [**ShipNav**](ShipNav.md) |  | 
**cooldown** | [**Cooldown**](Cooldown.md) |  | 
**transaction** | [**MarketTransaction**](MarketTransaction.md) |  | 
**agent** | [**Agent**](Agent.md) |  | 

## Example

```python
from openapi_client.models.jump_ship200_response_data import JumpShip200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of JumpShip200ResponseData from a JSON string
jump_ship200_response_data_instance = JumpShip200ResponseData.from_json(json)
# print the JSON string representation of the object
print(JumpShip200ResponseData.to_json())

# convert the object into a dict
jump_ship200_response_data_dict = jump_ship200_response_data_instance.to_dict()
# create an instance of JumpShip200ResponseData from a dict
jump_ship200_response_data_from_dict = JumpShip200ResponseData.from_dict(jump_ship200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


