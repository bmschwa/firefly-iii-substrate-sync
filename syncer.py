import os
import json
import random
from decimal import Decimal
import requests

from substrateinterface import SubstrateInterface



FIREFLY_III_API_URL = os.getenv("FIREFLY_III_API_URL")
FIREFLY_III_PAT = os.getenv("FIREFLY_III_PAT")  # Personal Access Token


response = requests.get("/".join([FIREFLY_III_API_URL, 'about']),
                        headers={
                            "Authorization": "Bearer %s"%FIREFLY_III_PAT,
                            "Accept": "application/json"})
print(response)


if not response.ok:
    print(f"Failed to access... {response.text}")
    exit(1)

print(f"Connected & About ({response.elapsed.total_seconds()}): {response.json()}")


with open("conf.json", 'r') as f:
    conf = json.load(f)


# Function to fetch transactions
def fetch_transactions(substrate, provider_address):
    # Get recent block hashes
    chain_head = substrate.get_block()
    block_number = chain_head['header']['number']

    transactions = []

    # Iterate through recent blocks (modify range for more history)
    for block_offset in range(10):  # Adjust for more historical data
        block_hash = substrate.get_block_hash(block_number - block_offset)
        block = substrate.get_block(block_hash=block_hash)

        for extrinsic in block['extrinsics']:
            # Check if it's a transfer call
            if extrinsic['call']['call_module'] == "Balances" and extrinsic['call']['call_function'] in ["transfer",
                                                                                                         "transfer_keep_alive"]:
                sender = extrinsic['signature']['signer']
                receiver = extrinsic['call']['call_args'][0]['value']

                if sender == provider_address or receiver == provider_address:
                    yield {
                        "block_number": block_number - block_offset,
                        "sender": sender,
                        "receiver": receiver,
                        "amount": extrinsic['call']['call_args'][1]['value'],
                        "hash": extrinsic['hash']
                    }



def update_substrate(sym, details):
    # Construct the API provider
    url = random.choice(details.get('public_urls', []))
    print(f"Using {url} for {sym}")
    ws_provider = SubstrateInterface(
         url=url
    )

    # List of available runtime constants in the metadata
    #constant_list = ws_provider.get_metadata_constants()
    #print(constant_list)


    for addr, addr_details in details.get("owned_addresses", {}).items():


        acct_number = addr_details.get("firefly_iii_acct", -1)
        # get details from firefly account:
        response = requests.get("/".join([FIREFLY_III_API_URL, 'accounts', str(acct_number)]),
                                headers={
                                    "Authorization": "Bearer %s" % FIREFLY_III_PAT,
                                    "Accept": "application/json"})
        if not response.ok:
            print(f"Failed getting {sym} / {addr} --> {acct_number}: {response.text}")
            continue

        print(f"Retrieved Account Info {sym} / {addr} --> {acct_number} in {response.elapsed.total_seconds()}")

        response = requests.get("/".join([FIREFLY_III_API_URL, 'accounts', str(acct_number), "transactions"]),
                                headers={
                                    "Authorization": "Bearer %s" % FIREFLY_III_PAT,
                                    "Accept": "application/json"})

        hash_at_head = ws_provider.get_chain_head()
        block_number = ws_provider.get_block_number(hash_at_head)

        result = ws_provider.query(
            "System", "Account", [addr], block_hash=hash_at_head
        )

        balance_int = (result.value["data"]["free"] + result.value["data"]["reserved"])
        balance_format = Decimal(format(balance_int / 10 ** ws_provider.properties.get('tokenDecimals', 0), ".15g"))

        print(f"At Blockheight {block_number}; {addr} has {balance_format}")

        for tx in fetch_transactions(ws_provider, addr):
            print(tx)

        print(response)


for symbol, substrate_params in conf.get("substrate", {}).items():
    update_substrate(symbol, substrate_params)

