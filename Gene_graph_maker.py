import argparse
parser = argparse.ArgumentParser(description='Find shorteat way in graph')
parser.add_argument('-graph', type=str, help='graph.txt', required=True)
parser.add_argument('-dot_save_way', type=str, help='new_save_way.dot', required=True)
parser.add_argument('-png_save_way', type=str, help='png_save_way.png', required=True)
parser.add_argument('-D', default=2, type=int, help='max-lengh')
args = parser.parse_args()
import sys

#import matrix 
import numpy as np 
A = np.loadtxt(args.graph, dtype=np.str)

#ref_maker
reference = []
new_ref = []
for i in A:
    if i[2] == 'g1':
        x = [i[0], i[1]]
        reference.append(x)

#graph_maker
graph = {}
for i in A:
    if i[0] not in graph:
        graph[i[0]] = []
    if i[1] not in graph:
        graph[i[1]] = []
    edge = (i[1], i[2], i[3], i[4], i[5])
    graph[i[0]].append(edge)

#new_ref
new_ref = {}
for i in A:
    if i[2] == 'g1':
        if i[0] not in new_ref:
            new_ref[i[0]] = []
        if i[1] not in new_ref:
            new_ref[i[1]] = []
        edge = (i[1])
        new_ref[i[0]].append(edge)



import networkx as nx
#Ref graph
RSG = nx.DiGraph()
for node in new_ref:
    for n in new_ref[node]:   
        RSG.add_node(node, color='red')
        edge = (node, n)
        RSG.add_edge(*edge, color='red')

#Gene graph 
G = nx.MultiDiGraph()
count=0
for node in graph:
    for n in graph[node]:
        edge = (node, n[0])
        if node in RSG.nodes:
            G.add_node(node, color='red', width=n[2])#, pos='{}, {}!'.format(count*1, 0))
            count+=1
        else:
            G.add_node(node, color='blue', width=n[2])
        if edge[0] in RSG and edge[1] in RSG:
            #G.edge_subgraph(edge)
            G.add_edge(*edge, color='red')
        else:
            G.add_edge(*edge, color='blue')
for node in G.nodes:
    if node not in RSG.nodes:
        G.add_node(node, color='blue')
    else:
        G.add_node(node, color='red')

print(G.nodes())

for edge in reference:

    for path in nx.all_simple_paths(G, source=edge[0], target=edge[1], cutoff=args.D):
        print(path)


#import pydot
#import graphviz as gv
G = nx.nx_pydot.to_pydot(G)
RSG = nx.nx_pydot.to_pydot(RSG)

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
