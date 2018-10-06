import networkx as nx
import matplotlib.pyplot as plt
import sys

class Node():

    def __init__(self, name, parents, prob):
        self.name = name
        self.prob = prob
        self.parents = parents


def createNetwork(input_file):
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
    for node in nodes:
        network.add_node(node)
        for name in node.parents:
            pnode = findNodeByName(name, nodes)
            #print ('Edge: {}, {}'.format(pnode.name, node.name))
            network.add_edge(pnode, node)

    return network

def findNodeByName(name, node_list):
    for node in node_list:
        if node.name == name:
            return node
    return None

def drawNetwork(network):
    pos = nx.spring_layout(network)
    network_labels = {}
    for node in network.nodes():
        network_labels[node] = node.name
    nx.draw_networkx_labels(network, pos, labels=network_labels)
    nx.draw(network, pos=pos)#cmap = plt.get_cmap('jet')) #node_color = values)
    plt.show()


if __name__=="__main__":
        
#    print (sys.argv)
    input_file = "network_option_a.txt"
    network = createNetwork(input_file)
    drawNetwork(network)
