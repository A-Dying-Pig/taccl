import os
import re
import json




with open('Alltoall.n24-MI300X-MI300X-steps5-tacclsol-improve-1736557915_taccl.sccl.json') as f:
    # Load the JSON data into a Python dictionary
    data = json.load(f)

input_map = data["input_map"]
output_map = data["output_map"]

# print(output_map)
nrank = 24
outputs = {}
inters = {}
for i in range(0, nrank):
    outputs[str(i)] = []
    inters[str(i)] = []

for id, cur_scheduler in enumerate(data["steps"]):
    print(f"step {id}")
    scheduler = cur_scheduler['sends']
    for transfer in scheduler:
        chunk, src, dst, t, _ = transfer
        if chunk in input_map[str(src)] :
            input_map[str(src)].remove(chunk)
        elif chunk in inters[str(src)]:
            inters[str(src)].remove(chunk)
        else:
            print(f"data chunk{chunk} not at src/inter rank{src}")
            print(transfer)

        inters[str(dst)].append(chunk)

for i in range(0, nrank):
    outputs[str(i)] = inters[str(i)]

for rank, data in outputs.items():
    outputs[rank] = sorted(data)

for rank, data in output_map.items():
    output_map[rank] = sorted(data)

for rank, data in output_map.items():
    if data != outputs[rank]:
        print(f"RANK: {rank}")
        print("target: ")
        print(data)
        print("actual recv:")
        print(outputs[rank])

# empty_str = ""
# for i in range(10, 24):
#     empty_str += f"[{i*25}, {i}, {i}, 0, 0], "
# print(empty_str)
