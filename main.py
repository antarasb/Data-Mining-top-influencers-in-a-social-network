#!/usr/local/bin/python3.6

import sys, random
from Graph import *
from ReadDataset import *
from Heuristic import *
from adjacencyMatrix import *
import matplotlib.pyplot as pyplot;
import time;
from sklearn.cluster import SpectralClustering
from pagerank import *
from spectral import *

from InfluenceUtility import *
sys.setrecursionlimit(100000)



# random.seed(0)

#Test function for spectral clustering



def main () :
    fh = open(sys.argv[1], "rb")
    G = nx.read_edgelist(fh, create_using=nx.Graph(), nodetype=int, data=False)
    edges_list, weight_list, nodes_set = ReadGraphFile (sys.argv[1])
    graph_snaps = CreateRandomGraphs (50, edges_list, weight_list)

    # for graph in graph_snaps :
    #     print ("new graph")
    #     graph.print_graph ()
    # y = []
    # for i in range (1,10) :
    #     l = len((find_influence (set([24325]), graph_snaps, i)))
    #     print (l)
    #     y.append(l)
    
    # np.plot (range (1,10), y)
    # np.show ()
    
    # i = 0
    # nodes_list = list(nodes_set)
    # for i in range(len(nodes_list)-10) :
    #     # print (i, len(find_influence (set([nodes_list[i], nodes_list[i+1], nodes_list[i+2], nodes_list[i+3], nodes_list[i+4]]), graph_snaps, 45)))
    #     print (i, nodes_list[i], len(find_influence (set([nodes_list[i]]), graph_snaps, 30)))

    step_size = 1;
    threshold = 1
    totalNodes = range(0, 11);

    optimizedGreedyHeuristic = [];
    greedyHeuristic = [];
    randomHeuristic = [];
    optimizedGreedyHeuristic.append(0);
    greedyHeuristic.append(0);
    randomHeuristic.append(0);

    # print (len(influence.find_influence(set([65687]), graph_snaps, threshold)))
    # print (len(influence.find_influence(set([44262]), graph_snaps, threshold)))
    influenceMap = getInfluenceMap(nodes_set,graph_snaps,threshold);
    optimizedGreedyHeuristicSelectedSet = set();
    greedyHeuristicSelectedSet = set();
    randomHeuristicTime = [];
    randomHeuristicTime.append(0);
    optimizedGreedyHeuristicTime = [];

    optimizedGreedyHeuristicTime.append(0);
    greedyHeuristicTime = [];
    greedyHeuristicTime.append(0);

    pageRankTime = [];
    pageRankTime.append(0)

    spectralClusteringTime = []
    spectralClusteringTime.append(0)

    for k in totalNodes :
        print ("k = ", k)

        if k == 0:
            continue;

        startTime = time.time();
        randomHeuristicCount = random_heuristic(graph_snaps, nodes_set, k, step_size, threshold);
        randomHeuristicTime.append(time.time() - startTime);
        randomHeuristic.append(randomHeuristicCount);

        startTime = time.time();
        influenceSet = heuristic1(graph_snaps, nodes_set, k, step_size, threshold,influenceMap,optimizedGreedyHeuristicSelectedSet);

        optimizedGreedyHeuristicTime.append(time.time() - startTime);
        # print(influenceSet);
        #print("Size of influenced set is ", len(influenceSet));


        # print ("random influenced set is ", influenceSetRandom)
        optimizedGreedyHeuristicCount = len(influenceSet);
        startTime = time.time();
        greedyHeuristicCount = len(heuristic2(graph_snaps,nodes_set,k,step_size,threshold,influenceMap,greedyHeuristicSelectedSet));
        greedyHeuristicTime.append(time.time() - startTime)
        # print("Size of influenced set by greedy heuristic is ", greedyHeuristicCount);


        #print ("Size of influenced set by random heuristic is ", randomHeuristicCount)

        optimizedGreedyHeuristic.append(optimizedGreedyHeuristicCount);
        greedyHeuristic.append(greedyHeuristicCount);
        print("Selected set for optimized greedy heuristic is ", optimizedGreedyHeuristicSelectedSet);
        print("Selected set for  greedy heuristic is ", greedyHeuristicSelectedSet);

    g = CreateGraph(edges_list)
    #=================================
    t1 = time.time()
    dictionary = pagerank(G)
    sorted_x = sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True)
    nodes = []
    for index in range(0, k):
        nodes.append(sorted_x[index][0])
    # print(nodes)
    visited = set()
    influence = [0]
    t2 = time.time()

    for node in nodes:
        startTime = time.time();

        g.dfs_clustering(node, visited)
        influence.append(len(visited))
        pageRankTime.append(time.time() - startTime)
    vals = [x for x in range(0, k+1)]
    print("Page Rank Top 10", nodes[:11])
    pyplot.plot(vals, influence, '-y', label='PageRank Algorithm')


    # =================================
    # closeness_dict = closeness_centrality(G)
    # sorted_x = sorted(closeness_dict.items(), key=lambda kv: kv[1], reverse=True)
    # nodes = []
    # for index in range(0, k):
    #     nodes.append(sorted_x[index][0])
    # visited = set()
    # influences = [0]
    # for node in nodes:
    #
    #     g.dfs_clustering(node, visited)
    #     influences.append(len(visited))
    # pyplot.plot(vals, influences, '-m', label='Closeness centrality')
    # #===========================================
    # startTime = time.time()
    sc_clustering = spectral()
    pyplot.plot(vals, sc_clustering, '-k', label='Spectral Clustering')

    print("Starting to plot graphs:")
    pyplot.plot(totalNodes, optimizedGreedyHeuristic, '-b', label='Optimized Greedy Heuristic')
    pyplot.plot(totalNodes, greedyHeuristic, '-r', label='Greedy Heuristic')
    pyplot.plot(totalNodes, randomHeuristic, '-g', label='Random Heuristic')

    pyplot.legend(loc=4)
    pyplot.ylabel('Total nodes influenced');
    pyplot.xlabel('Total nodes selected');
    pyplot.show()
    pyplot.savefig('zoomed')
    pyplot.plot(totalNodes, optimizedGreedyHeuristicTime, '-b', label='Optimized Greedy Heuristic')
    pyplot.plot(totalNodes, greedyHeuristicTime, '-r', label='Greedy Heuristic')
    pyplot.plot(totalNodes, randomHeuristicTime, '-g', label='Random Heuristic')
    # pyplot.plot(totalNodes, spectralClusteringTime, '-k', label= 'Spectral Clustering')
    pyplot.plot(totalNodes, pageRankTime, '-y', label = 'PageRank ')

    pyplot.legend(loc=0)
    pyplot.ylabel('Total execution time');
    pyplot.xlabel('Total nodes selected');
    pyplot.show()
    pyplot.savefig('greedy_heuristics_time');

main ()
# test()