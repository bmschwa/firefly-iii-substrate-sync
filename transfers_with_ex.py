import requests
import json

url_base = "https://polkadot.api.subscan.io"

txfr_url = '/'.join([url_base, "api/v2/scan/transfers"])
address = "12poTLCFb5SAqDppMRjxZHMocCDTsADVPuy8fitaq9HtCk9L"

headers = {
   'Content-Type': 'application/json',
    'x-api-key': "c892353964294dfaa50aff310bbfcb16"
}


data = {
    "address": address,
    "row": 100
}

transfers = requests.post(txfr_url, headers=headers, json=data)

if not transfers.ok:
    raise Exception()


import datetime
from decimal import Decimal
transfersd = transfers.json()
txfr_cnt = transfersd['data']['count']
print(f"Retrieved {txfr_cnt} transfers in {datetime.timedelta(seconds=transfers.elapsed.total_seconds())}")
for txfr in sorted(transfersd.get('data', {}).get('transfers', []), key=lambda k: k['block_timestamp']):
    dt = datetime.datetime.fromtimestamp(txfr['block_timestamp'], tz=datetime.UTC)
    amt = Decimal(txfr['amount'])
    print(f"{dt}: block={txfr['block_num']} @ {amt}")


url = "api/scan/account/balance_history"

payload = json.dumps({
   "address": "19ZCyrUMaV1tSeC5GBp15UMVV8ZSQEhsS7snwL62YB3Stej",
   #"block_range": "string",
   #"end": "string",
   #"recent_block": 10000,
   #"start": "string"

    # extrinsincs:
    "row": 100
})

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

r2 = requests.post(url, headers=headers, data=payload)

print(r2)



txfr_r = requests.post(url2, headers=headers, data=payload)
print(txfr_r)


#response2 = requests.post("https://polkadot.api.subscan.io/api/v2/scan/extrinsics", headers=headers,
#                          data=payload)

#print(response2.json())