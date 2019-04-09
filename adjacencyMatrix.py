# Adjacency matrix for the graph
def create_adj_matrix(adjacency_list):
    max_length = 0
    for node, neighbors in adjacency_list.items():
        if node > max_length:
            max_length = node
        temp_max = max(neighbors)
        if temp_max > max_length:
            max_length = temp_max

    # initialize a matrix for the range (0 -> max_length)
    adjacency_matrix = [[0 for i in range(0, max_length + 1)] for j in range(max_length + 1)]

    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            adjacency_matrix[node][neighbor] = 1
            adjacency_matrix[neighbor][node] = 1
    # print(max_length) = 4038 for facebook dataset
    return adjacency_matrix


def print_matrix(matrix):
    for i in range(0, len(matrix)):
        print("\n ", matrix[i], ":")
        for j in range(0, len(matrix)):
            print(matrix[i][j])

'''
Testing:
def test():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(2, 4)
    g.add_edge(5, 3)
    g.add_edge(1, 4)
    g.add_edge(2, 3)
    g.print_graph()
    adjacency_list = g.adjlist()
    adjacency_matrix = create_adj_matrix(adjacency_list)
    print(adjacency_matrix)

test()
'''
