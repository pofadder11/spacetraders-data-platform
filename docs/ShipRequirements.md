# ShipRequirements

The requirements for installation on a ship

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**power** | **int** | The amount of power required from the reactor. | [optional] 
**crew** | **int** | The number of crew required for operation. | [optional] 
**slots** | **int** | The number of module slots required for installation. | [optional] 

## Example

```python
from openapi_client.models.ship_requirements import ShipRequirements

# TODO update the JSON string below
json = "{}"
# create an instance of ShipRequirements from a JSON string
ship_requirements_instance = ShipRequirements.from_json(json)
# print the JSON string representation of the object
print(ShipRequirements.to_json())

# convert the object into a dict
ship_requirements_dict = ship_requirements_instance.to_dict()
# create an instance of ShipRequirements from a dict
ship_requirements_from_dict = ShipRequirements.from_dict(ship_requirements_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


