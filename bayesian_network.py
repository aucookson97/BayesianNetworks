import networkx as nx
import matplotlib.pyplot as plt
import sys
import random
import math

class Node():

    def __init__(self, name, parents, prob):
        self.name = name
        self.prob = prob
        self.parents = parents
        self.value = None
        self.evidence = None
        self.query = None

    def setValue(self, network):
        if self.value != None:
            return self.value
        val = random.random()
        if (len(self.parents) == 0): # Top Level Node
            if (val < self.prob[0]):
                self.value = False
            else:
                self.value = True
        else:
            index = 0
            for i in range(len(self.parents)):
                p = findNodeByName(self.parents[i], network.nodes())
                if p.setValue(network):
                    index += math.pow(2, i+1)
            if val < self.prob[int(index)]:
                self.value = False
            else:
                self.value = True
        return self.value
            
        
    def __str__(self):
        return("Name: {}\nParents: {}\nProb. Table: {}\nEvidence: {}\nQuery: {}\nValue: {}".format(self.name, self.parents, self.prob, self.evidence, self.query, self.value))

def createNetwork(input_file, assignment_file):
    network = nx.DiGraph()

    nodes_raw = []
    nodes = []

    with open(input_file, 'r') as file:
        l = file.read()
        nodes_raw = l.split('\n')
        
    for n in nodes_raw:
        #node = n.split(' ')
        node = n.split('[')
        if len(node) > 1:
            name = node[0].replace(':', '').strip()
            parents = node[1].replace(']', '').split(' ')
            parents = [p for p in parents if p != '']
            table = [float(i) for i in node[2].replace(']', '').split(' ')]
            nodes.append(Node(name, parents, table))
    nodes = assignValue(assignment_file, nodes)

    for node in nodes:
        network.add_node(node)
        for name in node.parents:
            pnode = findNodeByName(name, nodes)
            #print ('Edge: {}, {}'.format(pnode.name, node.name))
            network.add_edge(pnode, node)

    return network

def assignValue(input_file, node_list):

    queries = []

    with open(input_file, 'r') as file:
        l = file.read()
        queries = l.strip().split(',')
    for queryElem in range(len(queries)):
        if(queries[queryElem] == "?" or queries[queryElem] == "q"):
            node_list[queryElem].query = True
        if(queries[queryElem] == "t"):
            node_list[queryElem].evidence = True
        if(queries[queryElem] == "f"):
            node_list[queryElem].evidence = False
        if(queries[queryElem] == "-"):
            pass
    return node_list

def rejectionSampling(network, num_samples):

    total_valid_samples = 0
    num_queries = 0
    
    for i in range(num_samples):
        for node in network.nodes():
            node.setValue(network)
        if validEvidence(network):
            total_valid_samples += 1
            for node in network.nodes():
                if node.query:
                    if node.value:
                        num_queries += 1
                    break
        reset(network)

    probability = num_queries / float(total_valid_samples)
    return probability

def likelihoodWeighting(network, num_samples):
    return 1

def validEvidence(network):
    for node in network.nodes():
        if (node.evidence != None and node.evidence != node.value):
            return False
    return True

def reset(network):
    for node in network.nodes():
        node.value = None

def findNodeByName(name, node_list):
    for node in node_list:
        if node.name == name:
            return node
    return None

def drawNetwork(network):
    pos = nx.spectral_layout(network)
    network_labels = {}
    for node in network.nodes():
        network_labels[node] = node.name
    nx.draw_networkx_labels(network, pos, labels=network_labels)
    nx.draw(network, pos=pos)#cmap = plt.get_cmap('jet')) #node_color = values)
    plt.show()

def printNetwork(network):
    for node in network.nodes():
        print(node)
        print()


if __name__=="__main__":
        
#    print (sys.argv)
    input_file = "network_option_a.txt"
    assignment_file = "query1.txt"
    network = createNetwork(input_file, assignment_file)
    #prob = rejectionSampling(network, 100000)
    prob = likelihoodWeighting(network, 1000)
    print ('P(X|e) = {}'.format(prob))
    drawNetwork(network)
