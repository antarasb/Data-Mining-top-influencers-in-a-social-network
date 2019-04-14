
from Heuristic import *
from adjacencyMatrix import *
import time;
from sklearn.cluster import SpectralClustering
from pagerank import *

def spectral():
    edges_list, weightlist,  nodes_set = ReadGraphFile(sys.argv[1])
    g = CreateGraph(edges_list)
    adjacency_list = g.adjlist()
    adjacency_matrix = create_adj_matrix(adjacency_list)
    # print(len(adjacency_matrix))
    k = 10
    k_influence = [0]
    for index in range(1,k+1):
        start_time = time.time()
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


        #max influence in each cluster:
        total_influence = 0
        for label, cluster in cluster_points.items():
            edgesCluster, weightlist = createGraphSubset(cluster, edges_list)
            step_size = 1
            threshold = 5
            graph_snaps = CreateRandomGraphs(50, edgesCluster, weightlist)
            influenceMap = getInfluenceMap(set(cluster), graph_snaps, threshold)
            greedyHeuristicSelectedSet = set()
            if k == 10:
                print(heuristic2(graph_snaps, set(cluster), 1, step_size, threshold, influenceMap, greedyHeuristicSelectedSet))
            greedyHeuristicCount=len(heuristic2(graph_snaps, set(cluster), 1, step_size, threshold, influenceMap, greedyHeuristicSelectedSet))
            # print("influence:", greedyHeuristicCount)
            total_influence += greedyHeuristicCount
        # print("12 clusters:",total_influence)
        k_influence.append(total_influence)
        timer.append(time.time() - start_time)
    return k_influence