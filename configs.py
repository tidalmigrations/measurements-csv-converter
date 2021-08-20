"""Authentication Credentials

Add subdomain and bearer token for authentication.
   - Subdomain is the name of your workspace.
   - Bearer token can be found at https://[subdomain].tidalmg.com/#/admin/settings >  Authentication Token
"""
tidal_subdomain = "dev"
tidal_email = "dev@tidalmigrations.com"
tidal_password = "dev123"

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

"""Use of environment

`environment` is used to change the API URLs 
   in local development and Production.
Anything but 'Development' will run the script as Production.
"""
environment = "Development"

"""Use of is_using_configs variable

is_using_configs variable is used to switch between location of credentials.
   - When True: environment variables TIDAL_SUBDOMAIN and TIDAL_BEARER_TOKEN is used for authentication.
   - When False: Manually enter the subdomain and bearer token when running the script.
"""
is_using_configs = True
