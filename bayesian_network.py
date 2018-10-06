import networkx as nx
import matplotlib.pyplot as plt
import sys

class Node():

    def __init__(self, name, prob):
        self.name = name
        self.prob = prob




network = nx.DiGraph()


#pos = {"A": (1, 2),
 #      "B": (2, 3),
  #     "C": (3, 4)}
pos = nx.spring_layout(G)

values = [val_map.get(node, .25) for node in G.nodes]
nx.draw_networkx_labels(G, pos, val_map)
nx.draw(G, cmap = plt.get_cmap('jet'), node_color = values)
plt.show()

print ("Done")



if __name__=="__main__":
        
