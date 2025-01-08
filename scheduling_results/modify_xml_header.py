import os
import re

def modify_header_only(input_folder, output_folder, fname):
    print(fname)
    with open(os.path.join(input_folder, fname), 'r') as f:
        lines = f.readlines()
    res = []
    for l in lines:
        indent = len(l) - len(l.lstrip())
        l = l.strip()
        if l.startswith('<copy'):
            continue
        elif l.startswith('<algo'):
            pattern = r'<algo name="(\w+)" nchannels="(\d+)" nchunksperloop="(\d+)" proto="(\w+)" coll="(\w+)" inplace="(\d+)" redop="(\w+)" ngpus="(\d+)">'
            match = re.search(pattern, l)
            assert match
            algo_name, nchannels, nchunksperloop, proto, coll, inplace, redop, ngpus = match.groups()
            algo_name, nchannels, nchunksperloop, proto, coll, inplace, redop, ngpus = algo_name, int(nchannels), int(nchunksperloop), proto, coll, int(inplace), redop, int(ngpus)
            assert inplace == 0 or inplace == 1
            l = f'<algo name="{algo_name}" proto="{proto}" nchunksperloop="{nchunksperloop}" ngpus="{ngpus}" coll="{coll}" inplace="{inplace}" outofplace="{1 - inplace}" minBytes="0" maxBytes="1099511627776" nchannels="{nchannels}">'

        res.append(' ' * indent + l)
    with open(os.path.join(output_folder, "original-" + fname), 'w') as f:
        f.write('\n'.join(res))


modify_header_only("./", "./r", "Alltoall.n16-MI300X-MI300X-steps2-tacclsol-improve-1736366150_i1_scRemote1_IBContig.sccl.xml")