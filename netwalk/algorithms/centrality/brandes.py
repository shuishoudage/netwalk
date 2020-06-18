#
# Summary of your module
#
# @Author: Terry Pan
# @Date: Thu Jun 18 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Thu Jun 18 2020 2:33:11 PM
#
from netwalk.utils.graph import Graph
from typing import List, Dict, Deque
from collections import defaultdict, deque

"""
Brandes Algorithm implementation

Brandes algorithm implements the idea of centrality. The idea is in a graph
(network), the more central nodes have more paths go through it.

1. Assume a directed, unweighted, connected graph G=<V, E>
2. Define \sigma(s,t), as the number of shortest paths between nodes s and t
3. Define \sigma(s,t|v) as the number of shortest paths between nodes s and t
also pass through v.
4. The betweenness centrality of v is defined as
C_b(v) = \sum \frac{\sigma(s,t|v)}{\sigma(s,t)}

to make it simple, the algorithm above is just calculate the percentage of
betweenness of each nodes in a graph.

In the algorithm above, the most time consuming part is calculate \sigma(s,t|v)
The improvments from Brandes is by utlizing BFS search, we find all the
shortest paths between s and all other nodes and store the paths for each
target v. This is called forward go through.

For each t, for each vertex w that occurs on one of the stored paths, count the
number of times w appears in total to give \sigma(s, t| w) and divide by the
total number of paths between s and t (i.e \sigma(s,t)). Add the result
to C_b(w). This is called backward go through.

See: https://d1b10bmlvqabco.cloudfront.net/attach/k6oypy582xc46g/k6pzzh0uq171kp/k8vic6pjvyh6/A_faster_algorithm_for_betweenness_centrality.pdf
"""


class Brandes:
    def __init__(self, graph: Graph):
        self.__graph = graph
        self.__pred: Dict[str, List[str]]
        self.__stack: List[str]
        self.__betweenness: Dict[str, float] = dict.\
            fromkeys(self.__graph.get_nodes(), 0.0)

    def run_brandes_algorithm(self):
        """
        In this method, a forward sweep is going through the network by using
        BFS search.
        """
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
        """
        The backward step to calculate the share by different nodes. Please
        refer the paper mentioned above.
        """
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
