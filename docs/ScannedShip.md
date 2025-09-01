# ScannedShip

The ship that was scanned. Details include information about the ship that could be detected by the scanner.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | The globally unique identifier of the ship. | 
**registration** | [**ShipRegistration**](ShipRegistration.md) |  | 
**nav** | [**ShipNav**](ShipNav.md) |  | 
**frame** | [**ScannedShipFrame**](ScannedShipFrame.md) |  | [optional] 
**reactor** | [**ScannedShipReactor**](ScannedShipReactor.md) |  | [optional] 
**engine** | [**ScannedShipEngine**](ScannedShipEngine.md) |  | 
**mounts** | [**List[ScannedShipMountsInner]**](ScannedShipMountsInner.md) | List of mounts installed in the ship. | [optional] 

## Example

```python
from openapi_client.models.scanned_ship import ScannedShip

# TODO update the JSON string below
json = "{}"
# create an instance of ScannedShip from a JSON string
scanned_ship_instance = ScannedShip.from_json(json)
# print the JSON string representation of the object
print(ScannedShip.to_json())

# convert the object into a dict
scanned_ship_dict = scanned_ship_instance.to_dict()
# create an instance of ScannedShip from a dict
scanned_ship_from_dict = ScannedShip.from_dict(scanned_ship_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


