import requests
import json

url = "https://polkadot.api.subscan.io/api/scan/account/balance_history"

payload = json.dumps({
   "address": "19ZCyrUMaV1tSeC5GBp15UMVV8ZSQEhsS7snwL62YB3Stej",
   #"block_range": "string",
   #"end": "string",
   #"recent_block": 10000,
   #"start": "string"

    # extrinsincs:
    "row": 100
})
headers = {
   'Content-Type': 'application/json',
    'x-api-key': "eee937f9914f4cbe96465316adc7d706"
}

#response = requests.request("POST", url, headers=headers, data=payload)

#print(response.text)

response2 = requests.post("https://polkadot.api.subscan.io/api/v2/scan/extrinsics", headers=headers,
                          data=payload)

print(response2.json())