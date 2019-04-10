#!/usr/local/bin/python3.6

import sys, random
from Graph import *
from ReadDataset import *
from Heuristic import *
from adjacencyMatrix import *
import matplotlib.pyplot as pyplot;
import time;
from sklearn.cluster import SpectralClustering
from InfluenceUtility import *
sys.setrecursionlimit(100000)



# random.seed(0)

#Test function for spectral clustering
def test():
    edges_list, weightlist,  nodes_set = ReadGraphFile(sys.argv[1])
    g = CreateGraph(edges_list)
    adjacency_list = g.adjlist()
    adjacency_matrix = create_adj_matrix(adjacency_list)
    # print(len(adjacency_matrix))
    k = 101
    k_influence = []
    for index in range(1,k):
        sc = SpectralClustering(k, affinity='precomputed', n_init=100)
        sc.fit(adjacency_matrix)
        y_pred = sc.labels_
        # print(y_pred)
        cluster_points = {}
        greedyHeuristicSelectedSet = set()
        for index, label in enumerate(y_pred):
            if cluster_points.get(label):
                cluster_points[label].append(index+1)
            else:
                cluster_points[label] = [index+1]
        # print(cluster_points)

        #max influence in each cluster:
        total_influence = 0
        for label, cluster in cluster_points.items():
            edgesCluster, weightlist = createGraphSubset(cluster, edges_list)
            step_size = 1
            threshold = 2
            graph_snaps = CreateRandomGraphs(50, edgesCluster, weightlist)
            influenceMap = getInfluenceMap(set(cluster), graph_snaps, threshold)
            greedyHeuristicSelectedSet = set()
            # print(heuristic2(graph_snaps, set(cluster), 1, step_size, threshold, influenceMap, greedyHeuristicSelectedSet))
            greedyHeuristicCount=len(heuristic2(graph_snaps, set(cluster), 1, step_size, threshold, influenceMap, greedyHeuristicSelectedSet))
            # print("influence:", greedyHeuristicCount)
            total_influence += greedyHeuristicCount
        # print("12 clusters:",total_influence)
        k_influence.append(total_influence)

    totalNodes = [x for x in range(1, k)]
    pyplot.plot(totalNodes, k_influence, '-r', label='Spectral Clustering')
    pyplot.legend(loc='upper left')
    pyplot.ylabel('Total nodes influences');
    pyplot.xlabel('Total nodes selected');
    pyplot.show()
    pyplot.savefig('Sc');

def main () :
    edges_list, weight_list, nodes_set = ReadGraphFile (sys.argv[1])
    graph_snaps = CreateRandomGraphs (10, edges_list, weight_list)

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
    threshold = 5
    totalNodes = range(0, 2);

    #optimizedGreedyHeuristic = [];
    greedyHeuristic = [];
    randomHeuristic = [];
    #optimizedGreedyHeuristic.append(0);
    greedyHeuristic.append(0);
    randomHeuristic.append(0);

    # print (len(influence.find_influence(set([65687]), graph_snaps, threshold)))
    # print (len(influence.find_influence(set([44262]), graph_snaps, threshold)))
    influenceMap = getInfluenceMap(nodes_set,graph_snaps,threshold);
    #optimizedGreedyHeuristicSelectedSet = set();
    greedyHeuristicSelectedSet = set();
    randomHeuristicTime = [];
    randomHeuristicTime.append(0);
    #optimizedGreedyHeuristicTime = [];

    #optimizedGreedyHeuristicTime.append(0);
    greedyHeuristicTime = [];
    greedyHeuristicTime.append(0);

    for k in totalNodes :
        print ("k = ", k)

        if k == 0:
            continue;

        startTime = time.time();
        randomHeuristicCount = random_heuristic(graph_snaps, nodes_set, k, step_size, threshold);
        randomHeuristicTime.append(time.time() - startTime);
        randomHeuristic.append(randomHeuristicCount);

        startTime = time.time();
        #influenceSet = heuristic1(graph_snaps, nodes_set, k, step_size, threshold,influenceMap,optimizedGreedyHeuristicSelectedSet);
        #optimizedGreedyHeuristicTime.append(time.time() - startTime);
        # print(influenceSet);
        #print("Size of influenced set is ", len(influenceSet));


        # print ("random influenced set is ", influenceSetRandom)
        #optimizedGreedyHeuristicCount = len(influenceSet);
        startTime = time.time();
        greedyHeuristicCount = len(heuristic2(graph_snaps,nodes_set,k,step_size,threshold,influenceMap,greedyHeuristicSelectedSet));
        greedyHeuristicTime.append(time.time() - startTime);
        print("Size of influenced set by greedy heuristic is ", greedyHeuristicCount);


        print ("Size of influenced set by random heuristic is ", randomHeuristicCount)

        #optimizedGreedyHeuristic.append(optimizedGreedyHeuristicCount);
        greedyHeuristic.append(greedyHeuristicCount);
        #print("Selected set for optimized greedy heuristic is ", optimizedGreedyHeuristicSelectedSet);
        print("Selected set for  greedy heuristic is ", greedyHeuristicSelectedSet);


    #pyplot.plot(totalNodes, optimizedGreedyHeuristic, '-b', label='Optimized Greedy Heuristic')
    pyplot.plot(totalNodes, greedyHeuristic, '-r', label='Greedy Heuristic')
    pyplot.plot(totalNodes, randomHeuristic, '-g', label='Random Heuristic')

    pyplot.legend(loc='upper left')
    pyplot.ylabel('Total nodes influnced');
    pyplot.xlabel('Total nodes selected');
    pyplot.show()

   # pyplot.plot(totalNodes, optimizedGreedyHeuristicTime, '-b', label='Optimized Greedy Heuristic')
    pyplot.plot(totalNodes, greedyHeuristicTime, '-r', label='Greedy Heuristic')
    pyplot.plot(totalNodes, randomHeuristicTime, '-g', label='Random Heuristic')

    pyplot.legend(loc='upper left')
    pyplot.ylabel('Total execution time');
    pyplot.xlabel('Total nodes selected');
    pyplot.show()
    pyplot.savefig('greedy_heuristics_time');


# main ()
test()