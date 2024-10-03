from tkinter import *
from RouterNetwork import *

import tkinter as tk
from PIL import Image, ImageTk

# Create main window
root = tk.Toplevel()
root.geometry('1200x600')
# root.configure(bg='#9ea3b5')
root.title('CPS706 PROJECT')
root.resizable(False, False)


##### FUNCTIONS #####

def add_router(dropdowns_list, dropdowns_values, routerNetwork, image_frame):
    """
    Adds a router to the network and updates the image of the network
    :param routerNetwork: RouterNetwork object containing the network
    :param image_frame: Frame of the image
    :return: None
    """
    print("add router")
    if routerNetwork.add_router():
        load_graph(image_frame)
        update_dropdowns(dropdowns_list, dropdowns_values, routerNetwork)
    else:
        print("Too many nodes")


def add_edge(edges_text, from_node, to_node, cost, routerNetwork, image_frame):
    """
    Adds an edge to the network and loads the graph image.
    """

    print("adding edge")

    # check if input is valid
    if cost.get().isdigit() and int(cost.get()) <= 0:
        print("Edge cost must be over 0")
    elif from_node.get() == to_node.get():
        print("Source node and destination node must be different")
    elif not cost.get().isdigit():
        print("Edge cost must be one number")
    elif cost.get().isdigit() and (from_node.get() != to_node.get()):
        routerNetwork.add_connection(from_node.get(), to_node.get(), int(cost.get()))
        edges_text.set(routerNetwork.get_str_edges())
        load_graph(image_frame)
    else:
        print("bad edge input")


def remove_edge(edges_text, from_node, to_node, cost, routerNetwork, image_frame):
    """
    Removes an edge from the graph and re-displays the graph.
    """
    print("removing edge")

    # check if input is valid
    if routerNetwork.remove_connection(from_node.get(), to_node.get()):
        edges_text.set(routerNetwork.get_str_edges())
        load_graph(image_frame)
    else:
        print("bad edge input")


def begin_simulation(network_path, current_step, origin, destination, algo_type, routerNetwork, image_frame):
    """
    Initializes graph simulation for respective routing algorithm.
    """
    print("beginning simulation")

    algo = ''

    if algo_type.get() == "Centralized (Dijkstra)":
        algo = 'centralized'
    else:
        algo = 'decentralized'

    current_step.set('0')
    origin_value = origin.get()
    destination_value = destination.get()

    if (origin_value != destination_value) and (origin_value != "") and (destination_value != ""):
        # routerNetwork.dummy_visited_path()
        network_path.set(routerNetwork.simulate(origin_value, destination_value, algo))
        load_graph(image_frame)
    else:
        print("bad origin or destination")


def next_step(current_step, routerNetwork, image_frame):
    """
    Displays the next step in the current routing algorithm for the network.
    """
    if routerNetwork.iterate():
        load_graph(image_frame)
        current_step.set(int(current_step.get()) + 1)
    else:
        print("no more iterations")


def load_graph(image_frame):
    """
    Loads the graph image with the updated Graph.png file
    :param image_frame:
    :return: None
    """
    print("load graph")
    # Load sample image
    image2 = Image.open("Graph.png")
    image2 = image2.crop((150, 140, 1090, 1080)).resize((400, 400))

    # Convert the image to a Tkinter PhotoImage
    photo2 = ImageTk.PhotoImage(image2, master=root)

    image_frame.configure(image=photo2)
    image_frame.image = photo2


def update_dropdowns(dropdowns_list, dropdowns_values, routerNetwork):
    """
    Updates each dropdowm menu containing nodes with the updated list of nodes.
    :return: None
    """

    # clear menus
    for d in dropdowns_list:
        d["menu"].delete(0, "end")

    # clear variables in menus
    for v in dropdowns_values:
        v.set('')

    # add each node to the menus
    for item in routerNetwork.get_nodes():
        dropdowns_list[0]["menu"].add_command(
            label=item,
            command=lambda value=item: dropdowns_values[0].set(value)
        )
        dropdowns_list[1]["menu"].add_command(
            label=item,
            command=lambda value=item: dropdowns_values[1].set(value)
        )
        dropdowns_list[2]["menu"].add_command(
            label=item,
            command=lambda value=item: dropdowns_values[2].set(value)
        )
        dropdowns_list[3]["menu"].add_command(
            label=item,
            command=lambda value=item: dropdowns_values[3].set(value)
        )


def main():
    routerNetwork = RouterNetwork()
    routerNetwork.build_network()
    routerNetwork.render_network()

    # Create main window
    root.geometry('1200x600')
    root.title('CPS706 PROJECT')
    root.resizable(False, False)

    # Create a 'Step' header to show that step the graph is in

    step_label = tk.Label(root, text='Step:', font="Bahnschrift")
    step_label.grid(row=0, column=2, sticky=tk.E)

    current_step = tk.StringVar(value='0')
    num_label = tk.Label(root, textvariable=current_step, font="Bahnschrift")
    num_label.grid(row=0, column=3)

    # Load sample image
    image = Image.open("Graph.png")
    image = image.crop((150, 140, 1090, 1080)).resize((400, 400))

    # Convert the image to a Tkinter PhotoImage
    photo = ImageTk.PhotoImage(image, master=root)

    # Create image frame
    image_frame = tk.Label(root, image=photo)
    image_frame.image = photo
    image_frame.grid(row=1, column=2, rowspan=6, padx=10, pady=10)  # Set the position of the image frame

    # Create dropdown menu for centralized/decentralized selection
    tk.Label(root, text='Network Type: ', font="Bahnschrift").grid(row=0, column=0, sticky=tk.W)
    network_type = tk.StringVar(value='Centralized (Dijkstra)')
    network_type_dropdown = tk.OptionMenu(root, network_type, 'Centralized (Dijkstra)', 'Decentralized (Bellman Ford)')
    network_type_dropdown.grid(row=0, column=1, sticky=tk.W)

    # Create Add Router button, lambda is used so the command doesnt activate when loading the button
    tk.Button(root, text='Add Router',
              command=lambda: add_router(dropdowns_list, dropdowns_values, routerNetwork, image_frame),
              font="Bahnschrift", bg="red", fg="white", activebackground="red", activeforeground="black", borderwidth=2, relief=tk.RAISED, cursor="hand2").grid(row=1,
                                                                                                             column=0,
                                                                                                             sticky=tk.W)

    # Create frame for edges table
    edges_frame = tk.Frame(root, relief='solid', borderwidth=1)
    edges_frame.grid(row=2, column=0)

    # Create header for edges table
    tk.Label(edges_frame, text='Add or Remove an Edge', font="Bahnschrift").grid(row=0, column=0, columnspan=4)

    # Create dropdowns for edges
    tk.Label(edges_frame, text='From:').grid(row=1, column=0, sticky=tk.W)
    from_input = tk.StringVar(value='A')
    from_input_dropdown = tk.OptionMenu(edges_frame, from_input, *routerNetwork.get_nodes())
    from_input_dropdown.grid(row=1, column=1, sticky=tk.W)

    tk.Label(edges_frame, text='To:').grid(row=1, column=2)
    to_input = tk.StringVar(value='A')
    to_input_dropdown = tk.OptionMenu(edges_frame, to_input, *routerNetwork.get_nodes())
    to_input_dropdown.grid(row=1, column=3, sticky=tk.W)

    # Create Origin Input dropdown
    tk.Label(root, text='Origin Router: ', font="Bahnschrift").grid(row=7, column=0)
    origin_input = tk.StringVar(value='A')
    origin_input_dropdown = tk.OptionMenu(root, origin_input, *routerNetwork.get_nodes())
    origin_input_dropdown.grid(row=7, column=1)

    # Create Destination Input dropdown
    tk.Label(root, text='Destination Router: ', font="Bahnschrift").grid(row=8, column=0)
    destination_input = tk.StringVar(value='A')
    destination_input_dropdown = tk.OptionMenu(root, destination_input, *routerNetwork.get_nodes())
    destination_input_dropdown.grid(row=8, column=1)

    # Package dropdowns
    dropdowns_list = [from_input_dropdown, to_input_dropdown, origin_input_dropdown, destination_input_dropdown]
    dropdowns_values = [from_input, to_input, origin_input, destination_input]

    tk.Label(edges_frame, text='Cost:').grid(row=2, column=0, sticky=tk.W)
    cost_input = tk.Entry(edges_frame)
    cost_input.grid(row=2, column=1, sticky=tk.W)

    tk.Button(edges_frame, text='Add edge',
              command=lambda: add_edge(edges_text, from_input, to_input, cost_input, routerNetwork, image_frame), bg="#C0C0C0", fg="#9c0505", activebackground="red", activeforeground="black", borderwidth=2, relief=tk.RAISED, cursor="hand2").grid(
        row=2,
        column=2)

    tk.Button(edges_frame, text='Remove edge',
              command=lambda: remove_edge(edges_text, from_input, to_input, cost_input, routerNetwork,
                                          image_frame), bg="#C0C0C0", fg="#9c0505", activebackground="red", activeforeground="black", borderwidth=2, relief=tk.RAISED, cursor="hand2").grid(row=2, column=3, sticky=tk.W)

    # Edges info
    tk.Label(edges_frame, text="\nEdges:", font="Bahnschrift").grid(row=3, column=0, columnspan=4, sticky=tk.W)
    edges_text = tk.StringVar(value=routerNetwork.get_str_edges())
    edges_info_label = tk.Label(edges_frame, textvariable=edges_text)
    edges_info_label.grid(row=4, column=0, columnspan=4, sticky=tk.W)

    # Create a Path label in row 0 column 0
    path_label = tk.Label(root, text="Path:", font="Bahnschrift")
    path_label.grid(row=7, column=2)

    # Text output for path
    network_path_text = tk.StringVar(value='')
    network_path = tk.Label(root, textvariable=network_path_text, font="Bahnschrift", height=1, width=30)
    network_path.grid(row=7, column=3)

    # Create a Next Step button
    button = tk.Button(root, text="Next Step", command=lambda: next_step(current_step, routerNetwork, image_frame), font="Bahnschrift", bg="red", fg="white", activebackground="red", activeforeground="black", borderwidth=2, relief=tk.RAISED, cursor="hand2")
    button.grid(row=8, column=2)

    # Create Begin Simulation button
    tk.Button(root, text='Begin Simulation', command=lambda: begin_simulation(
        network_path_text, current_step, origin_input, destination_input, network_type, routerNetwork,
        image_frame), font="Bahnschrift", bg="red", fg="white", activebackground="red", activeforeground="black", borderwidth=2, relief=tk.RAISED, cursor="hand2").grid(row=9, column=0)

    root.mainloop()


if __name__ == "__main__":
    main()
