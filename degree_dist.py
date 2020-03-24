import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import collections
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
   p = 0.8

   for t in range(1,2):
       #runtime.append(time.time())
       G = nx.Graph()

       # adding two first nodes and the edge between them manually
       G.add_node(float(1))
       G.add_node(float(2))
       G.add_edge(1, 2)
       y = []
       z = []
       #set the required timesteps needed here. In the paper it's 50000
       for i in range(3,20000):
           print("loop number:",i)

           #check if all the nodes all deleted, two initial nodes and the edge between them gets added manually
           if G.number_of_nodes() == 0:
               G.add_node(float(1))
               G.add_node(float(2))
               G.add_edge(1, 2)
               G = addition_deletion(G,p)
           else:
               G = addition_deletion(G,p)

       def f(x):
           return (x**(-3.667))

       x = np.arange(1,80,0.25)
       y = [f(t) for t in x]
       y_norm = [t/sum(y) for t in y]
       y_cumul = [sum(y[t+1:])/sum(y) for t in range(len(y))]
       degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
       degreeCount = collections.Counter(degree_sequence)
       deg, cnt = zip(*degreeCount.items())
       cnt_norm = [x/sum(cnt) for x in cnt]
       cnt_cumul = [sum(cnt[:x+1])/sum(cnt) for x in range(len(cnt))]

       fig, ax = plt.subplots()
       ax.plot(deg[:-1], cnt_cumul[:-1], 'rs')
       ax.plot(x,y_cumul,'b-')
       ax.set_xlabel("k", fontsize=15)
       ax.set_ylabel("$p'(k)$", fontsize=15)
       plt.xscale("log")
       plt.yscale("log")
       plt.savefig("plot4.png")

       plt.show()


main()

