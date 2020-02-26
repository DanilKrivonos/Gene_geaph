import numpy as np
import pandas as pd
import argparse
import cairo
import math
from pyglet import app, clock, gl, image, window
import sys
parser = argparse.ArgumentParser(description='Making backbone file')
parser.add_argument('-Sibloose', type=str, help='Sibmatrix_loose', required=True)
parser.add_argument('-Sibfine', type=str, help='Sibmatrix_fine', required=True)
parser.add_argument('-Mauve', type=str, help='Mauvematrix', required=True)
parser.add_argument('-Sibuserset', type=str, help='Sibmatrix_uset', required=True)
parser.add_argument('-ref', type=str, default='g1')
parser.add_argument('-png_save_way', type=str, default=None, help='output image file')
parser.add_argument('-svg_save_way', type=str, default=None, help='output image file')
args = parser.parse_args()

A = np.loadtxt(args.Sibfine, dtype=np.str)
B = np.loadtxt(args.Sibloose, dtype=np.str)
C = np.loadtxt(args.Mauve, dtype=np.str)
D = np.loadtxt(args.Sibuserset, dtype=np.str)

pdEdges = pd.read_csv(args.Sibloose, header=None, names=['source', 'target', 'genome', 'len1', 'len2', 'coordinate1', 'coordinate2', 'maxlen'], sep=' ')

Sibloosegraph = {}
Edges = {}
ref_nodes = set()
ref_edges = set()
max_len = 0 
for i in range(len(pdEdges)):
    if pdEdges['source'][i] not in Sibloosegraph:
        Sibloosegraph[pdEdges['source'][i]] = {
            'length': int(pdEdges['len1'][i])/int(pdEdges['maxlen'][i])*7.4 + 0.01,
            'adj': [],
            'coordinates': (int(pdEdges['coordinate1'][i]),  int(pdEdges['coordinate2'][i]))
        }
    max_len = int(pdEdges['maxlen'][i])
    if pdEdges['target'][i] not in Sibloosegraph:
        Sibloosegraph[pdEdges['target'][i]] = {
            'length': int(pdEdges['len2'][i])/int(pdEdges['maxlen'][i])*7.4 + 0.01,
            'adj': [],
            'coordinates' :  (int(pdEdges['coordinate1'][i]),  int(pdEdges['coordinate2'][i]))
        }

    if pdEdges['genome'][i] == args.ref:
        ref_nodes.add(pdEdges['source'][i])
        ref_nodes.add(pdEdges['target'][i])
        ref_edges.add((pdEdges['source'][i], pdEdges['target'][i]))
    
    if (pdEdges['source'][i], pdEdges['target'][i]) not in Edges:
        Edges[(pdEdges['source'][i], pdEdges['target'][i])] = 0
    
    Edges[(pdEdges['source'][i], pdEdges['target'][i])] += 1
 
for edge in Edges:
    Sibloosegraph[edge[0]]['adj'].append((edge[1], Edges[edge]))

pdEdges = pd.read_csv(args.Sibfine, header=None, names=['source', 'target', 'genome', 'len1', 'len2', 'coordinate1', 'coordinate2', 'maxlen'], sep=' ')

Sibfinegraph = {}
Edges = {}
ref_nodes = set()
ref_edges = set()
max_len = 0 
for i in range(len(pdEdges)):
    if pdEdges['source'][i] not in Sibfinegraph:
        Sibfinegraph[pdEdges['source'][i]] = {
            'length': int(pdEdges['len1'][i])/int(pdEdges['maxlen'][i])*7.4 + 0.01,
            'adj': [],
            'coordinates': (int(pdEdges['coordinate1'][i]),  int(pdEdges['coordinate2'][i]))
        }
    max_len = int(pdEdges['maxlen'][i])
    if pdEdges['target'][i] not in Sibfinegraph:
        Sibfinegraph[pdEdges['target'][i]] = {
            'length': int(pdEdges['len2'][i])/int(pdEdges['maxlen'][i])*7.4 + 0.01,
            'adj': [],
            'coordinates' :  (int(pdEdges['coordinate1'][i]),  int(pdEdges['coordinate2'][i]))
        }

    if pdEdges['genome'][i] == args.ref:
        ref_nodes.add(pdEdges['source'][i])
        ref_nodes.add(pdEdges['target'][i])
        ref_edges.add((pdEdges['source'][i], pdEdges['target'][i]))
    
    if (pdEdges['source'][i], pdEdges['target'][i]) not in Edges:
        Edges[(pdEdges['source'][i], pdEdges['target'][i])] = 0
    
    Edges[(pdEdges['source'][i], pdEdges['target'][i])] += 1
 
for edge in Edges:
    Sibfinegraph[edge[0]]['adj'].append((edge[1], Edges[edge]))

pdEdges = pd.read_csv(args.Mauve, header=None, names=['source', 'target', 'genome', 'len1', 'len2', 'coordinate1', 'coordinate2', 'maxlen'], sep=' ')

Mauvegraph = {}
Edges = {}
ref_nodes = set()
ref_edges = set()
max_len = 0 
for i in range(len(pdEdges)):
    if pdEdges['source'][i] not in Mauvegraph:
        Mauvegraph[pdEdges['source'][i]] = {
            'length': int(pdEdges['len1'][i])/int(pdEdges['maxlen'][i])*7.4 + 0.01,
            'adj': [],
            'coordinates': (int(pdEdges['coordinate1'][i]),  int(pdEdges['coordinate2'][i]))
        }
    max_len = int(pdEdges['maxlen'][i])
    if pdEdges['target'][i] not in Mauvegraph:
        Mauvegraph[pdEdges['target'][i]] = {
            'length': int(pdEdges['len2'][i])/int(pdEdges['maxlen'][i])*7.4 + 0.01,
            'adj': [],
            'coordinates' :  (int(pdEdges['coordinate1'][i]),  int(pdEdges['coordinate2'][i]))
        }

    if pdEdges['genome'][i] == args.ref:
        ref_nodes.add(pdEdges['source'][i])
        ref_nodes.add(pdEdges['target'][i])
        ref_edges.add((pdEdges['source'][i], pdEdges['target'][i]))
    
    if (pdEdges['source'][i], pdEdges['target'][i]) not in Edges:
        Edges[(pdEdges['source'][i], pdEdges['target'][i])] = 0
    
    Edges[(pdEdges['source'][i], pdEdges['target'][i])] += 1
 
for edge in Edges:
    Mauvegraph[edge[0]]['adj'].append((edge[1], Edges[edge]))

pdEdges = pd.read_csv(args.Sibuserset, header=None, names=['source', 'target', 'genome', 'len1', 'len2', 'coordinate1', 'coordinate2', 'maxlen'], sep=' ')

Sibusersetgraph = {}
Edges = {}
ref_nodes = set()
ref_edges = set()
max_len = 0 
for i in range(len(pdEdges)):
    if pdEdges['source'][i] not in Sibusersetgraph:
        Sibusersetgraph[pdEdges['source'][i]] = {
            'length': int(pdEdges['len1'][i])/int(pdEdges['maxlen'][i])*7.4 + 0.01,
            'adj': [],
            'coordinates': (int(pdEdges['coordinate1'][i]),  int(pdEdges['coordinate2'][i]))
        }
    max_len = int(pdEdges['maxlen'][i])
    if pdEdges['target'][i] not in Sibusersetgraph:
        Sibusersetgraph[pdEdges['target'][i]] = {
            'length': int(pdEdges['len2'][i])/int(pdEdges['maxlen'][i])*7.4 + 0.01,
            'adj': [],
            'coordinates' :  (int(pdEdges['coordinate1'][i]),  int(pdEdges['coordinate2'][i]))
        }

    if pdEdges['genome'][i] == args.ref:
        ref_nodes.add(pdEdges['source'][i])
        ref_nodes.add(pdEdges['target'][i])
        ref_edges.add((pdEdges['source'][i], pdEdges['target'][i]))
    
    if (pdEdges['source'][i], pdEdges['target'][i]) not in Edges:
        Edges[(pdEdges['source'][i], pdEdges['target'][i])] = 0
    
    Edges[(pdEdges['source'][i], pdEdges['target'][i])] += 1
 
for edge in Edges:
    Sibusersetgraph[edge[0]]['adj'].append((edge[1], Edges[edge]))

ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, 3600, 1000)
cr = cairo.Context(ims)

palette = [
    (255, 0, 0),
    (0, 0, 139),
    (0, 255, 0)
]

i = 0
for node in Sibloosegraph:
    left = Sibloosegraph[node]['coordinates'][0]/1000
    right = Sibloosegraph[node]['coordinates'][1]/1000
    cr.rectangle(left, 300, right-left, 80)
    cr.set_source_rgb(*palette[i])
    cr.fill()
    i += 1

    if i >= 3:
        i = 0
i = 0
cr.select_font_face("white", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
for node in Sibfinegraph:
    left = Sibfinegraph[node]['coordinates'][0]/1000
    right = Sibfinegraph[node]['coordinates'][1]/1000
    cr.rectangle(left, 100, right-left, 80)
    cr.set_source_rgb(*palette[i])
    cr.fill()
    i += 1

    if i >= 3:
        i = 0

i = 0
for node in Mauvegraph:
    left = Mauvegraph[node]['coordinates'][0]/1000
    right = Mauvegraph[node]['coordinates'][1]/1000
    cr.rectangle(left, 500, right-left, 80)
    cr.set_source_rgb(*palette[i])
    cr.fill()
    i += 1

    if i >= 3:
        i = 0
i = 0
for node in Sibusersetgraph:
    left = Sibusersetgraph[node]['coordinates'][0]/1000
    right = Sibusersetgraph[node]['coordinates'][1]/1000
    cr.rectangle(left, 700, right-left, 80)
    cr.set_source_rgb(*palette[i])
    cr.fill()
    i += 1

    if i >= 3:
        i = 0
ims.write_to_png(args.png_save_way)
