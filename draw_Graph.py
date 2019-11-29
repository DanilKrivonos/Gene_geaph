import pandas as pd
import numpy as np 
from pydot import Graph, Node, Edge, Dot
import argparse

parser = argparse.ArgumentParser(description='Find shorteat way in graph')
parser.add_argument('-graph', type=str, help='graph.txt', required=True)
parser.add_argument('-dot_save_way', type=str, default=None, help='output DOT file')
parser.add_argument('-png_save_way', type=str, default=None, help='output image file')
parser.add_argument('-ref', type=str, required=True)


args = parser.parse_args()

if args.dot_save_way is None:
    args.dot_save_way = '{}.png'.format(args.graph)
if args.png_save_way is None:
    args.png_save_way = '{}.png'.format(args.graph)

print(args)


pdEdges = pd.read_csv(args.graph, header=None, names=['source', 'target', 'genome', 'len1', 'len2', '??'], sep=' ')

GeneGraph = {}
Edges = {}
ref_nodes = set()
ref_edges = set()

for i in range(len(pdEdges)):
    if pdEdges['source'][i] not in GeneGraph:
        GeneGraph[pdEdges['source'][i]] = {
            'length': pdEdges['len1'][i],
            'adj': []
        }
    if pdEdges['target'][i] not in GeneGraph:
        GeneGraph[pdEdges['target'][i]] = {
            'length': pdEdges['len2'][i],
            'adj': []
        }

    if pdEdges['genome'][i] == args.ref:
        ref_nodes.add(pdEdges['source'][i])
        ref_nodes.add(pdEdges['target'][i])
        ref_edges.add((pdEdges['source'][i], pdEdges['target'][i]))
    
    if (pdEdges['source'][i], pdEdges['target'][i]) not in Edges:
        Edges[(pdEdges['source'][i], pdEdges['target'][i])] = 0
    
    Edges[(pdEdges['source'][i], pdEdges['target'][i])] += 1
    
for edge in Edges:
    GeneGraph[edge[0]]['adj'].append((edge[1], Edges[edge]))


G = Dot()

for node in GeneGraph:
    if node in ref_nodes:
        G.add_node(Node(name=node, width=str(GeneGraph[node]['length']), color='red'))
    else:
        G.add_node(Node(name=node, width=str(GeneGraph[node]['length']), color='blue'))

for node in GeneGraph:
    for _node in GeneGraph[node]['adj']:
        if (node, _node[0]) in ref_edges:
            G.add_edge(Edge(src=node, dst=_node[0], penwidth=str(np.sqrt(_node[1])), weight=str(_node[1]), color='red'))

        else:
            G.add_edge(Edge(src=node, dst=_node[0], penwidth=str(np.sqrt(_node[1])), weight=str(_node[1]), color='blue'))

for i in G.get_nodes():
    i.set_shape('box')
    i.set_style('filled')

G.set_rotate('landscape')
G.set_orientation('lL')
G.set_overlap('false')
G.set_splines('ortho')
G.set_rankdir('LR')
G.write(args.dot_save_way)
G.write_png(args.png_save_way)