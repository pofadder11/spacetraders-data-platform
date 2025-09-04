# RefuelShipRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**units** | **int** | The amount of fuel to fill in the ship&#39;s tanks. When not specified, the ship will be refueled to its maximum fuel capacity. If the amount specified is greater than the ship&#39;s remaining capacity, the ship will only be refueled to its maximum fuel capacity. The amount specified is not in market units but in ship fuel units. | [optional] 
**from_cargo** | **bool** |  | [optional] 

## Example

```python
from openapi_client.models.refuel_ship_request import RefuelShipRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RefuelShipRequest from a JSON string
refuel_ship_request_instance = RefuelShipRequest.from_json(json)
# print the JSON string representation of the object
print(RefuelShipRequest.to_json())

# convert the object into a dict
refuel_ship_request_dict = refuel_ship_request_instance.to_dict()
# create an instance of RefuelShipRequest from a dict
refuel_ship_request_from_dict = RefuelShipRequest.from_dict(refuel_ship_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


