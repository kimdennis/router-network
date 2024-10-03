from dijkstra import *

#for item in translate_to_matrix():
#    print(item)

# nodes = [0, 1,2,3,4,5,6,7]
# start_edges = [0,0,0,1,1,2,2,2,2,3,3,3,3,4,4,5,5,5,6,6,7,7]
# end_edges = [2,3,4,2,3,0,1,5,6,0,1,5,7,0,6,2,3,7,2,4,3,5]
# edge_weights = [3,2,2,6,7,3,6,7,6,2,7,1,9,2,9,7,1,1,6,9,9,1]

# nodes = ["C", "B","D", "E","W", "A","F"]
# start_edges = ["A", "A", "B", "B", "B", "C", "D", "B"]
# end_edges = ["B", "D", "D", "E", "C", "E", "E", "F"]
# edge_weights = [6, 1, 2, 2, 5, 5, 1, 3]

print("----")
        # 0  1  2  3  4  5  6  7
graph = [[0, 0, 3, 2, 2, 0, 0, 0], # 0
         [0, 0, 6, 7, 0, 0, 0, 0], # 1
         [3, 6, 0, 0, 0, 7, 6, 0], # 2
         [2, 7, 0, 0, 0, 1, 0, 9], # 3
         [2, 0, 0, 0, 0, 0, 9, 0], # 4
         [0, 0, 7, 1, 0, 0, 0, 1], # 5
         [0, 0, 6, 0, 9, 0, 0, 0], # 6
         [0, 0, 0, 9, 0, 1, 0, 0]] # 7

        # 0  1  2  3  4  5  6  7
grap2 = [[0, 8, 0, 0, 7, 0, 0, 0], # 0
         [8, 0, 6, 1, 0, 4, 0, 0], # 1
         [0, 6, 0, 0, 0, 1, 0, 0], # 2
         [0, 1, 0, 0, 0, 0, 0, 0], # 3
         [7, 0, 0, 0, 0, 0, 0, 0], # 4
         [0, 4, 1, 0, 0, 0, 0, 0], # 5
         [0, 0, 0, 0, 0, 0, 0, 0], # 6
         [0, 0, 0, 0, 0, 0, 0, 0]] # 7

# test dijkstra algorithm
routerNetwork = RouterNetwork()
routerNetwork.build_network()
routerNetwork.render_network()
print(shortestPath(routerNetwork,"C","A"))