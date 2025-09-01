# ShipCrew

The ship's crew service and maintain the ship's systems and equipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**current** | **int** | The current number of crew members on the ship. | 
**required** | **int** | The minimum number of crew members required to maintain the ship. | 
**capacity** | **int** | The maximum number of crew members the ship can support. | 
**rotation** | **str** | The rotation of crew shifts. A stricter shift improves the ship&#39;s performance. A more relaxed shift improves the crew&#39;s morale. | [default to 'STRICT']
**morale** | **int** | A rough measure of the crew&#39;s morale. A higher morale means the crew is happier and more productive. A lower morale means the ship is more prone to accidents. | 
**wages** | **int** | The amount of credits per crew member paid per hour. Wages are paid when a ship docks at a civilized waypoint. | 

## Example

```python
from openapi_client.models.ship_crew import ShipCrew

# TODO update the JSON string below
json = "{}"
# create an instance of ShipCrew from a JSON string
ship_crew_instance = ShipCrew.from_json(json)
# print the JSON string representation of the object
print(ShipCrew.to_json())

# convert the object into a dict
ship_crew_dict = ship_crew_instance.to_dict()
# create an instance of ShipCrew from a dict
ship_crew_from_dict = ShipCrew.from_dict(ship_crew_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


