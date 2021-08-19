"""
This python file is used to send the CPU and memory utilization measurements to the Tidal Migrations API.

It uses subdomain and bearer token for authentication.
    - Subdomain is the name of your workspace.
    - Bearer token can be found at https://[subdomain].tidalmg.com/#/admin/settings >  Authentication Token

This script takes the JSON file that was created by the machine-stats and send the custom fields as the measurements.
You can mention the fields to measure in the global variables FIELDS_TO_MEASURE and CUSTOM_FIELDS_TO_MEASURE.
Tidal MIgrations API will use the current time as the timestamp.
"""

import json
import urllib.request


SUBDOMAIN = ""
BEARER_TOKEN = ""
FIELDS_TO_MEASURE = ["ram_used_gb"]
CUSTOM_FIELDS_TO_MEASURE = ['cpu_average', 'cpu_peak']

"""Use of ENVIRONMENT global variable

ENVIRONMENT global variable is used to change the API URLs 
   in local development and Production.
Anything but 'Development' will run the script as Production.
"""
ENVIRONMENT = "Development"


def authenticate():
    print(">> Authentication")
    SUBDOMAIN = input("   Enter your subdomain: ")
    BEARER_TOKEN = input("   Enter your bearer token: ")

    try:
        if(ENVIRONMENT == "Development"):
            url = "http://dev.localtest.me:3000/api/v1/ping"
        else:
            url ="https://" + SUBDOMAIN + ".tidalmg.com/api/v1/ping"

        request = urllib.request.Request()
        request.add_header("Authorization", "bearer " + BEARER_TOKEN)
        response = json.loads(urllib.request.urlopen(request).read())

        if(response['authenticated']):
            print("   Authentication successful.")
            return True
    except:
        print("\nError: Authentication failed. Make sure you have the right subdomain and bearer token. Do not include `Bearer` at the beginning of the bearer token.\n")
        return False


def process_json_payload(payload_json_data):
    try:
        """Process JSON payload

        Go through each server in the JSON payload, for the fields mentioned in the 
          FIELDS_TO_MEASURE or CUSTOM_FIELDS_TO_MEASURE, add its measurements to the
          processed data. (See file example_processed_payload.json)
        """
        processed_json_payload = {'measurements': []}
        for server in payload_json_data['servers']:
            for field in server:
                # Add data from FIELDS_TO_MEASURE list to the processed_json_payload dictionary
                if field in FIELDS_TO_MEASURE:
                    server_dict = {}
                    server_dict['name'] = server['host_name']
                    server_dict['measurable_type'] = 'server'
                    server_dict['field_name'] = field + \
                        '_timeseries'
                    server_dict['value'] = server[field]

                    processed_json_payload['measurements'].append(
                        server_dict)

                # Add custom fields data from CUSTOM_FIELDS_TO_MEASURE list to the processed_json_payload dictionary
                elif field == "custom_fields":
                    for custom_field in server['custom_fields']:
                        if custom_field in CUSTOM_FIELDS_TO_MEASURE:
                            server_dict = {}
                            server_dict['name'] = server['host_name']
                            server_dict['measurable_type'] = 'server'
                            server_dict['field_name'] = custom_field + \
                                '_timeseries'
                            server_dict['value'] = server['custom_fields'][custom_field]

                            processed_json_payload['measurements'].append(
                                server_dict)
    except:
        print("\nError: Could not process the data. Make sure that all the servers have custom fields mentioned in CUSTOM_FIELDS_TO_MEASURE list.\n")
        raise

    print("   Processed JSON payload data.")
    return processed_json_payload


def send_data_to_tidal_api(processed_json_payload):
    try:
        if(ENVIRONMENT == "Development"):
            url = "http://dev.localtest.me:3000/api/v1/measurements/import"
        else:
            url = "https://" + SUBDOMAIN + ".tidalmg.com/api/v1/measurements/import"
        
        request = urllib.request.Request(url)

        payload_in_bytes = json.dumps(processed_json_payload).encode(
            'utf-8')    # encode payload dictionary to bytes

        request.add_header('Content-Type', 'application/json; charset=utf-8')
        request.add_header("Authorization", "bearer " + BEARER_TOKEN)
        request.add_header('Content-Length', len(payload_in_bytes))

        response = urllib.request.urlopen(request, payload_in_bytes)

        if(response.status):
            print("\n>> Data sent to the Tidal Migrations API!\n")
    except:
        print("\nError: Could not send the request to the Tidal Migrations API.\n")
        raise


if(authenticate()):
    print("\n>> Add JSON Payload")
    payload_file_name = input("   Enter the name of your JSON payload file: ")

    try:
        with open(payload_file_name) as json_file_wrapper:
            payload_json_data = json.load(json_file_wrapper)
            json_file_wrapper.close()
    except:
        print("\nError: Could not access the JSON payload file. Please include the relative path if the file is not in the same directory.\n")
        raise

    processed_json_payload = process_json_payload(payload_json_data)

    send_data_to_tidal_api(processed_json_payload)
