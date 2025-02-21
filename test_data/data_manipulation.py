import os
import json
import datetime

f = os.path.join(os.getcwd(), "subscan_examples", "extrinsics", "address_example_ex1.json")

with open(f, 'r') as p:
    d = json.load(p)

print(d)


for q in sorted(d.get('data', {}).get('extrinsics'), key=lambda k: k['block_timestamp']):
    dt = datetime.datetime.fromtimestamp(q['block_timestamp'], tz=datetime.UTC)
    print(f"{dt}: {q}")