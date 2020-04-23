from netwalk.utils.graph import Graph
from typing import List, Tuple
import heapq


class Dijkstra:
    def __init__(self, graph: Graph, src: str):
        self.__graph = graph
        self.__create_min_heap(src)

    def __create_min_heap(self, src: str):
        self.__min_heap: List[Tuple[float, str]] = []
        for node in self.__graph.get_nodes():
            if node == src:
                heapq.heappush(self.__min_heap, (0, src))
            else:
                heapq.heappush(self.__min_heap, (float('inf'), node))

    def shortest_path(self):
        while len(self.__min_heap):
            source_node = heapq.heappop(self.__min_heap)[1]

            for neighbour in self.__graph[source_node]:
                pass
