import string, queue
from dijkstra import *

# from NetworkGUI import load_graph
import networkx as nx
import matplotlib.pyplot as plt


class RouterNetwork:
    nx_graph = nx.Graph()
    fig = plt.figure(figsize=(12, 12))
    ax = plt.subplot(111)
    origin = ""
    destination = ""
    # Holds the edges updated for each iteration in a list of lists.
    # The last item contains the final path.
    algo_steps = queue.Queue()

    colours = {
        'visited': '#FF4760',  # red
        'unvisited': 'black',
        'origin': '#5DB626',  # green
        'shortest path': '#5DB626',  # green
        'destination': '#527CA3',  # dark blue
        'default': '#87C4FD'  # light blue
    }

    def __init__(self):
        print("initializing network")
        # self.ax.set_title('Graph test', fontsize=10)

    def get_nodes(self):
        return list(self.nx_graph.nodes)

    def build_network(self):
        """
        Builds the network from a data.txt file.
        :return: None
        """
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
            self.nx_graph.add_edge(edge[0], edge[1], weight=int(edge[2]), color=self.colours['unvisited'])

    def render_network(self):
        """
        Updates the image of the graph
        :return: None
        """

        pos = nx.planar_layout(self.nx_graph)  # setting up graph layout (or try spring_layout)

        # setting up edge and node labels

        # putting edges into dictionary, so we can display them using networkx
        edges = dict([((startn, endn), w['weight'])
                            for startn, endn, w in self.nx_graph.edges(data=True)])

        # each edge and node colour in a list to be referenced when displaying graph
        list_colours = [self.nx_graph[u][v]['color'] for u, v in edges]

        node_colours = []
        for n in self.get_nodes():
            if n == self.origin: node_colours.append(self.colours['origin'])
            elif n == self.destination: node_colours.append(self.colours['destination'])
            else: node_colours.append(self.colours['default'])

        # drawing graph
        nx.draw_networkx(self.nx_graph, pos, node_size=1500, node_color=node_colours, edge_color=list_colours, width=5, font_color='black', font_size=15, font_weight='bold')
        nx.draw_networkx_edge_labels(self.nx_graph, pos, edge_labels=edges, font_color='#CB3636', font_size=15,
                                     font_weight='bold')

        plt.savefig("Graph.png", format="PNG")
        plt.clf()  # clear the graph to avoid overlap

    def add_router(self):
        """
        Adds a router to the network. Each router is named a letter, if there are too many routers, return False
        :return: whether add_router was successful
        """
        nodes = self.get_nodes()

        # find a letter not used in the graph, then update the graph
        for letter in string.ascii_uppercase:
            if letter not in nodes:
                self.nx_graph.add_node(letter)
                self.render_network()
                return True
        return False

    def add_connection(self, n1: string, n2: string, w: int):
        """
        Adds a connection between routers n1 and n2 to the network. If the connection already exists, update the
        existing connection with the given weight. If given an invalid weight or set of nodes, returns False.
        :param n1: node 1
        :param n2: node 2
        :param w: weight
        :return: Boolean: Whether adding the connection was successful
        """

        if n1 != n2 and w > 0:
            self.nx_graph.add_edge(n1, n2, weight=w, color=self.colours['unvisited'])
            self.render_network()
            return True
        return False

    def remove_connection(self, n1, n2):
        """
        Remove an edge in the graph.
        :param n1: Connecting node
        :param n2: Connecting node
        :return bool: Whether edge was successfully removed
        """
        try:
            self.nx_graph.remove_edge(n1, n2)
            self.render_network()
            return True
        except nx.NetworkXError:
            return False

    def get_str_edges(self):
        """
        Returns the edges as a string.
        :return String:
        """
        str = ''
        for e in self.nx_graph.edges(data=True):
            str = str + '\n({n1}, {n2})   weight: {w}'.format(
                n1=e[0], n2=e[1], w=e[2]['weight']
            )
        return str

    def get_graph_info(self):
        """
        Takes networkx graph information and returns a list of lists to help with matrix conversion
        :return: list of lists: [nodes, start_nodes, end_nodes, edge_weights]
        """
        nodes = self.get_nodes()
        start_nodes = []
        end_nodes = []
        edge_weights = []

        for e in self.nx_graph.edges(data=True):
            start_nodes.append(e[0])
            end_nodes.append(e[1])
            edge_weights.append(e[2]["weight"])

        return [nodes, start_nodes, end_nodes, edge_weights]

    def simulate(self, origin, destination, algo_type):
        """
        Begins simulation of the respective routing algorithm.
        :param origin: Origin node
        :param destination: Destination node
        :param algo_type: Routing algorithm
        :return String: Resulting shortest path
        """
        # reset colours in graph
        for e in self.nx_graph.edges(data=True):
            self.nx_graph.add_edge(e[0], e[1], color=self.colours['unvisited'])

        # clear algo_steps
        while not self.algo_steps.empty():
            self.algo_steps.get()

        self.origin = origin
        self.destination = destination
        self.render_network()

        if algo_type == "centralized":
            # call djiktras
            path = shortestPath(self, origin, destination)
            print("beginning centralized calc")
            return path
        else:
            # call belman ford
            print("beginning de-centralized calc")

    def iterate(self):
        """
        Iterates through each step of the algorithm in algo_steps and updates the graph accordingly.
        :return bool: Whether there are more steps in iterations
        """
        if self.algo_steps.empty():
            return False

        edges_visited = self.algo_steps.get()

        # for the last element, display edges for final path with a different colour

        if self.algo_steps.qsize() == 0:
            for e in edges_visited:
                self.nx_graph.add_edge(e[0], e[1], color=self.colours['shortest path'])
            self.render_network()
        else:
            for e in edges_visited:
                self.nx_graph.add_edge(e[0], e[1], color=self.colours['visited'])
            self.render_network()

        return True


