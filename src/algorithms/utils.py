from graph import *

def depth_first_search(graph, s, t):
    for node in graph.nodes():
        node.visited = False
    path = Path(s)
    if not _dfs(graph, s, t, path):
        path = None
    for node in graph.nodes():
        del node.visited
    return path

def _dfs(graph, cur, t, path):
    cur.visited = True
    for edge in cur.outgoing_edges():
        n = edge.destination()
        if not n.visited:
            path.append(edge, n)
            if n == t or _dfs(graph, n, t, path): 
                return True
            path.pop()
    return False

def has_cycles(graph):
    """
    Returns a list of path objects, each making up a cycle in the input graph.
    If there is no path and empty list will be returned.
    """
    if graph.empty():
        return []
    for node in graph.nodes():
        node.color = "white"
    res = _dfs_cycle(graph, graph.nodes()[0], Path(graph.nodes()[0]))
    for node in graph.nodes():
        del node.color
    return res


def _dfs_cycle(graph, cur, path):
    cur.color = "grey"
    for edge in cur.outgoing_edges():
        n = edge.destination()
        if n.color == "white":
            path.append(edge, n)
            if _dfs_cycle(graph, n, path):
                return True
            path.pop()
        elif n.color == "grey":
            return True
    cur.color = "black"
    return False
