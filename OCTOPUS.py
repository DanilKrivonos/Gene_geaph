import argparse
import sys
import numpy as np 
import networkx as nx
import pandas as pd
import pydot
from pydot import Graph, Node, Edge, Dot
import json

parser = argparse.ArgumentParser(description='Synteny graph drawer')
parser.add_argument('-graph', 
    type=str, 
    help='Print path to your synteny matrix', 
    required=True
    )
parser.add_argument('-ref', 
    type=str, 
    help='Print name of the reference orgsnism',
    default='g1'
    )
parser.add_argument('-start_node', 
    type=str, 
    default=None, 
    help='Print name of strt node'
    )
parser.add_argument('-annotation', 
    type=str, 
    default=None, 
    help='Print path to annotation'
    )
parser.add_argument('-depth_lim', 
    type=str, 
    default='full', 
    help='Graph traversal depth'
    )
parser.add_argument('-dot_save_way', 
    type=str, 
    default=None, 
    help='Print output path to dot file'
    )
parser.add_argument('-png_save_way', 
    type=str, 
    default=None, 
    help='Print output path to png picture'
    )
parser.add_argument('-svg_save_way', 
    type=str, 
    default=None, 
    help='Print output path to svg picture'
    )
parser.add_argument('-json', 
    type=str, 
    default=None, 
    help='If you want to take json print Need'
    )
parser.add_argument('-save_way', 
    type=str, 
    default=None, 
    help='output image file'
    )
args = parser.parse_args()

print('Oh, it seems someone wants to appreciate unstable :)')
pdEdges = pd.read_csv(args.graph, 
    header=None, 
    names=('source', 'target', 'genome', 'coordinate1', 'coordinate2', 'maxlen'), 
    sep='\t'
    ).drop(0)

GeneGraph = {}
Edges = {}
ref_nodes = set()
ref_edges = set()
max_len = 0 
print('Starting parsing your matrix ...')
for i in range(len(pdEdges)):
    if i != 0:
        if pdEdges['source'][i] not in GeneGraph:
            length = int(abs(int(pdEdges['coordinate1'][i]) - int(pdEdges['coordinate2'][i])))
            GeneGraph[pdEdges['source'][i]] = {
                'length': length/ int(pdEdges['maxlen'][i])*7.4 + 0.01,
                'adj': [],
                'coordinates': (int(pdEdges['coordinate1'][i]),  int(pdEdges['coordinate2'][i])),
                'annotation' : []
            }
        max_len = int(pdEdges['maxlen'][i])
        if pdEdges['target'][i] not in GeneGraph:
            length = int(abs(int(pdEdges['coordinate1'][i + 1]) - int(pdEdges['coordinate2'][i + 1])))
            GeneGraph[pdEdges['target'][i]] = {
                'length': length/int(pdEdges['maxlen'][i])*7.4 + 0.01,
                'adj': [],
                'coordinates' :  (int(pdEdges['coordinate1'][i]), int(pdEdges['coordinate2'][i])),
                'annotation' : []
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

if args.annotation != None:
    annotation = pd.read_csv(args.annotation, 
        header=None, 
        names=('Strain', 'SB', 'Coord_of_SB','Protein', 'Coord_of_prot', 'Part', 'Condition'), 
        sep='\t'
        ).drop(0)
    for node in GeneGraph:
        for ind in range(len(annotation)):
            if ind == 0:
                continue
            if node == annotation['SB'][ind]:
                GeneGraph[node]['annotation'] = '{} {} {}'.format(
                    annotation['Protein'][ind], 
                    annotation['Part'][ind], 
                    annotation['Condition'][ind]
                    )

Gdot = Dot(graph_type='digraph')

for node in GeneGraph:
    if node in ref_nodes:
        Gdot.add_node(Node(name=node, 
        width=str( GeneGraph[node]['length']), 
        color='red'
        ))
    else:
        Gdot.add_node(Node(name=node, 
        width=str( GeneGraph[node]['length']), 
        color='royalblue'
        ))

for node in GeneGraph:
    for _node in GeneGraph[node]['adj']:
        if (node, _node[0]) in ref_edges:
            Gdot.add_edge(Edge(src=node, 
            dst=_node[0], 
            penwidth=str(np.sqrt(_node[1])), 
            weight=str(_node[1]*1000), 
            color='red'
            ))

        else:
            Gdot.add_edge(Edge(src=node, 
            dst=_node[0], 
            penwidth=str(np.sqrt(_node[1])), 
            weight=str(_node[1]), 
            color='royalblue'
            ))
print('Your graph is written ...')
for i in Gdot.get_nodes():
    i.set_shape('box')
    i.set_style('filled')
G=nx.nx_pydot.from_pydot(Gdot)

if args.depth_lim == 'full':
    print('Making full graph ...')
    for node in Gdot.get_nodes():
        node.set_shape('box')
        node.set_style('rounded')
    Gdot.set_rotate('landscape')
    Gdot.set_orientation('lL')
    Gdot.set_splines('ortho')
    Gdot.set_rankdir('LR')
    if args.dot_save_way != None:
        Gdot.write(args.dot_save_way)
    elif args.png_save_way != None:
        Gdot.write_png(args.png_save_way)
    elif args.svg_save_way != None:
        Gdot.write_svg(args.svg_save_way)

else:
    lim_G = nx.Graph(nx.bfs_edges(G,   
        args.start_node, 
        reverse=False, 
        depth_limit=int(args.depth_lim)
        ))

    lset = set(lim_G.nodes) 
    not_short_graph_nodes = []
    for node in G.nodes:
        if node not in set(lim_G.nodes):
            not_short_graph_nodes.append(node)

    G.remove_nodes_from(not_short_graph_nodes)
    short_G = nx.nx_pydot.to_pydot(G)

    print('Drow your graph...')
    for node in short_G.get_nodes():
        node.set_shape('box')
        node.set_style('rounded')
    short_G.set_rotate('landscape')
    short_G.set_orientation('lL')
    short_G.set_splines('ortho')
    short_G.set_rankdir('LR')
    if args.dot_save_way != None:
        short_G.write(args.dot_save_way)
    elif args.png_save_way != None:
        short_G.write_png(args.png_save_way)
    elif args.svg_save_way != None:
        short_G.write_svg(args.svg_save_way)
    print('Now, you can look at it!')

if args.json == 'Need':
    ('Making json ...')
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

    for i in graphWithPositions.get_nodes():
        nodename = i.get_name()
        for node in JGG['elements']['nodes']:
            if nodename == node['data']['id']:
                print(node['data'])
                y, x = i.get_pos()[1:-1].split(',')
                node['data']['x'] = float(x)
                node['data']['y'] = float(y)
                print(node['data'])
    for node in JGG['elements']['nodes']:
        node['data']['width'] = (((float(node['data']['width']) - 0.01 ) * max_len) /7.4)/ 100
        for i in GeneGraph:
            node['data']['coordinates'] = str(GeneGraph[i]['coordinates'])
            node['data']['annotation'] = str(GeneGraph[i]['annotation'])
        print(node['data'])

    my_details = short_G
    with open(args.save_way + '.json', 'w') as json_file:
        json.dump(JGG, json_file)
    
    print('json was compiled')
print('Done!')