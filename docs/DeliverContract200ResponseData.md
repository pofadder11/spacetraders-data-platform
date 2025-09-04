# DeliverContract200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contract** | [**Contract**](Contract.md) |  | 
**cargo** | [**ShipCargo**](ShipCargo.md) |  | 

## Example

```python
from openapi_client.models.deliver_contract200_response_data import DeliverContract200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of DeliverContract200ResponseData from a JSON string
deliver_contract200_response_data_instance = DeliverContract200ResponseData.from_json(json)
# print the JSON string representation of the object
print(DeliverContract200ResponseData.to_json())

# convert the object into a dict
deliver_contract200_response_data_dict = deliver_contract200_response_data_instance.to_dict()
# create an instance of DeliverContract200ResponseData from a dict
deliver_contract200_response_data_from_dict = DeliverContract200ResponseData.from_dict(deliver_contract200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


