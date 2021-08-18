# authenticate
# get payload
#   validate
#   add '_timeseries'
# Send it to the mmp

import json
import urllib.request

def authenticate():
    subdomain = input("Enter your subdomain: ")
    bearer_token = input("Enter your bearer token: ")
    
    try:
        request = urllib.request.Request("https://" + subdomain + ".tidalmg.com/api/v1/ping")
        request.add_header("Authorization", "bearer " + bearer_token)
        response = json.loads(urllib.request.urlopen(request).read())

        if(response['authenticated']):
            print("Authentication successful.")
            return True
    except:
        print("Authentication failed. Make sure you have the right subdomain and bearer token. Do not include `Bearer` at the beginning of the bearer token.")
        # raise
        return False

if(authenticate()):
    print("Authenticated")