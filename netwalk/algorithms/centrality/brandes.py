from netwalk.utils.graph import Graph
from typing import List, Dict, Deque
from collections import defaultdict, deque


class Brandes:
    def __init__(self, graph: Graph):
        self.__graph = graph
        self.__pred: Dict[str, List[str]]
        self.__stack: List[str]
        self.__betweenness: Dict[str, float] = dict.\
            fromkeys(self.__graph.get_nodes(), 0.0)

    def run_brandes_algorithm(self):
        adj_list: Dict[str, List[str]] = self.__graph.get_out_adj_list()
        for src in self.__graph.get_nodes():
            pred: Dict[str, List[str]] = defaultdict(list)
            dist: Dict[str, float] = {node: float('inf') for node in
                                      self.__graph.get_nodes()}
            num_of_shortest_paths: Dict[str, int] = {node: 0 for node in
                                                     self.__graph.
                                                     get_nodes()}
            dist[src] = 0
            stack = []
            num_of_shortest_paths[src] = 1
            dequeue: Deque[str] = deque()
            dequeue.append(src)
            while len(dequeue):
                parent = dequeue.popleft()
                stack.append(parent)
                for neighbour in adj_list[parent]:
                    if dist[neighbour] == float('inf'):
                        dist[neighbour] = dist[parent] + 1
                        dequeue.append(neighbour)
                    if dist[neighbour] == dist[parent] + 1:
                        pred[neighbour].append(parent)
                        num_of_shortest_paths[neighbour] += \
                            num_of_shortest_paths[parent]
            self.__backward(src, pred, stack, num_of_shortest_paths)

    def __backward(self, src, pred, stack, num_of_shortest_paths):
        dependency: Dict[str, float] = {node: 0.0 for node in
                                        self.__graph.get_nodes()}
        self.__betweenness[src] += len(stack) - 1
        while len(stack):
            child = stack.pop()
            for parent in pred[child]:
                # the line is essentially implement formula
                # \sigma(s,v) / \sigma(s,w) * (1 + \delta(s|w))
                dependency[parent] += \
                    (num_of_shortest_paths[parent] /
                     num_of_shortest_paths[child]) * \
                    (1 + dependency[child])
            if child != src:
                self.__betweenness[child] += dependency[child]

    def get_betweenness(self) -> Dict[str, float]:
        return self.__betweenness

    def get_top_n_betweenness(self, betweenness: Dict[str, float],
                              n: int = 10,
                              with_measure: bool = False):
        """
        return top n betweenness nodes, if with_measure set to True, the
        centrality value will be also returned
        """
        if not isinstance(n, int):
            raise TypeError("n must be integer")
        if n <= 0 or n > self.__graph.get_nodes_count():
            raise ValueError(
                "n must be greater than zero and less than total nodes")
        soreted_betweenness = sorted(betweenness.items(),
                                     key=lambda kv: kv[1],
                                     reverse=True)
        top_n = soreted_betweenness[:n]
        if with_measure:
            return top_n
        return [node[0] for node in top_n]
