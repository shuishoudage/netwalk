#
# Deepwalk algorithm implementation
#
# @Author: Terry Pan
# @Date: Wed Jun 17 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Wed Jun 17 2020 4:23:31 PM
#
from .walk_strategy import Walk
from netwalk.utils.graph import Graph
from typing import Dict, Callable, List
from random import choice, random

"""
Network feature representation sampling algorithm

This algorithm implement deepwalk algorithm. Deepwalk algorithm utilizes
random walk to sampling features from a given network. The way that creates
features that affected by random walk strategies (DFS, BFS), the deepth of the
random walk.
"""


class Deepwalk:
    def __init__(self, G: Graph, strategy: Walk, walk_length: int = 5, iteration: int = 1, p: float = 0.5):
        """initialize a deepwalk object

        Parameters
        ----------
        G : Graph
            run a random walk by the given graph
        strategy : Walk
            the walk strategy (DFS, BFS, BFS&DFS)
        walk_length : int, default 5
            the deepth of the random walk
        iteration : int, default 1
            this parameter controls the total sampling size
        p : float, default 0.5
            the probability that the random walk strategy chooses BFS and DFS
        """
        self.graph = G
        self.neighbours = self.graph.get_out_adj_list()
        self.strategies: Dict[Walk, Callable] = {}
        self.strategies[Walk.BFS] = self.__bfs_search
        self.strategies[Walk.DFS] = self.__dfs_search
        self.strategies[Walk.BFS_DFS] = self.__bfs_dfs_search
        self.walk_length = walk_length
        self.probability = p
        self.iter = iteration
        self.strategy = strategy

    def __bfs_search(self, node: str) -> List[str]:
        """bfs search strategy

        Parameters
        ----------
        node : str
            the starting node

        Returns
        -------
        List[str]
            the visited node of the total steps (walk_length) 
        """
        return [choice([node] + self.neighbours[node])
                for _ in range(self.walk_length)]

    def __dfs_search(self, node: str) -> List[str]:
        """dfs search

        Parameters
        ----------
        node : str
            the starting node

        Returns
        -------
        List[str]
            the visited node of the total steps (walk_length).
        """
        res: List[str] = [node]
        for _ in range(self.walk_length-1):
            node = choice(self.neighbours[node])
            res.append(node)
        return res

    def __bfs_dfs_search(self, node: str) -> List[str]:
        """the combination of bfs and dfs search

        Parameters
        ----------
        node : str
            the starting node

        Returns
        -------
        List[str]
            the visited node of the total steps (walk_length).
        """
        res: List[str] = [node]

        for _ in range(self.walk_length-1):
            # Based on the given probability, random() generates number
            # between (0,1), the argument probability controls how likely
            # a bfs or dfs been selected.
            if random() > self.probability:  # select dfs
                node = choice(self.neighbours[node])
                res.append(node)
            else:  # select bfs
                res.append(choice([node] + self.neighbours[node]))
        return res

    def __iter__(self):
        nodes = self.graph.get_nodes()
        for _ in range(self.iter):
            for node in nodes:
                sentence = self.strategies[self.strategy](node)
                yield sentence
