# authenticate
# get payload
#   validate
#   add '_timeseries'
# Send it to the mmp

import json
import urllib.request

SUBDOMAIN = ""
BEARER_TOKEN = ""


def authenticate():
    print(">> Authentication:")
    SUBDOMAIN = input("   Enter your subdomain: ")
    BEARER_TOKEN = input("   Enter your bearer token: ")

    try:
        request = urllib.request.Request(
            "https://" + SUBDOMAIN + ".tidalmg.com/api/v1/ping")
        request.add_header("Authorization", "bearer " + BEARER_TOKEN)
        response = json.loads(urllib.request.urlopen(request).read())

        if(response['authenticated']):
            print("   Authentication successful.")
            return True
    except:
        print("\nAuthentication failed. Make sure you have the right subdomain and bearer token. Do not include `Bearer` at the beginning of the bearer token.")
        # raise
        return False


def validate_json_payload():
    return True


def manipulate_json_payload(payload_json_data):
    for server in payload_json_data['servers']:
        server['custom_fields']['cpu_average_timeseries'] = server['custom_fields'].pop(
            'cpu_average')
        server['custom_fields']['cpu_peak_timeseries'] = server['custom_fields'].pop(
            'cpu_peak')

    return payload_json_data


if(authenticate()):
# if(True):
    print("\n>> Add JSON Payload:")
    # payload_file_name = input("   Enter the name of your JSON payload file: ")
    payload_file_name = "./payload.json"

    try:
        with open(payload_file_name) as json_file_wrapper:
            payload_json_data = json.load(json_file_wrapper)
            json_file_wrapper.close()
    except:
        print("Could not access the JSON payload file. Please include the relative path if the file is not in the same directory.\n")
        raise

    processed_json_payload = manipulate_json_payload(payload_json_data)

    # TODO JSON schema validation

    # if(validate_json_payload()):
    #     print("   JSON schema validated.")
