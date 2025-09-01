from time import time

# use module PyJWT
import jwt
import requests

header = {
  "alg": "HS256",
  "typ": "JWT"
}

data = {
  "iss": "ppm-tech-user",
  "iat": int(round(time() * 1000))
}

secret = "*********"

token_ser = jwt.encode(data, secret, algorithm="HS256", headers=header)
print(token_ser)

api_to_call = 'https://bld11.smartkyc.com/smartkyc/t/BOS/api/LATEST/etc/flavor/settings'

payload = {}
headers = {
  'Authorization': token_ser
}

response = requests.request("GET", api_to_call, headers=headers, data=payload)

print(response.text)
