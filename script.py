"""
This python file is used to send the CPU and memory utilization measurements to the Tidal Migrations API.

It uses subdomain and bearer token for authentication.
    - Subdomain is the name of your workspace.
    - Bearer token can be found at https://[subdomain].tidalmg.com/#/admin/settings >  Authentication Token

You can add these auth credentials in CLI when running the script or 
   add them into configs file: TIDAL_SUBDOMAIN, TIDAL_BEARER_TOKEN
  - You can change this method using configs.is_using_configs variable

This script takes the JSON file that was created by the machine-stats and send the custom fields as the measurements.
You can mention the fields to measure in the configs: custom_fields_to_measure and custom_fields_to_measure.
Tidal Migrations API will use the current time as the timestamp.
"""

import configs
import json
import os
import urllib.request


SUBDOMAIN = ""
BEARER_TOKEN = ""


def authenticate():
    print(">> Authentication")

    global SUBDOMAIN
    global BEARER_TOKEN

    if(configs.is_using_configs):
        SUBDOMAIN = configs.tidal_subdomain
        email = configs.tidal_email
        password = configs.tidal_password
    else:
        SUBDOMAIN = input("   Enter your subdomain: ")
        email = input("   Enter your email: ")
        password = input("   Enter your email: ")
        print("\n")

    try:
        if(configs.environment == "Development"):
            url = "http://" + SUBDOMAIN + ".localtest.me:3000/api/v1/authenticate"
        else:
            url = "https://" + SUBDOMAIN + ".tidalmg.com/api/v1/authenticate"

        request = urllib.request.Request(url)

        payload = {
            "username": email,
            "password": password
        }
        payload_in_bytes = json.dumps(payload).encode('utf-8')

        request.add_header('Content-Type', 'application/json; charset=utf-8')
        request.add_header('Content-Length', len(payload_in_bytes))

        response = json.loads(urllib.request.urlopen(request, payload_in_bytes).read())

        if(response['access_token']):
            BEARER_TOKEN = response['access_token']
            print("   Authentication successful.")
            return True
    except:
        print("\nError: Authentication failed. Make sure you have the right subdomain and bearer token. Do not include `Bearer` at the beginning of the bearer token.\n")
        return False


def process_json_payload(payload_json_data):
    try:
        """Process JSON payload

        Go through each server in the JSON payload, for the fields mentioned in the 
          custom_fields_to_measure or custom_fields_to_measure, add its measurements to the
          processed data. (See file example_processed_payload.json)
        """
        processed_json_payload = {'measurements': []}
        for server in payload_json_data['servers']:
            for field in server:
                # Add data from custom_fields_to_measure list to the processed_json_payload dictionary
                if field in configs.custom_fields_to_measure:
                    server_dict = {}
                    server_dict['name'] = server['host_name']
                    server_dict['measurable_type'] = 'server'
                    server_dict['field_name'] = field + \
                        '_timeseries'
                    server_dict['value'] = server[field]

                    processed_json_payload['measurements'].append(
                        server_dict)

                # Add custom fields data from custom_fields_to_measure list to the processed_json_payload dictionary
                elif field == "custom_fields":
                    for custom_field in server['custom_fields']:
                        if custom_field in configs.custom_fields_to_measure:
                            server_dict = {}
                            server_dict['name'] = server['host_name']
                            server_dict['measurable_type'] = 'server'
                            server_dict['field_name'] = custom_field + \
                                '_timeseries'
                            server_dict['value'] = server['custom_fields'][custom_field]

                            processed_json_payload['measurements'].append(
                                server_dict)
    except:
        print("\nError: Could not process the data. Make sure that all the servers have custom fields mentioned in custom_fields_to_measure list.\n")
        raise

    print("   Processed JSON payload data.")
    return processed_json_payload


def send_data_to_tidal_api(processed_json_payload):
    try:
        if(configs.environment == "Development"):
            url = "http://" + SUBDOMAIN + ".localtest.me:3000/api/v1/measurements/import"
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
    if(configs.is_using_configs):
        payload_file_name = configs.payload_json_file_name
    else:
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
