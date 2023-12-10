import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data = {'chat_history': [], 'question': 'how are you'}

body = str.encode(json.dumps(data))

url = 'https://machinelearningdemo-deploy2.canadacentral.inference.ml.azure.com/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
api_key = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjM1RjEzRUVDMzI2RjI1NkIxOTM5NUE3QTE3RjIyNjE4Qzk1MjVGRjIiLCJ0eXAiOiJKV1QifQ.eyJjYW5SZWZyZXNoIjoiRmFsc2UiLCJ3b3Jrc3BhY2VJZCI6ImRlM2I4Y2E5LWIzZjctNDlhOC04NGEyLWI1NTAwNzQ3M2YzNCIsInRpZCI6ImFkYWE0OThkLTQxZWEtNDQ2MC1hYjkwLTViY2I1N2ZmYjMzMSIsIm9pZCI6ImMzNWUzMzNiLWU5OGYtNGFmYy04MTA0LTg5YmQ3OTgzM2U5NSIsImFjdGlvbnMiOiJbXCJNaWNyb3NvZnQuTWFjaGluZUxlYXJuaW5nU2VydmljZXMvd29ya3NwYWNlcy9vbmxpbmVFbmRwb2ludHMvc2NvcmUvYWN0aW9uXCJdIiwiZW5kcG9pbnROYW1lIjoibWFjaGluZWxlYXJuaW5nZGVtby1kZXBsb3kyIiwic2VydmljZUlkIjoibWFjaGluZWxlYXJuaW5nZGVtby1kZXBsb3kyIiwiZXhwIjoxNzAyMDkyNzk2LCJpc3MiOiJhenVyZW1sIiwiYXVkIjoiYXp1cmVtbCJ9.Kf6BhKumNqQhnbIz1jVw1n80kh8gVTWVP49pGVFvUXlKC5WtpBI61xrVjkGmdNjWBX4TZuZ7tsjQCzTiH789esAvhfUrWcilVuACdQQvBwnyb8J9aKvBxQhtSNhe2qZgaLfTM_I51gZ1gbeChCgcYw0s7mz23xw7mQfZyY2ipd9GLrZhozT2jNBYhboqcdjmy4Hzz1PryAUvnzUKL9s0F8A0nBVFmn7LnzUgiPWXlL8NtglJpebH9et3El4aN7vzZG9iQCS3ORLGmvl-bI2W5e-E6BXkUGhJWmoJck4pRHrzvFunQWMsyAOVeGaU-aeYp-VS69RVUSSGG8lksyGNgQ'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'machinelearningdemo-deploy2-1' }

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))