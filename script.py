"""Send measurements to the Tidal Migrations API.

This python script is used to send the CPU and memory utilization measurements to the Tidal Migrations API.

It uses your email, password and subdomain (your workspace name) for authentication.
You can either add these auth credentials in the configs file or in CLI when running the script.
You can change this method using `configs.is_using_configs` variable.

This script takes the JSON file that was created by the machine-stats and send 
   the fields mentioned in the `configs.fields_to_measure` and `configs.custom_fields_to_measure` as the measurements.

Tidal Migrations API will use the current time as the timestamp.
"""

import argparse
import configs
import json
import urllib.request


SUBDOMAIN = ""
BEARER_TOKEN = ""
ENVIRONMENT = "Production"


def authenticate():
    print(">> Authenticating...")

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
        if(ENVIRONMENT == "Development"):
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

        response = json.loads(urllib.request.urlopen(
            request, payload_in_bytes).read())

        if(response['access_token']):
            BEARER_TOKEN = response['access_token']
            print("   Authentication successful!")
            return True
    except:
        print("\nError: Authentication failed. \nMake sure you have the right subdomain, email and password. Check your configs file.\n")
        return False


def process_json_payload(payload_json_data):
    try:
        """Process JSON payload

        Go through each server in the JSON payload, and for the fields mentioned in the 
          `configs.fields_to_measure` or `configs.custom_fields_to_measure`, add its measurements to the
          processed data. (See file example_processed_payload.json for reference)
        """
        processed_json_payload = {'measurements': []}
        for server in payload_json_data['servers']:
            for field in server:
                # Add data from custom_fields_to_measure list to the processed_json_payload dictionary
                if field in configs.custom_fields_to_measure:
                    server_dict = {}
                    server_dict['measurable_type'] = 'server'
                    server_dict['field_name'] = field + \
                        '_timeseries'
                    server_dict['value'] = server[field]
                    server_dict['measurable'] = { 'host_name': server['host_name'] }

                    processed_json_payload['measurements'].append(
                        server_dict)

                # Add custom fields data from custom_fields_to_measure list to the processed_json_payload dictionary
                elif field == "custom_fields":
                    for custom_field in server['custom_fields']:
                        if custom_field in configs.custom_fields_to_measure:
                            server_dict = {}
                            server_dict['measurable_type'] = 'server'
                            server_dict['field_name'] = custom_field + \
                                '_timeseries'
                            server_dict['value'] = server['custom_fields'][custom_field]
                            server_dict['measurable'] = { 'host_name': server['host_name'] }

                            processed_json_payload['measurements'].append(
                                server_dict)
    except:
        print("\nError: Could not process the data. \nMake sure that all the servers have the necessary fields. You can customize them on the configs file.\n")
        raise

    print("   Process completed!")
    return processed_json_payload


def send_data_to_tidal_api(processed_json_payload):
    print("\n>> Sending data to the Tidal Migrations API!")
    try:
        if(ENVIRONMENT == "Development"):
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
            print("   Success!\n")
    except:
        print("\nError: Could not send the request to the Tidal Migrations API.\n")
        raise




def add_cli_args():
    parser = argparse.ArgumentParser(description='This script will facilitate sending your server measurements to the Tidal Migrations API.\n\n'
                                                    'To get you started, please adjust the config file located at the root of this folder.\n'
                                                    'You will need to add your Tidal Migrations credentials, such as subdomain, email and password\n'
                                                    'As well as, the file name containing your machine stats output.\n'
                                                    'Now that you are ready, run the script with this command.\n\n'
                                                    '`python3 script.py`\n', formatter_class=argparse.RawTextHelpFormatter)

    args = parser.parse_args()


add_cli_args()

if(authenticate()):
    print("\n>> Processing machine-stats output...")
    if(configs.is_using_configs):
        payload_file_name = configs.payload_json_file_name
    else:
        payload_file_name = input(
            "   Enter the name of your machine-stats output file: ")

    try:
        with open(payload_file_name) as json_file_wrapper:
            payload_json_data = json.load(json_file_wrapper)
            json_file_wrapper.close()
    except:
        print("\nError: Could not find the machine-stats output file. \nPlease double check the payload_json_file_name variable in your configs file . Make sure you include the relative path if the file is not in the same directory.\n")
        raise

    processed_json_payload = process_json_payload(payload_json_data)

    send_data_to_tidal_api(processed_json_payload)
