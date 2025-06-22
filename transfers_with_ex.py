import requests
import json

url_base = "https://polkadot.api.subscan.io"

txfr_url = '/'.join([url_base, "api/v2/scan/transfers"])
address = "12poTLCFb5SAqDppMRjxZHMocCDTsADVPuy8fitaq9HtCk9L"

headers = {
   'Content-Type': 'application/json',
    'x-api-key': "c892353964294dfaa50aff310bbfcb16"
}


request_data = {
    "address": address,
    "row": 100
}

transfers = requests.post(txfr_url, headers=headers, json=request_data)

if not transfers.ok:
    raise Exception()


import datetime
import pandas as pd
from decimal import Decimal

transfersd = transfers.json()
txfr_cnt = transfersd['data']['count']
print(f"Retrieved {txfr_cnt} transfers in {datetime.timedelta(seconds=transfers.elapsed.total_seconds())}")
data = []
for txfr in sorted(transfersd.get('data', {}).get('transfers', []), key=lambda k: k['block_timestamp']):
    dt = datetime.datetime.fromtimestamp(txfr['block_timestamp'], tz=datetime.UTC)
    amt = Decimal(txfr['amount'])
    print(f"{dt}: block={txfr['block_num']} @ {amt}")
    data.append({
        'source': 'transfers',
        'block_timestamp': dt,
        'block_num': txfr['block_num'],
        'amount': amt,
        'from': txfr['from'],
        'to': txfr['to'],
        'extrinsic_hash': txfr.get('extrinsic_hash'),
        'extrinsic_index': txfr.get('extrinsic_index'),
        'extrinsic_module': txfr.get('extrinsic_module'),
        'extrinsic_call': txfr.get('extrinsic_call'),
        'extrinsic_args': txfr.get('extrinsic_args'),
        'extrinsic_signature': txfr.get('extrinsic_signature'),
        'extrinsic_signature_type': txfr.get('extrinsic_signature_type'),
        'hash': txfr['hash'],
        'block_hash': txfr.get('block_hash'),
    })

df = pd.DataFrame(data)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

# https://support.subscan.io/api-6449744
url = "api/scan/account/balance_history"

request_data['block_range'] = f"{str(df['block_num'].min() - 1000)}-{df['block_num'].max()}" 
payload = json.dumps(request_data)

response = requests.request("POST", '/'.join([url_base, url]), headers=headers, data=payload)

print(response.text)

r2 = requests.post(url, headers=headers, data=payload)

print(r2)



txfr_r = requests.post(url2, headers=headers, data=payload)
print(txfr_r)


#response2 = requests.post("https://polkadot.api.subscan.io/api/v2/scan/extrinsics", headers=headers,
#                          data=payload)

#print(response2.json())