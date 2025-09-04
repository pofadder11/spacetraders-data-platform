# ScannedSystem

Details of a system was that scanned.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**symbol** | **str** | Symbol of the system. | 
**sector_symbol** | **str** | Symbol of the system&#39;s sector. | 
**type** | [**SystemType**](SystemType.md) |  | 
**x** | **int** | Position in the universe in the x axis. | 
**y** | **int** | Position in the universe in the y axis. | 
**distance** | **int** | The system&#39;s distance from the scanning ship. | 

## Example

```python
from openapi_client.models.scanned_system import ScannedSystem

# TODO update the JSON string below
json = "{}"
# create an instance of ScannedSystem from a JSON string
scanned_system_instance = ScannedSystem.from_json(json)
# print the JSON string representation of the object
print(ScannedSystem.to_json())

# convert the object into a dict
scanned_system_dict = scanned_system_instance.to_dict()
# create an instance of ScannedSystem from a dict
scanned_system_from_dict = ScannedSystem.from_dict(scanned_system_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


