import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph
from ReadDataset import *
fh=open("data/facebook_combined.txt","rb")
G=nx.read_edgelist(fh, create_using=nx.Graph(), nodetype=int, data=False)

# pos = nx.spring_layout(G,k=0.5,iterations=20)
# nx.draw(G)
final = [3437, 107, 1684, 0, 1912, 348, 686, 3980, 414, 698]
ogreedy = [0, 34, 3490, 107, 3980, 3468, 686, 3439, 3442, 3476]
greedy = [0, 353, 107, 363, 395, 366, 370, 373, 376, 348]
spectral = [257, 1632, 2052, 1536, 578, 768, 3840, 3072, 2944, 4002]
color_map = []
size_list = []
for node in G:
    if node in spectral:
        color_map.append('orange')
        size_list.append(120)
    else:
        color_map.append('green')
        size_list.append(2)

nx.draw(G,node_color = color_map, node_size=size_list)
plt.show()

# d = dict(nx.degree(G))
#
# nx.draw(G, nodelist=d.keys(), node_size=[v * 5 for v in d.values()])
# # plt.show()
#
# plt.show()

# dot = Digraph(comment='My Network')
#
# def make_topology(network_name, mytopo):
#     dot = Digraph(comment=network_name, format='png')
#     dot.attr('node', shape='box')
#     dot.attr('edge', dir='both')
#     dot.attr('edge', arrowsize='2')
#     dot.body.append(r'label = "\n\nMy Prettier Network Diagram"')
#     dot.body.append('fontsize=20')
#     for i in mytopo[0]:
#         dot.node(i)
#     for i in mytopo[1]:
#         dot.edge(i[0], i[1], i[2])
#     return dot
#
# edges_list, weight_list, nodes_set = ReadGraphFile ("data/facebook_combined.txt")
# my_topo = [list(nodes_set), edges_list]
# dot = make_topology("My New Network", my_topo)
# dot.render(filename='SimplePrettierTopo')