import argparse
import sys
import numpy as np
parser = argparse.ArgumentParser(description='Parsing of Mauve')
parser.add_argument('-backbone', type=str, help='backbonefile', required=True)
parser.add_argument('-save_way', type=str, help='saveway', required=True)
args = parser.parse_args()

import pandas as pd

A = pd.read_csv(args.backbone, sep='\t')

A = np.array(A)

S=[]
for i in range(0, A.shape[1], 2):
    S.append(A[:,i:i+2].tolist())
S = np.array(S, dtype=np.float64)

S[S==0] = np.inf
S = S.tolist()

for org in S:
    for ind in range(len(org)):
        org[ind] += [ind]

for i in S:
    i.sort()

NS = np.array(S)
OrgMax = []
for org in NS:
    sliceS = org[:,:2]
    sliceS[sliceS == np.inf] = 0
    lens = sliceS[:, 1] - sliceS[:, 0]
    maxlen = int(np.abs(np.max(lens)))
    OrgMax.append(maxlen)
maxlen = max(OrgMax)

print('Max len {}'.format(maxlen))
#print(np.array(S))

node = []
edges = ''
current_org = 1
#print(np.array(S).shape)

for org in S:
    for n in range(len(org)-1):
        if org[n][0] == float('inf') or org[n+1][0] == float('inf'):
            continue
        startnode = int(org[n][2])
        endnode = int(org[n+1][2])
        len1 = int(abs(org[n][1] - org[n][0]))
        len2 = int(abs(org[n+1][1] - org[n+1][0]))
        print(org[n][0])
        #Lim from  0.75
        #len1 = len1/maxlen * 7.4 + 0.01
        #len2 = len2/maxlen * 7.4 + 0.01
        edges += 'sb{} sb{} g{} {} {} {} {} {}\n'.format(startnode, endnode, current_org, len1, len2, org[n][0], org[n][1], maxlen  )

    current_org += 1

savefile = open(args.save_way, 'w')
savefile.write(edges)

savefile.close()