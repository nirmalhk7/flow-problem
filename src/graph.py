from collections import OrderedDict          # use ordered dicts to preserve element ordering     

class Graph:
    def __init__(self):
        self._nodes = OrderedDict()
        self._edges = []
    def nodes(self):
        """
        Returns all nodes in this graph.
        """
        return list(self._nodes.values())
    def edges(self):
        """
        Returns all edges in this graph.
        """
        return list(self._edges)
    def empty(self):
        return False if self._nodes else True
    def add_node(self, name, data = None):
        if self.has_node(name):
            raise ValueError("Node %s already exists" % name)
        self._nodes[name] = Node(name, data)
        return self._nodes[name]

    def add_nodes(self, l):
        ret = []
        for name in l:
            ret.append(self.add_node(name))
        return ret

    def remove_node(self, n):
        node = self._node_lookup([n])
        for edge in self.edges():
            if node in edge.nodes():
                self.remove_edge(edge)
        del self._nodes[node.name()]

    def add_edge(self, src, dst, data = None): #adds directed edge
        srcnode, dstnode = self._node_lookup([src, dst])
        if srcnode is None or dstnode is None:
            raise ValueError("No such node in this graph")
        edge = Edge(srcnode, dstnode, data)
        self._edges.append(edge)
        srcnode._add_outgoing_edge(edge)
        dstnode._add_incoming_edge(edge)
        return edge

    def remove_edge(self, edge):
        if not edge in self._edges:
            return
        self._edges.remove(edge)
        if edge.is_directed():
            edge.source()._remove_outgoing_edge(edge)
            edge.destination()._remove_incoming_edge(edge)
        else:
            for node in edge.nodes():
                node._remove_undirected_edge(edge)

    def get_node(self, name):
        return self._nodes.get(name)

    def has_node(self, name):
        return name in self._nodes


    def get_reverse_edge(self, edge):
        return edge.destination().edge_to(edge.source())

    def has_reverse_edge(self, edge):
        return self.get_reverse_edge(edge) is not None
    def _node_lookup(self, l):
        """
        Returns the graphs node object or None for the given node/node name or every
        element in the given list of nodes/node names.
        """
        res = []
        for obj in l:
            if obj in self.nodes():
                res.append(obj)
            else:
                res.append(self._nodes.get(obj))

        return res if not len(res) == 1 else res[0]

    def __str__(self):
        res = "Nodes:\n"
        for node in self._nodes.values():
            res += str(node)

        res += "Edges:\n"
        for edge in self._edges:
            res += str(edge)

        return res


class Node:
    def __init__(self, name, data = None):
        self._name = name
        self._outgoing_edges = OrderedDict()
        self._incoming_edges = OrderedDict()
        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)

    def _add_outgoing_edge(self, edge):
        self._outgoing_edges[edge.destination()] = edge

    def _add_incoming_edge(self, edge):
        self._incoming_edges[edge.source()] = edge

    def _add_undirected_edge(self, edge):
        other = edge.node1() if not self is edge.node1() else edge.node2()
        self._outgoing_edges[other] = edge
        self._incoming_edges[other] = edge

    def _remove_outgoing_edge(self, edge):
        del self._outgoing_edges[edge.destination()]

    def _remove_incoming_edge(self, edge):
        del self._incoming_edges[edge.source()]

    def _remove_undirected_edge(self, edge):
        other = edge.node1() if not self is edge.node1() else edge.node2()
        del self._outgoing_edges[other]
        del self._incoming_edges[other]

    def name(self):
        return self._name

    def outgoing_edges(self):
        return list(self._outgoing_edges.values())

    def incoming_edges(self):
        return list(self._incoming_edges.values())

    def edge_to(self, node):
        return self._outgoing_edges.get(node)

    def edge_from(self, node):
        return self._incoming_edges.get(node)

    def has_edge_to(self, node):
        return self.edge_to(node) is not None

    def has_edge_from(self, node):
        return self.edge_from(node) is not None
    def __str__(self):
        res = self._name + "\n"
        return res


class Edge:
    def __init__(self, node1, node2, data = None):
        self._node1 = node1
        self._node2 = node2
        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)

    def nodes(self):
        return [self._node1, self._node2]

    def source(self):
        return self._node1

    def destination(self):
        return self._node2

    def is_directed(self):
        return True;

    def is_undirected(self):
        return not self.is_directed()
    def flow(self):
        res = 0
        for key, value in vars(self).items():
            if key == "load":
                res = value
        return res

    def __str__(self):
        res = self._node1.name() + " --> " + self._node2.name() + "\n"
        for key, value in vars(self).items():
            if not key.startswith("_"):
                res += "    " + str(key) + " : " + str(value) + "\n"

        return res


class UndirectedEdge(Edge):
    def source(self):
        return None     # no source or destination defined for undirected edges

    def destination(self):
        return None     
 
    def node1(self):
        return self._node1

    def node2(self):
        return self._node2

    def is_directed(self):
        return False;

    def __str__(self):
        res = self._node1.name() + " <--> " + self._node2.name() + "\n"
        for key, value in vars(self).items():
            if not key.startswith("_"):
                res += "    " + str(key) + " : " + str(value) + "\n"
        return res


class Path:
    def __init__(self, start):
        self._nodes = [start]
        self._edges = []

    def nodes(self):
        return list(self._nodes)

    def edges(self):
        return list(self._edges)

    def start(self):
        return self._nodes[0]

    def end(self):
        return self._nodes[-1]
    def append(self, edge, node):
        if not edge.source() == self._nodes[-1] or not edge.destination() == node:
            raise ValueError("Edge is not connecting the new and the previous node")
        self._nodes.append(node)
        self._edges.append(edge)
        return self     # allows function chaining
    def pop(self):
        self._nodes.pop()
        self._edges.pop()
        return self

    def __str__(self):
        res = ""
        for edge in self.edges():
            res += str(edge)
        return res
