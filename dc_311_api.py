DELIM="|"
import requests
from auth import API_KEY_311

BASE_URL='https://dc311-api.herokuapp.com/311/v4/request/'
URL_SUFFIX='?api_key=' + API_KEY_311

def get_sr_from_311(service_request_id):
    resp = requests.get(BASE_URL + service_request_id + '.json' + URL_SUFFIX)
    return resp.json()[0]

def get_sr_datapoints(service_request_id):
    sr_data=get_sr_from_311(service_request_id)
    status = sr_data["status"]
    lat = sr_data["lat"]
    long = sr_data["long"]
    service_name = sr_data["service_name"]
    last_update = sr_data["additional_details"]["last_updated_datetime"]
    sr_datapoints_line = f"{DELIM}{status}{DELIM}{lat}{DELIM}{long}{DELIM}{service_name}{DELIM}{last_update}"
    return sr_datapoints_line

#get_sr_from_311('22-00499040')