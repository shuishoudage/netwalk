from typing import Tuple, Dict, List, Set
from collections import defaultdict

"""
This is the abstract graph class, it's not meant to be creating objects
"""


class Graph(object):
    def __init__(self):
        """initialize Graph class. This constructor is not meant to concrete

        Parameters
        ----------
        __out_adj_list : Dict[str, List[str]]
            the out going adjacency list. For example
            a->b, a->c, a->d, the out_adj_list is {'a':['b', 'c', 'd']}
        __in_ajd_list : Dict[str, List[str]]
            the incoming adjacency list. For example
            a->b, a->c, a->d, the in_adj_list is
            {'b', ['a'], 'c':['a'], 'd':['a']}
        """
        self._out_adj_list: Dict[str, List[str]] = defaultdict(list)
        self._in_adj_list: Dict[str, List[str]] = defaultdict(list)
        self._nodes: Set[str] = set()

    def get_out_adj_list(self) -> Dict[str, List[str]]:
        return self._out_adj_list

    def get_in_adj_list(self) -> Dict[str, List[str]]:
        return self._in_adj_list

    def get_nodes_count(self) -> int:
        """
        return the total number of nodes in the graph
        """
        return len(self._nodes)

    def add_node(self, node: str):
        """
        add nodes to graph
        """
        if not isinstance(node, str):
            raise TypeError("node only support string type")
        if node == '':
            raise ValueError("node cannot be empty")
        self._nodes.add(node)

    def get_nodes(self) -> Set[str]:
        """
        return nodes in the graph
        """
        return self._nodes

    def _add_edge(self, edge: Tuple[str, str]):
        """
        an abstract parent class method, this method is used to check
        the format of given edge
        """
        if not isinstance(edge, tuple):
            raise TypeError("edge must be in tuple")
        if len(edge) != 2:
            raise ValueError("edge length must be 2")
        if not isinstance(edge[0], str) and not isinstance(edge[1], str):
            raise TypeError("edge value type must be string")


class DiGraph(Graph):
    def __init__(self):
        super().__init__()

    def add_edge(self, edge: Tuple[str, str]):
        self._add_edge(edge)
        self._out_adj_list[edge[0]].append(edge[1])
        self._in_adj_list[edge[1]].append(edge[0])
        self.get_nodes().add(edge[0])
        self.get_nodes().add(edge[1])


class UndiGraph(Graph):
    def __init__(self):
        super().__init__()

    def add_edge(self, edge: Tuple[str, str]):
        self._add_edge(edge)
        self._out_adj_list[edge[0]].append(edge[1])
        self._in_adj_list[edge[0]].append(edge[1])
        self.get_nodes().add(edge[0])
        self.get_nodes().add(edge[1])
        # when there is a self-loop, avoid adding node to the list again
        if edge[0] != edge[1]:
            self._out_adj_list[edge[1]].append(edge[0])
            self._in_adj_list[edge[1]].append(edge[0])
