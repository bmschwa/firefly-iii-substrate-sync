# some somequery tests

import requests

#curl -X POST -H 'Content-Type: application/json'  --data '{"jsonrpc":"2.0","method":"chain_getHeader","params": [],"id":1}' \
#  "https://polkadot.rpc.subquery.network/public"

SUBQUERY_URL = "https://polkadot.rpc.subquery.network/public"

headers = {'content-type': 'application/json'}

import json

# Example echo method
payload = {
    "method": "rpc_methods",
    "params": [],
    "jsonrpc": "2.0",
    "id": 0,
}
response = requests.post(
    SUBQUERY_URL, data=json.dumps(payload), headers=headers).json()


from xmlrpc.client import ServerProxy

s = ServerProxy(SUBQUERY_URL,
            headers=[
                ("Content-Type", "application/json")
            ],
            verbose=True)

r = s.chain_getHeader()

print(r)
#requests.post(SUBQUERY_URL,
#              data={
#                  88
#              })