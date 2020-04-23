from typing import Tuple, Union
from netwalk.utils.graph import UndiGraph, Graph
import enum


class Position(enum.Enum):
    TOP_LEFT = 'top_left'
    TOP_RIGHT = 'top_right'
    BOTTOM_LEFT = 'bottom_left'
    BOTTOM_RIGHT = 'bottom_right'
    EDGE_TOP = 'edge_top'
    EDGE_BOTTOM = 'edge_bottom'
    EDGE_LEFT = 'edge_left'
    EDGE_RIGHT = 'edge_right'


class GridToGraph:
    def __init__(self, dimension: Tuple[int, int],
                 is_8_direction: bool = False):
        self.__row = dimension[0]
        self.__col = dimension[1]
        self.__is_8_direction = is_8_direction

    def _determine_corner(self, position: Tuple[int, int]) \
            -> Union[Position, None]:
        if position == (0, 0):
            return Position.TOP_LEFT
        if position == (0, self.__col - 1):
            return Position.TOP_RIGHT
        if position == (self.__row - 1, 0):
            return Position.BOTTOM_LEFT
        if position == (self.__row - 1, self.__col - 1):
            return Position.BOTTOM_RIGHT
        return None

    def _determine_edge(self, position: Tuple[int, int]) \
            -> Union[Position, None]:
        if position[0] == 0 and \
                (position[1] != 0 or position[1] != self.__col - 1):
            return Position.EDGE_TOP
        if position[0] == self.__row - 1 and \
                (position[1] != 0 or position[1] != self.__col - 1):
            return Position.EDGE_BOTTOM
        if position[1] == 0 and \
                (position[0] != 0 or position[0] != self.__row - 1):
            return Position.EDGE_LEFT
        if position[1] == self.__col - 1 and \
                (position[0] != 0 or position[0] != self.__row - 1):
            return Position.EDGE_RIGHT
        return None

    def _to_string(self, row: int, col: int) -> Tuple[str, str]:
        return (str(row), str(col))

    def _add_corner_position(self, graph: UndiGraph, position: Tuple[int, int]):
        i, j = position
        if position == Position.TOP_LEFT:
            graph.add_edge(self._to_string(i, i + 1))
            graph.add_edge(self._to_string(i, j + 1))
        if position == Position.TOP_RIGHT:
            graph.add_edge(self._to_string(i, i + 1))
            graph.add_edge(self._to_string(i, j - 1))
        if position == Position.BOTTOM_LEFT:
            graph.add_edge(self._to_string(i - 1, j))
            graph.add_edge(self._to_string(i, j + 1))
        if position == Position.BOTTOM_RIGHT:
            graph.add_edge(self._to_string(i - 1, j))
            graph.add_edge(self._to_string(i, j - 1))

    def _add_edge_position(self, graph: UndiGraph, position: Tuple[int, int]):
        i, j = position
        if position == Position.EDGE_TOP:
            graph.add_edge(self._to_string(i, j - 1))
            graph.add_edge(self._to_string(i, j + 1))
            graph.add_edge(self._to_string(i + 1, j))
        if position == Position.EDGE_BOTTOM:
            graph.add_edge(self._to_string(i, j - 1))
            graph.add_edge(self._to_string(i, j + 1))
            graph.add_edge(self._to_string(i - 1, j))
        if position == Position.EDGE_LEFT:
            graph.add_edge(self._to_string(i + 1, j))
            graph.add_edge(self._to_string(i - 1, j))
            graph.add_edge(self._to_string(i, j + 1))
        if position == Position.EDGE_RIGHT:
            graph.add_edge(self._to_string(i + 1, j))
            graph.add_edge(self._to_string(i + 1, j))
            graph.add_edge(self._to_string(i, j-1))

    def generate_graph(self) -> Graph:
        graph = UndiGraph()
        for i in range(self.__row):
            for j in range(self.__col):
                corner = self._determine_corner((i, j))
                edge = self._determine_edge((i, j))
                if corner:
                    self._add_corner_position(graph, (i, j))
                if edge:
                    pass

        return graph
