"""Authentication Credentials

Add subdomain and bearer token for authentication.
   - Subdomain is the name of your workspace.
   - Bearer token can be found at https://[subdomain].tidalmg.com/#/admin/settings >  Authentication Token
"""
tidal_subdomain = "dev"
tidal_bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJVRkNORVZDT1VRd1EwTXdNMFpDUlVKQk9UZEJSREl4TjBWRFFVSkJOVFl3UlRsQ1FqTkVRdyJ9.eyJpc3MiOiJodHRwczovL3RpZGFsLXRlc3QuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDU5NzYzNjEzMTNmNDBiMDg0ODVkMmIwMSIsImF1ZCI6InRpZGFsLXRlc3QtYXBpIiwiaWF0IjoxNjI5NDQ1MDY1LCJleHAiOjE2Mjk0NzM4NjUsImF6cCI6IlM5UndjU0tMNzB3d1JEdHVyVnIzdjNJWGc1V1RUdHR2Iiwic2NvcGUiOiJvZmZsaW5lX2FjY2VzcyIsImd0eSI6InBhc3N3b3JkIn0.NFzDXUPEbAirAZqLxCqo4sLtW-YGW-Yl8PF9diYohHB1j0mJUxVUZ_mTxyHzFRTPwGu_yJM9UFN5UaBDcPIBC_4271L4Qe-fUrNHl8Yy8SSfD2XDVUS1Q8Vu2U4UaU6Z_1T07Mw9u-cQVIUAf62qMLgsByKMTs28ZCYZSk0nTT7JVAAeInXeq8_F2n3rjRKJYYoZqjx9lVH_1w1BIUz-tZBkcd-Bgrw88Az7l0iN2FzoafssbTHFDIgkQtjUE0I3Z_wykacQV2ZmJKLC84FcyygmN-R_S3dxOs1VwmalbB0HyAw3jTqmJEPgutopr0NqVq6aInsSXVMLsgfyAah8vw"

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
