"""Authentication Credentials

Add subdomain and bearer token for authentication.
   - Subdomain is the name of your workspace.
   - Bearer token can be found at https://[subdomain].tidalmg.com/#/admin/settings >  Authentication Token
"""
tidal_subdomain = "trreb"
tidal_email = "dev@trreb.com"
tidal_password = "myPassword"


"""JSON Payload file name

Please include the relative path if the file is not in the same directory. `../dir/example_payload.json`
"""
payload_json_file_name = "example_payload.json"


"""How to measure fields

The fields that need to be tracked can be added in the fields_to_measure list.
If it's a custom field than please add it to the custom_fields_to_measure list.
"""
fields_to_measure = ["ram_used_gb"]
custom_fields_to_measure = ['cpu_average', 'cpu_peak']


"""Run the script locally

`environment` is used to change the API URLs 
   in the local development and Production.
Set it to `Development` to run the script locally.
"""
environment = "Development"


"""Use configs from this file in the script

`is_using_configs` variable is used to switch between location of credentials.
   - When True: Credentials and configs from this file will be used.
   - When False: Manually enter the credentials and configs in the CLI.
"""
is_using_configs = True
