"""
This python file is used to send the CPU and memory utilization measurements to the Tidal Migrations API.

It uses subdomain and bearer token for authentication.
    - Subdomain is the name of your workspace.
    - Bearer token can be found at https://[subdomain].tidalmg.com/#/admin/settings >  Authentication Token

This script takes the JSON file that was created by the machine-stats and send the custom fields as the measurements.
Current time will be used as the timestamp by the Tidal MIgrations API.
"""

import json
import urllib.request

SUBDOMAIN = ""
BEARER_TOKEN = ""


def authenticate():
    print(">> Authentication")
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
        return False


def manipulate_json_payload(payload_json_data):
    for server in payload_json_data['servers']:
        server['custom_fields']['cpu_average_timeseries'] = server['custom_fields'].pop(
            'cpu_average')
        server['custom_fields']['cpu_peak_timeseries'] = server['custom_fields'].pop(
            'cpu_peak')

    print("   Processed JSON payload data.")
    return payload_json_data


def send_data_to_tidal_api(processed_json_payload):
    try:
        url = "https://" + SUBDOMAIN + ".tidalmg.com/api/v1/measurements"
        request = urllib.request.Request(url)

        request.add_header('Content-Type', 'application/json; charset=utf-8')
        request.add_header("Authorization", "bearer " + BEARER_TOKEN)

        payload_in_bytes = json.dumps(processed_json_payload).encode(
            'utf-8')
        request.add_header('Content-Length', len(payload_in_bytes))

        response = urllib.request.urlopen(request, payload_in_bytes)

        if(response.status):
            print("\n>> Data sent to the Tidal Migrations API!")
    except:
        print("Could not send the request to the Tidal Migrations API.")
        raise


if(authenticate()):
    print("\n>> Add JSON Payload")
    payload_file_name = input("   Enter the name of your JSON payload file: ")

    try:
        with open(payload_file_name) as json_file_wrapper:
            payload_json_data = json.load(json_file_wrapper)
            json_file_wrapper.close()
    except:
        print("Could not access the JSON payload file. Please include the relative path if the file is not in the same directory.\n")
        raise

    processed_json_payload = manipulate_json_payload(payload_json_data)

    send_data_to_tidal_api(processed_json_payload)
