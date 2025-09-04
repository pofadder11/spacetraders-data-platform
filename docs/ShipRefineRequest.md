# ShipRefineRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**produce** | **str** | The type of good to produce out of the refining process. | 

## Example

```python
from openapi_client.models.ship_refine_request import ShipRefineRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ShipRefineRequest from a JSON string
ship_refine_request_instance = ShipRefineRequest.from_json(json)
# print the JSON string representation of the object
print(ShipRefineRequest.to_json())

# convert the object into a dict
ship_refine_request_dict = ship_refine_request_instance.to_dict()
# create an instance of ShipRefineRequest from a dict
ship_refine_request_from_dict = ShipRefineRequest.from_dict(ship_refine_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


