import argparse
import sys
import numpy as np 
import networkx as nx
import pandas as pd
import pydot
from pydot import Graph, Node, Edge, Dot
import json
parser = argparse.ArgumentParser(description='Draw sbgraph')
parser.add_argument('-graph', type=str, help='graph.txt', required=True)
parser.add_argument('-ref', type=str, default='g1')
parser.add_argument('-start_node', type=str, default=None, help='print node name')
parser.add_argument('-depth_lim', type=int, default=None, help='lim of nodes')
parser.add_argument('-dot_save_way', type=str, default=None, help='output DOT file')
parser.add_argument('-png_save_way', type=str, default=None, help='output image file')
parser.add_argument('-svg_save_way', type=str, default=None, help='output image file')
parser.add_argument('-save_way', type=str, default=None, help='output image file')
args = parser.parse_args()

if args.dot_save_way is None:
    args.dot_save_way = '{}.png'.format(args.graph)
if args.png_save_way is None:
    args.png_save_way = '{}.png'.format(args.graph)

#import matrix with numpy
A = np.loadtxt(args.graph, dtype=np.str)

pdEdges = pd.read_csv(args.graph, header=None, names=['source', 'target', 'genome', 'len1', 'len2', 'coordinate1', 'coordinate2', 'maxlen'], sep=' ')

GeneGraph = {}
Edges = {}
ref_nodes = set()
ref_edges = set()
max_len = 0 
for i in range(len(pdEdges)):
    if pdEdges['source'][i] not in GeneGraph:
        GeneGraph[pdEdges['source'][i]] = {
            'length': int(pdEdges['len1'][i])/int(pdEdges['maxlen'][i])*7.4 + 0.01,
            'adj': [],
            'coordinates': (int(pdEdges['coordinate1'][i]),  int(pdEdges['coordinate2'][i]))
        }
    max_len = int(pdEdges['maxlen'][i])
    if pdEdges['target'][i] not in GeneGraph:
        GeneGraph[pdEdges['target'][i]] = {
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
    GeneGraph[edge[0]]['adj'].append((edge[1], Edges[edge]))

Gdot = Dot(graph_type='graph')

for node in GeneGraph:
    if node in ref_nodes:
        Gdot.add_node(Node(name=node, width=str( GeneGraph[node]['length']), color='red'))
    else:
        Gdot.add_node(Node(name=node, width=str( GeneGraph[node]['length']), color='royalblue'))

for node in GeneGraph:
    for _node in GeneGraph[node]['adj']:
        if (node, _node[0]) in ref_edges:
            Gdot.add_edge(Edge(src=node, dst=_node[0], penwidth=str(np.sqrt(_node[1])), weight=str(_node[1]*1000), color='red'))

        else:
            Gdot.add_edge(Edge(src=node, dst=_node[0], penwidth=str(np.sqrt(_node[1])), weight=str(_node[1]), color='royalblue'))

for i in Gdot.get_nodes():
    i.set_shape('box')
    i.set_style('filled')
print(Gdot.get_nodes()[0])
print(GeneGraph)
G=nx.nx_pydot.from_pydot(Gdot)
lim_G = nx.Graph(nx.bfs_edges(G, args.start_node, reverse=False, depth_limit=args.depth_lim))


lset = set(lim_G.nodes) 
not_short_graph_nodes = []
for node in G.nodes:
    if node not in set(lim_G.nodes):
        not_short_graph_nodes.append(node)

G.remove_nodes_from(not_short_graph_nodes)
short_G = nx.nx_pydot.to_pydot(G)

for node in short_G.get_nodes():
    node.set_shape('box')
    #node.set_style('filled')
    node.set_style('rounded')
short_G.set_rotate('landscape')
short_G.set_orientation('lL')
#for neato graph G.set_overlap('true')
short_G.set_splines('ortho')
short_G.set_rankdir('LR')
short_G.write(args.dot_save_way)#, prog='neato')
short_G.write_png(args.png_save_way)#, prog='neato')
short_G.write_svg(args.svg_save_way)#, prog='neato')

short_G = nx.nx_pydot.from_pydot(short_G)
__all__ = ['cytoscape_data', 'cytoscape_graph']

_attrs = dict(name='name', ident='id')

def cytoscape_data(short_G, attrs=None):
    if not attrs:
        attrs = _attrs
    else:
        attrs.update({k: v for (k, v) in _attrs.items() if k not in attrs})

    name = attrs["name"]
    ident = attrs["ident"]

    if len(set([name, ident])) < 2:
        raise nx.NetworkXError('Attribute names are not unique.')

    jsondata = {"data": list(short_G.graph.items())}
    jsondata['directed'] = short_G.is_directed()
    jsondata['multigraph'] = short_G.is_multigraph()
    jsondata["elements"] = {"nodes": [], "edges": []}
    nodes = jsondata["elements"]["nodes"]
    edges = jsondata["elements"]["edges"]

    for i, j in short_G.nodes.items():
        n = {"data": j.copy()}
        n["data"]["id"] = j.get(ident) or str(i)
        n["data"]["value"] = i
        n["data"]["name"] = j.get(name) or str(i)
        nodes.append(n)

    if short_G.is_multigraph():
        for e in short_G.edges(keys=True):
            n = {"data": short_G.adj[e[0]][e[1]][e[2]].copy()}
            n["data"]["source"] = e[0]
            n["data"]["target"] = e[1]
            n["data"]["key"] = e[2]
            edges.append(n)
    else:
        for e in short_G.edges():
            n = {"data": short_G.adj[e[0]][e[1]].copy()}
            n["data"]["source"] = e[0]
            n["data"]["target"] = e[1]
            edges.append(n)
    return jsondata
JGG = cytoscape_data(short_G)

graphWithPositions = pydot.graph_from_dot_data(Gdot.create_dot().decode('utf-8'))[0]
print(graphWithPositions.get_nodes())

#print(JGG['elements']['nodes'])
for i in graphWithPositions.get_nodes():
    nodename = i.get_name()
    for node in JGG['elements']['nodes']:
        if nodename == node['data']['id']:
            print(node['data'])
            x, y = i.get_pos()[1:-1].split(',')
            node['data']['x'] = float(x)
            node['data']['y'] = float(y)
            #node['data']['width'] = float(node['data']['width'])*100
            print(node['data'])
for node in JGG['elements']['nodes']:
    node['data']['width'] = (((float(node['data']['width']) - 0.01 ) * max_len) /7.4) / 100
    for i in GeneGraph:
        node['data']['coordinates'] = str(GeneGraph[i]['coordinates'])
    print(node['data'])

my_details = short_G
with open(args.save_way, 'w') as json_file:
    json.dump(JGG, json_file)
