from graph import *

def _get_active_node(graph, s, t):
    for node in graph.nodes():
        if not node is t and not node is s and node.overrun > 0:
            return node
    return None

def _has_active_node(graph, s, t):
    return True if not _get_active_node(graph, s, t) is None else False

def _push(node):
    success = False
    for edge in node.outgoing_edges():
        neighbor = edge.destination()
        if not node.dist == neighbor.dist + 1 or edge.load == edge.capacity:
            continue
        success = True
        reverse_edge = node.edge_from(neighbor)
        push = min(edge.capacity - edge.load, node.overrun)
        edge.load         += push
        reverse_edge.load -= push
        neighbor.overrun  += push
        node.overrun      -= push
        if node.overrun == 0:
            break
    return success

def _relabel(node):
    min_dist = None
    for edge in node.outgoing_edges():
        if edge.load == edge.capacity:
            continue
        if min_dist is None or edge.destination().dist < min_dist:
            min_dist = edge.destination().dist

    node.dist = min_dist + 1
        

def solve_max_flow_pl(graph, s, t):
    for node in graph.nodes():
        node.dist = 0
        node.overrun = 0
    for edge in graph.edges():
        edge.load = 0
        if not graph.has_reverse_edge(edge):
            graph.add_edge(edge.destination(), edge.source(), {"capacity" : 0, "load" : 0, "tmp" : True})
    s.dist = len(graph.nodes())
    for edge in s.outgoing_edges():
        edge.load = edge.capacity
        edge.destination().overrun = edge.load
        edge.destination().edge_to(s).load = -edge.capacity
    while _has_active_node(graph, s, t):
        node = _get_active_node(graph, s, t)
        if not _push(node):
            _relabel(node)
    for edge in graph.edges():
        if hasattr(edge, "tmp"):
            graph.remove_edge(edge)

def conclusion(graph, team):
    flow = 0
    for edge in graph.edges():
        if "SINK" in edge._node2.name():
            flow = flow+edge.flow()
    return flow
