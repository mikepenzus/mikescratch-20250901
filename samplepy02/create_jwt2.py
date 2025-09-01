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

#old secret
secret = "NcRfUjXn2r5u8x!A%D*G-KaPdSgVkYp3"
#new secret
#secret = "kG2M@]j*vdPrb4y=u)88fatQz/8'?'{R"

token_ser = jwt.encode(data, secret, algorithm="HS256", headers=header)
print(token_ser)

api_to_call = 'https://bld05.smartkyc.com/smartkyc/t/EBRD/api/LATEST/etc/flavor/settings'

payload = {}
headers = {
  'Authorization': token_ser
}

response = requests.request("GET", api_to_call, headers=headers, data=payload)
print(response.text)


api_to_call = 'https://bld05.smartkyc.com/smartkyc/t/EBRD/api/LATEST/state/reviews/1723208816223/summary'

response = requests.request("GET", api_to_call, headers=headers, data=payload)
print(response.text)
