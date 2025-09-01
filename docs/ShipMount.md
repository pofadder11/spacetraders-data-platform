# ShipMount

A mount is installed on the exterier of a ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | Symbol of this mount. | 
**name** | **str** | Name of this mount. | 
**description** | **str** | Description of this mount. | 
**strength** | **int** | Mounts that have this value, such as mining lasers, denote how powerful this mount&#39;s capabilities are. | [optional] 
**deposits** | **List[str]** | Mounts that have this value denote what goods can be produced from using the mount. | [optional] 
**requirements** | [**ShipRequirements**](ShipRequirements.md) |  | 

## Example

```python
from openapi_client.models.ship_mount import ShipMount

# TODO update the JSON string below
json = "{}"
# create an instance of ShipMount from a JSON string
ship_mount_instance = ShipMount.from_json(json)
# print the JSON string representation of the object
print(ShipMount.to_json())

# convert the object into a dict
ship_mount_dict = ship_mount_instance.to_dict()
# create an instance of ShipMount from a dict
ship_mount_from_dict = ShipMount.from_dict(ship_mount_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


