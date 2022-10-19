DELIM="|"
import requests
from auth import API_KEY_311
from datetime import datetime

BASE_URL='https://dc311-api.herokuapp.com/311/v4/request/'
URL_SUFFIX='?api_key=' + API_KEY_311

def get_sr_from_311(service_request_id):
    resp = requests.get(BASE_URL + service_request_id + '.json' + URL_SUFFIX)
    if resp.status_code == 404:
        return "Invalid Service Request ID"
    else:
        return resp.json()[0]

def get_sr_line_headers():
    return f"{DELIM}SR Status{DELIM}Latitude{DELIM}Longitude{DELIM}Service Name{DELIM}SR Last Update Date"

def not_an_sr_datapoints():
    return f"{DELIM}{DELIM}{DELIM}{DELIM}{DELIM}"


def get_sr_datapoints(service_request_id):
    sr_data=get_sr_from_311(service_request_id)
    if sr_data == "Invalid Service Request ID":
        return f"{DELIM}{sr_data}"
    else:
        status = sr_data["status"]
        lat = sr_data["lat"]
        long = sr_data["long"]
        service_name = sr_data["service_name"]
        last_update = sr_data["additional_details"]["last_updated_datetime"]
        last_update_formatted=datetime.strptime(last_update,'%Y-%m-%dT%H:%M:%S.000Z').strftime("%m/%d/%Y")
        sr_datapoints_line = f"{DELIM}{status}{DELIM}{lat}{DELIM}{long}{DELIM}{service_name}{DELIM}{last_update_formatted}"
        return sr_datapoints_line

#get_sr_from_311('22-00501533')