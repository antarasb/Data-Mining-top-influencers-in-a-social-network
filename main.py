#!/usr/local/bin/python3.6

import sys, random
from Graph import *
from ReadDataset import *

sys.setrecursionlimit(100000)
import matplotlib.pyplot as pyplot;
import time;



# random.seed(0)

def main () :
    edges_list, weight_list, nodes_set = ReadGraphFile (sys.argv[1])
    graph_snaps = CreateRandomGraphs (50, edges_list, weight_list)

   
main ()
