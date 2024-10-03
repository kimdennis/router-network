from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt


class RouterNetwork:
    nx_graph = nx.Graph()
    fig = plt.figure(figsize=(12, 12))
    ax = plt.subplot(111)

    def __init__(self):
        print("initializing network")
        self.ax.set_title('Graph test', fontsize=10)

    def build_network(self):
        # reading file and formatting inputs
        f = open("data.txt", "r")
        nodes = f.readline().rstrip("\n").split(" ")
        start_edges = f.readline().rstrip("\n").split(" ")
        end_edges = f.readline().rstrip("\n").split(" ")
        edge_weights = f.readline().rstrip("\n").split(" ")

        # adding nodes
        self.nx_graph.add_nodes_from(nodes)

        # processing and adding edges
        edges = list(zip(start_edges, end_edges, edge_weights))

        for edge in list(edges):
            self.nx_graph.add_edge(edge[0], edge[1], weight=float(edge[2]))



    def render_network(self):
        pos = nx.spring_layout(self.nx_graph)  # setting up graph layout

        # setting up edge and node labels
        nx.draw(self.nx_graph, pos, with_labels=True, node_size=1500, node_color='white', font_size=8, font_weight='bold')

        # putting edges into dictionary, so we can display them using networkx
        edges = dict([((startn, endn), w['weight'])
                            for startn, endn, w in self.nx_graph.edges(data=True)])

        nx.draw_networkx_edge_labels(self.nx_graph, pos, edge_labels=edges, font_color='red', font_size=15, font_weight='bold')
        nx.draw_networkx(self.nx_graph, pos, font_color='black', font_size=15, font_weight='bold')


        plt.savefig("Graph.png", format="PNG")


n = RouterNetwork()
n.build_network()
n.render_network()