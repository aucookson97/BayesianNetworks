import networkx as nx
import matplotlib.pyplot as plt
import sys

class Node():

    def __init__(self, name, parents, prob):
        self.name = name
        self.prob = prob
        self.parents = parents
        self.evidence = None
        self.query = None

    def __str__(self):
        return("Name: {}\nParents: {}\nProb. Table: {}\nEvidence: {}\nQuery: {}\nUnknown: {}".format(self.name, self.parents, self.prob, self.evidence, self.query, self.unknown))

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
    printNodes(nodes)

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
        print(queries)
    for queryElem in range(len(queries)):
        if(queries[queryElem] == "?" or queries[queryElem] == "q"):
            node_list[queryElem].query = True
        if(queries[queryElem] == "t"):
            node_list[queryElem].evidence = True
        if(queries[queryElem] == "f"):
            node_list[queryElem].evidence = False
        if(queries[queryElem] == "-"):
            node_list[queryElem].query = False
            node_list[queryElem].evidence = False
    return node_list


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

def printNodes(node_list):
    for node in node_list:
        print(node)


if __name__=="__main__":
        
#    print (sys.argv)
    input_file = "network_option_a.txt"
    assignment_file = "query1.txt"
    network = createNetwork(input_file, assignment_file)
    drawNetwork(network)
