from RouterNetwork import *

def translate_to_matrix(nodes, start_nodes, end_nodes, edge_weights):
  """ 
  Use the information from the global lists (nodes, start_nodes, end_nodes and edge_weights)
  Translate the graph to a matrix where the name of nodes are converted from letters to indexes of the matrix
  Output: returns a matrix that represent the graph
  """
  # creating a matrix (size: n x n) that represents the graph, where n = # of nodes
  translated_graph = []
  for i in range(len(nodes)):
    row = [0] * len(nodes)
    translated_graph.append(row)

  # go through each edges and put it in the matrix translated_graph
  for i in range(len(start_nodes)):
    starting_node = start_nodes[i]
    ending_node = end_nodes[i]
    translated_graph[nodes.index(starting_node)][nodes.index(
      ending_node)] = edge_weights[i]
    translated_graph[nodes.index(ending_node)][nodes.index(
      starting_node)] = edge_weights[i]
  return translated_graph

def translate_from_number(numbers, nodes):
  """
  Translate a list of indexes (of the matrix) back to the name of the nodes
  Input: a list of indexes that was assigned to nodes
  Output: returns a list of node names that was translated from indexes to letters
  """
  translated_nodes = []
  for n in numbers:
    translated_nodes.append(nodes[n])
  return translated_nodes

def find_number_isolated_nodes(nodes, start_nodes, end_nodes):
  """
  Goes through nodes of the matrix and find the number of isolated nodes in the matrix
  Output: return a number of isolated nodes
  """
  isolated_nodes = 0
  for n in nodes:
    if n not in start_nodes and n not in end_nodes:
      isolated_nodes += 1
  return isolated_nodes

def relax(dist_to, edge_to, graph, node):
  """
  A helper function for dijkstra and this function updates the edges in edge_to if necessary
  Input: graph -> a matrix, node -> an index
  """
  for i in range(len(graph)):
    if int(graph[node][i]) > 0:
      cost = dist_to[node] + int(graph[node][i])
      if dist_to[i] > cost:
        dist_to[i] = cost
        edge_to[i] = node
  return (dist_to, edge_to)

def min_distance(dist_to, visited):
  """
  A helper function for dijkstra and this function finds an edge to an unvisited node with the minimum cost
  Input: visited -> a list of visited nodes (list of indexes)
  Output: returns an index of an unvisited node that connects to the min cost edge
  """
  min = 100000000000 # infinity
  min_index = 0
  for i in range(len(dist_to)):
    if dist_to[i] < min and i not in visited:
      min = dist_to[i]
      min_index = i
  return min_index

def dijkstra(source_node, graph, nodes, start_nodes, end_nodes, algo_steps):
  """
  Find the shortest path to all nodes using dijkstra algorithm
  Input: graph -> a matrix, source_node -> an index representing the source node
  Output: return a forwarding table
  """
  # dist_to = a list of the length shortest path to each nodes (index # = node)
  # initalize each length with 100000000000 (infinity)
  dist_to = [100000000000] * len(graph)
  dist_to[source_node] = 0

  # visited = list of nodes that are visited
  visited = [source_node]

  # edge_to = a list of the last node on the shortest path (dist_to) to each nodes (index # = node)
  edge_to = [-1] * len(graph)

  # path = result path of the matrix (graph)
  path = []
  for i in range(len(graph)):
    row = [0] * len(graph[i])
    path.append(row)

  # start the algorithim on the source node
  node = source_node
  while len(visited) != (len(nodes) - find_number_isolated_nodes(nodes, start_nodes, end_nodes)):
    dist_to, edge_to = relax(dist_to, edge_to, graph, node)
    # find the mininum distance in dist_to to add an edge to path[][]
    node = min_distance(dist_to, visited)

    # record the selected edge to the path
    index = edge_to[node]
    path[node][index] = graph[node][index]
    path[index][node] = graph[node][index]
    visited.append(node)
    algo_steps.put([translate_from_number([node,index], nodes)])
  return edge_to

def shortestPath(routerNetwork, source, destination):
  """
  Gets shortest path by following the forwarding table from the destination node backwards until it gets to the source node
  Input: source and destination nodes (node names)
  Output: return the path (in nodes names)
  """
  nodes, start_nodes, end_nodes, edge_weights = routerNetwork.get_graph_info()
  algo_steps = routerNetwork.algo_steps
  
  a_matrix = translate_to_matrix(nodes, start_nodes, end_nodes, edge_weights)
  # get the indexes of matrix that represents the source and destination nodes 
  source_number = nodes.index(source)
  dest_number = nodes.index(destination)
  
  forwardTable = dijkstra(source_number, a_matrix, nodes, start_nodes, end_nodes, algo_steps)

  # find the shortest path using the forwarding table
  path = [dest_number]
  list_path = []
  while path[0] != source_number:
    if path[0] == -1:
      return "No Path"  
    list_path.append(translate_from_number([path[0],forwardTable[path[0]]], nodes))
    path = [forwardTable[path[0]]] + path
  algo_steps.put(list_path)
  return (translate_from_number(path, nodes))
