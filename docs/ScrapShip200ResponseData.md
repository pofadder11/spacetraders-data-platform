# ScrapShip200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent** | [**Agent**](Agent.md) |  | 
**transaction** | [**ScrapTransaction**](ScrapTransaction.md) |  | 

## Example

```python
from openapi_client.models.scrap_ship200_response_data import ScrapShip200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of ScrapShip200ResponseData from a JSON string
scrap_ship200_response_data_instance = ScrapShip200ResponseData.from_json(json)
# print the JSON string representation of the object
print(ScrapShip200ResponseData.to_json())

# convert the object into a dict
scrap_ship200_response_data_dict = scrap_ship200_response_data_instance.to_dict()
# create an instance of ScrapShip200ResponseData from a dict
scrap_ship200_response_data_from_dict = ScrapShip200ResponseData.from_dict(scrap_ship200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


