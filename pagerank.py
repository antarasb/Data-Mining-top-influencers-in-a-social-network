import networkx as nx
import matplotlib.pyplot as plt
from itertools import count
from operator import itemgetter
from Graph import *
from ReadDataset import *

fh=open("data/facebook_combined.txt","rb")
G=nx.read_edgelist(fh, create_using=nx.Graph(), nodetype=int, data=False)


def pagerank(G, alpha=0.85, personalization=None,
             max_iter=100, tol=1.0e-6, nstart=None, weight='weight',
             dangling=None):
    if len(G) == 0:
        return {}

    if not G.is_directed():
        D = G.to_directed()
    else:
        D = G

    # Create a copy in (right) stochastic form
    W = nx.stochastic_graph(D, weight=weight)
    N = W.number_of_nodes()

    # Choose fixed starting vector if not given
    if nstart is None:
        x = dict.fromkeys(W, 1.0 / N)
    else:
        # Normalized nstart vector
        s = float(sum(nstart.values()))
        x = dict((k, v / s) for k, v in nstart.items())

    if personalization is None:

        # Assign uniform personalization vector if not given
        p = dict.fromkeys(W, 1.0 / N)
    else:
        missing = set(G) - set(personalization)
        # if missing:
        #     raise NetworkXError('Personalization dictionary '
        #                         'must have a value for every node. '
        #                         'Missing nodes %s' % missing)
        s = float(sum(personalization.values()))
        p = dict((k, v / s) for k, v in personalization.items())

    if dangling is None:

        # Use personalization vector if dangling vector not specified
        dangling_weights = p
    else:
        missing = set(G) - set(dangling)
        # if missing:
        #     raise NetworkXError('Dangling node dictionary '
        #                         'must have a value for every node. '
        #                         'Missing nodes %s' % missing)
        s = float(sum(dangling.values()))
        dangling_weights = dict((k, v / s) for k, v in dangling.items())
    dangling_nodes = [n for n in W if W.out_degree(n, weight=weight) == 0.0]

    # power iteration: make up to max_iter iterations
    for _ in range(max_iter):
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        danglesum = alpha * sum(xlast[n] for n in dangling_nodes)
        for n in x:

            # this matrix multiply looks odd because it is
            # doing a left multiply x^T=xlast^T*W
            for nbr in W[n]:
                x[nbr] += alpha * xlast[n] * W[n][nbr][weight]
            x[n] += danglesum * dangling_weights[n] + (1.0 - alpha) * p[n]

        # check convergence, l1 norm
        err = sum([abs(x[n] - xlast[n]) for n in x])
        if err < N * tol:
            return x
    # raise NetworkXError('pagerank: power iteration failed to converge '
    #                     'in %d iterations.' % max_iter)
#
# dictionary = pagerank(G)
#
#
# # sorted_x = sorted(dictionary.items(), key=itemgetter(1), reverse=True)
# sorted_x = sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True)
# # for node, rank in dictionary.items():
# #     print("Node:", node, "Rank:", rank)
# nodes = []
# for index in range(0,5):
#     # print("index:", index,"Val:", sorted_x[index])
#     nodes.append(sorted_x[index][0])
# print(nodes)
#
# edges_list, weightlist,  nodes_set = ReadGraphFile('data/facebook_combined.txt')
# g = CreateGraph(edges_list)
#
# visited = set()
# influence = [0]
# for node in nodes:
#     g.dfs_clustering(node,visited)
#     influence.append(len(visited))
# print(len(visited))
#
# vals = [x for x in range(0,6)]
# plt.plot( vals, influence, '-g')
# plt.show()

# nx.draw(G, pos = nx.spring_layout(G))

# groups = set(nx.get_node_attributes(G, 'group').values())
# mapping = dict(zip(sorted(groups), count()))
# nodes = G.nodes()
# colors = [mapping.node[n]['group'] for n in nodes]
#
# pos = nx.spring_layout(G)
# ec = nx.draw_networkx_edges(G, pos, alpha = 0.2)
# mc = nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=colors, with_labels = False, node_size=100, cmap=plt.cm.jet)
# plt.show()
