from graph import *
from .utils import depth_first_search


def solve_max_flow_ff(graph, s, t):
    while True:
        # Find a path between source and sink node
        path = depth_first_search(graph, s, t)
        
        if path is None:
            break
        # find minimum capacity on the current path
        min_capacity = None
        for edge in path.edges():
            if min_capacity is None or edge.capacity < min_capacity:
                min_capacity = edge.capacity

        # subtract min_capacity from all edges and add return edge
        for edge in path.edges():
            edge.capacity -= min_capacity
            if not graph.has_reverse_edge(edge):
                # Add a temporary edge from destination to source (Reverse Edge)
                graph.add_edge(edge.destination(), edge.source(), {"capacity" : min_capacity, "tmp" : True})
            else: 
                graph.get_reverse_edge(edge).capacity += min_capacity
            # If edge capacity is full, simply remove the edge from graph
            if edge.capacity == 0:
                graph.remove_edge(edge)
    for edge in graph.edges():
        # Find Temporary Edges (Reverse Edges)
        if hasattr(edge, "tmp"):
            if graph.has_reverse_edge(edge):
                graph.get_reverse_edge(edge).load = edge.capacity
            else:
                graph.add_edge(edge.destination(), edge.source(), {"load" : edge.capacity})
            # Remove particular temporary edge.
            graph.remove_edge(edge)
    for edge in graph.edges():
        if len(vars(edge)) == 4:
            vars(edge)['capacity'] += vars(edge)['load']

def conclusion(graph):
    flow = 0
    for edge in graph.edges():
        if "SINK" in edge._node2.name():
            flow = flow+edge.flow()

    return flow

