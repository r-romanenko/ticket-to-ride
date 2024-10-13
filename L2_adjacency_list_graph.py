from typing import Set, List, Dict, Tuple # I added tuple
from graph_base_class import Edge, GraphBaseClass


# Implement Graph using an adjacency list as the underlying representation
class AdjacencyListGraph(GraphBaseClass):

    # if is_directed is true, this should be a directed graph.  If false, it's an undirected graph
    # Make sure your implementation accounts for node order on an edge for directed and is neutral for undirected
    # super sets a property self.is_directed to the parameter value
    def __init__(self, is_directed:bool) -> None:
        self.nodes:Dict[Set] = dict()
        self.id_to_name = dict()
        self.name_to_id = dict()
        self.id_to_location = dict()
        super().__init__(is_directed)
    
    # Adds a node idd "id" to the graph.
    def add_node(self, id: int, name: str, location: Tuple[float, float]) -> None:
        self.nodes.setdefault(id, set())
        self.id_to_name[id] = name
        self.name_to_id[name] = id
        self.id_to_location[id] = location

    # Removes the node idd "id" and all arcs connected to it
    def remove_node(self, id:any) -> None:
        self.nodes.pop(id) # destroy node

        # destroy associated arcs
        for node in self.nodes:
            for edge in self.nodes[node]:
                if edge.start == id or edge.finish == id:
                    self.nodes[node].remove(edge)
                    break
    
    # Gets a set of the ids of all nodes in the graph
    def get_nodes(self) -> Set[any]:
        ids:Set = set()
        keys = self.nodes.keys()
        for key in keys:
            ids.add(key)
        return ids

    # Returns True if the node id1 is connected to the node id2 and False otherwise
    def is_connected(self, id1:any, id2:any) -> None:
        # return id2 in self.nodes[id1]
        edges = self.nodes[id1]
        for edge in edges:
            if edge.finish is id2:
                return True
        return False

    # Adds an edge from node start to node finish with the weight specified
    def add_edge(self, start:any, finish:any, weight:int) -> None:
        # add an Edge to the set of the node you're adding the arc to
        self.nodes[start].add(Edge(start, finish, weight))

        # add it the other way if it's not directed
        if not self.is_directed:
            self.nodes[finish].add(Edge(finish, start, weight))

    # Returns a set of the ids of nodes adjacent to the given node (i.e. there's an arc from the node to the neighbor)
    def get_neighbors(self, id:str) -> Set[any]:
        neighbors:Set = set()
        for edge in self.nodes[id]:
            neighbors.add(edge.finish)
        return neighbors
    
    # Gets a set of edges leading out of the given node
    def get_edges(self, id:str) -> Set[Edge]:
        return self.nodes[id]