from math import sqrt
import sys
from typing import Dict, List, Set, Tuple
from priority_queue import PriorityQueue


'''my import'''
from L2_adjacency_list_graph import AdjacencyListGraph
from graph_base_class import Edge

'''my note'''
# Ticket to Ride dataeset is an undirected graph
# All others are directed graphs. Make sure you account for that in your pathfinder class.

# You do not need to change this class.  It is used as the return type for get_minimum_path
class RouteInfo:
    def __init__(self, 
                 route: List[Tuple[str, str]], # list of tuples of friendly names for the start and destination cities
                 route_ids: List[Tuple[int, int]], # list of tuples of ids for the start and destination cities
                 cost: int) -> None: # the total cost of the route from start to destination
        self.route = route
        self.route_ids = route_ids
        self.cost = cost

# TO|DO: Implement the methods on the PathFinder class using an underlying graph representation
# of your choice. Feel free to use your graph classes from the practice exercises; copy the appropriate
# files into your project and import the classes at the top of this file.
class PathFinder:
    def __init__(self) -> None:
        self.graph = AdjacencyListGraph(True)

    # TO|DO: adds an edge to the graph, using a the id of the start node and id of the finish node
    def add_edge(self, start_id: int, finish_id:int , cost: float) -> None:
        self.graph.add_edge(start_id, finish_id, cost)

    # TO|DO: adds a node to the graph, passing in the id, friendly name, and location of the node.
    # location is a tuple with the x and y coordinates of the location
    def add_node(self, id: int, name: str, location: Tuple[float, float]) -> None:
        self.graph.add_node(id, name, location)


    # TODO: calculates the minimum path using the id of the start city and id of the destination city, using A*
    # Returns a RouteInfo object that contains the edges for the route.  See RouteInfo above for attributes
    # Note: This implementation should use A*.  Tests that should pass 
    def get_minimum_path(self, start_city_id: int, destination_id:int ) -> RouteInfo:

        p_queue = PriorityQueue() # NodeID : Total Cost
        prev_nodes = dict() # NodeID : PrevNodeID
        visited_nodes = set() # NodeIDs of prev cur_nodes
        cost_to = {start_city_id : 0, destination_id : sys.maxsize} # NodeID : cost to get there (no heuristic)
        dist_heuristics = dict() # NodeID : distance heuristic
        
        p_queue.enqueue(0, start_city_id)

        while not p_queue.is_empty():
            if cost_to[destination_id] is not sys.maxsize:
                break
            
            cur_node = p_queue.dequeue()
            visited_nodes.add(cur_node)

            final_loc = self.graph.id_to_location[destination_id]
            for edge in self.graph.get_edges(cur_node):
                
                neighbor = edge.finish

                if edge.finish not in visited_nodes:
                    
                    cur_loc = self.graph.id_to_location[neighbor]
                    # √ (x2 - x1)2 + (y2 - y1)2
                    distance = sqrt(pow(final_loc[0] - cur_loc[0], 2) + pow(final_loc[1] - cur_loc[1], 2))
                    dist_heuristics[neighbor] = distance
                    
                    if neighbor not in cost_to.keys() or edge.weight + cost_to[cur_node] < cost_to[neighbor]:
                        cost_to[neighbor] = edge.weight + cost_to[cur_node]
                        prev_nodes[neighbor] = cur_node

                        priority = cost_to[neighbor] + dist_heuristics[neighbor]
                        p_queue.enqueue(priority, neighbor)

        
        route: List[Tuple[str, str]] = []
        route_ids: List[Tuple[int, int]] = []
        cost: int = cost_to[destination_id]
        
        cur_node = destination_id
        while cur_node is not start_city_id:
            cur_node_name = self.graph.id_to_name[cur_node]
            prev_node = prev_nodes[cur_node]
            prev_node_name = self.graph.id_to_name[prev_node]

            route_ids.insert(0, (prev_node, cur_node))
            route.insert(0, (prev_node_name, cur_node_name))

            cur_node = prev_node
        

        return RouteInfo(route, route_ids, cost)