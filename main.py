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
def addition_deletion(graph, p=0.8, q=0.3):
    '''
    First, the addition or deletion is decided (based on p value).
    Then, a node is selected for addition or deletion. Then the node and edge get added or the node gets deleted'''

    global NodeCounter
    global TimeCounter

    if random.random() < p:  #addition
        degree_matrix_for_addition = return_degree_matrix_for_addition(graph)
        NodeCounter += 1
        TimeCounter += 1
        p = degree_matrix_for_addition[:,1] / (degree_matrix_for_addition[:,1].sum())
        node_to_connect_to = np.random.choice(degree_matrix_for_addition[:,0], 1, p=p)
        graph.add_node(NodeCounter)
        graph.add_edge(NodeCounter, node_to_connect_to[0])

    else:  #deletion
        degree_matrix_for_deletion = return_degree_matrix_for_deletion(graph)
        TimeCounter += 1
        p = degree_matrix_for_deletion[:,1] / (degree_matrix_for_deletion[:,1].sum())
        node_to_delete = np.random.choice(degree_matrix_for_deletion[:,0], 1, p=p)
        graph.remove_node(node_to_delete[0])

    return graph



NodeCounter = float(2)
TimeCounter = float(2)


def main():

    #set the testing p-values and the timesteps to record the results
    p_value = [0.6, 0.75, 0.9]
    times = [10000,20000,30000,40000,50000]

    #open the csv file and put the headings in the first row
    with open("results-nodes.csv", "w",) as f:
        writer = csv.writer(f)
        writer.writerow(["10000","20000","30000","40000","50000","trial", "p-value"])


    with open("results-edges.csv", "w",) as file:
        writer2 = csv.writer(file)
        writer2.writerow(["10000","20000","30000","40000","50000","trial", "p-value"])

    #runtime = []
    for p in p_value:

        for t in range(1,10):
            #runtime.append(time.time())
            G = nx.Graph()

            # adding two first nodes and the edge between them manually
            G.add_node(float(1))
            G.add_node(float(2))
            G.add_edge(1, 2)
            y = []
            z = []
            #set the required timesteps needed here. In the paper it's 50000
            for i in range(3,50005):

                #check if all the nodes all deleted, two initial nodes and the edge between them gets added manually
                if G.number_of_nodes() == 0:
                    G.add_node(float(1))
                    G.add_node(float(2))
                    G.add_edge(1, 2)
                    G = addition_deletion(G,p)
                else:
                    G = addition_deletion(G,p)

                #recording the results
                if i in times:
                    #runtime.append(time.time())
                    #print("reached step %s: This took %s second" %(i, runtime[-1] - runtime[-2]))
                    y.append(G.number_of_nodes())
                    z.append(G.number_of_edges())

            with open("results-nodes.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow(y+[t]+[p])

            with open("results-edges.csv","a") as file:
                writer2 = csv.writer(file)
                writer2.writerow(z+[t]+[p])

    #print("---%s seconds ---" %(time.time() - start_time))
if __name__ == "__main__":
    main()
