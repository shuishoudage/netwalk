from typing import Tuple, Dict, List, Set
from collections import defaultdict
import numpy as np

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
        self.__out_adj_list: Dict[str, List[str]] = defaultdict(list)
        self.__in_adj_list: Dict[str, List[str]] = defaultdict(list)
        self.__nodes: Set[str] = set()

    def __get_lookup_table(self) -> Dict[str, int]:
        """
        a helper method, mapping nodes to index. The index is used to update
        the value in adjacency matrix
        """
        return {node: index for index, node in enumerate(self.__nodes)}

    def __get_adj_matrix(self) -> np.ndarray:
        nodes_count = self.get_nodes_count()
        matrix = np.repeat(0, nodes_count*nodes_count).reshape(nodes_count,
                                                               nodes_count)
        lookup_table = self.__get_lookup_table()
        if len(self.__out_adj_list):
            for start, ends in self.__out_adj_list:
                index = lookup_table[start]
                updated_index = [lookup_table[i] for i in ends]
                matrix[index][updated_index] = 1
        return matrix

    def get_nodes_count(self) -> int:
        """
        return the total number of nodes in the graph
        """
        return len(self.__nodes)

    def add_node(self, node: str):
        """
        add nodes to graph
        """
        if not isinstance(node, str):
            raise TypeError("node only support string type")
        if node == '':
            raise ValueError("node cannot be empty")
        self.__nodes.add(node)

    def get_nodes(self) -> Set[str]:
        """
        return nodes in the graph
        """
        return self.__nodes

    def __add_edge(self, edge: Tuple[str, str]):
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
