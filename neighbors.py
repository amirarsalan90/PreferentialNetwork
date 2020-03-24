import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import csv
import time


#calculates the probability of each node to make an edge with the newcomer node
def compute_prob_each_node_addition(x,total_edge):
    if total_edge != 0:
        return x/(2*total_edge)
    else:
        return 1


#calculates the probability for each node to get deleted
def compute_prob_each_node_deletion(x,total_edge, total_node):
    if total_edge != 0:
        return (total_node-x)/(total_node*total_node-2*total_edge)
    else:
        return 1


#forms a matrix with the first column as nodes and the second column as the node's probability of getting getting the new edge
def return_degree_matrix_for_addition(graph):
    '''Because graph.degree gives us a networkx object which is hard to work with, first it is converted to a list*
    Then the list gets converted to a numpy array.

    We have a function (compute_pro_each_node_addition). We want to apply this function to each element of the first column
    and put it in front of it in the second column. So we have to vectorize the function.'''
    degree_list = [[node,degree] for node,degree in graph.degree]
    degree_matrix = np.array(degree_list)
    vfunc = np.vectorize(compute_prob_each_node_addition)
    temp = vfunc(degree_matrix[:,1], graph.number_of_edges())
    degree_matrix[:,1] = temp
    return degree_matrix



#forms a matrix with the first column as nodes and the second column as the node's probabiliyt of getting deleted
def return_degree_matrix_for_deletion(graph):
    degree_list = [[node, degree] for node, degree in graph.degree]
    degree_matrix = np.array(degree_list)
    vfunc = np.vectorize(compute_prob_each_node_deletion)
    temp = vfunc(degree_matrix[:,1], graph.number_of_edges(), graph.number_of_nodes())
    degree_matrix[:,1] = temp
    return degree_matrix



#this function gets adds or deletes a node and returns the graph
def addition_deletion(graph, p=0.8):
    '''
    First, the addition or deletion is decided (based on p value).
    Then, a node is selected for addition or deletion. Then the node and edge get added or the node gets deleted'''

    global NodeCounter
    global TimeCounter
    global new_round

    if new_round == False:
        TimeCounter = float(2)
        new_round = True

    if random.random() < p:  #addition
        degree_matrix_for_addition = return_degree_matrix_for_addition(graph)
        NodeCounter += 1
        TimeCounter += 1
        neighbors_degree = []
        p = degree_matrix_for_addition[:,1] / (degree_matrix_for_addition[:,1].sum())
        node_to_connect_to = np.random.choice(degree_matrix_for_addition[:,0], 1, p=p)
        chosen_node_degree = graph.degree(node_to_connect_to[0])
        graph.add_node(NodeCounter)
        graph.add_edge(NodeCounter, node_to_connect_to[0])

    else:  #deletion
        degree_matrix_for_deletion = return_degree_matrix_for_deletion(graph)
        TimeCounter += 1
        p = degree_matrix_for_deletion[:,1] / (degree_matrix_for_deletion[:,1].sum())
        node_to_delete = np.random.choice(degree_matrix_for_deletion[:,0], 1, p=p)
        neighbors_degree = []
        if TimeCounter > 40000:
            neighbors = graph[node_to_delete[0]]
            new_round = False
            for i in neighbors:
                neighbors_degree.append(graph.degree(i))
        chosen_node_degree = graph.degree(node_to_delete[0])
        graph.remove_node(node_to_delete[0])

    return graph, neighbors_degree, chosen_node_degree






NodeCounter = float(2)
TimeCounter = float(2)
new_round = True

def main():


    # set the testing p-values and the timesteps to record the results
    p = 0.8
    # with open("neighbors.csv", "w") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["list","degree"])

    for t in range(1,100):
        print("run",t)
        #runtime.append(time.time())
        G = nx.Graph()

        # adding two first nodes and the edge between them manually
        G.add_node(float(1))
        G.add_node(float(2))
        G.add_edge(1, 2)

        neighbors_degree = []
        new_round = True

        #set the required timesteps needed here. In the paper it's 50000
        for i in range(3,41000):

            print("loop number: ",i)

            #check if all the nodes all deleted, two initial nodes and the edge between them gets added manually
            if G.number_of_nodes() == 0:
                G.add_node(float(1))
                G.add_node(float(2))
                G.add_edge(1, 2)
                G, neighbors_degree, chosen_node_degree = addition_deletion(G, p)
            else:
                G, neighbors_degree, chosen_node_degree = addition_deletion(G, p)

            if len(neighbors_degree) != 0:
                break


        with open("neighbors.csv", "a") as file:
            writer2 = csv.writer(file)
            writer2.writerow(neighbors_degree+[chosen_node_degree])



main()