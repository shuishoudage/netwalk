#
# The implementation of NeighbourhoodBasedSimilarity
#
# @Author: Terry Pan
# @Date: Wed Jun 17 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Wed Jun 17 2020 4:34:11 PM
#
from typing import List, Set, Callable, Dict, Tuple
from netwalk.utils.graph import Graph
from .similarity_methods import Measure
from functools import reduce
import math
import operator

"""
NeighbourhoodBasedSimilarity implementation

NeighbourhoodBasedSimilarity algorithms are essentially different set operations
The core idea behind these algorithms is similar nodes have same neightbours
"""


class NeighbourhoodBasedSimilarity:
    def __init__(self, G: Graph):
        self.graph = G
        self.measures: Dict[Measure, Callable] = {}
        self.measures[Measure.JACCARD] = self.jaccard_similarity
        self.measures[Measure.ADAR] = self.adar_similarity
        self.measures[Measure.PREFERENTIAL] = self.preferential
        self.negibours: Dict[str, List[str]] = self.graph.get_out_adj_list()

    def jaccard_similarity(self, setA: Set, setB: Set) -> float:
        """Jaccard similarity
        jaccard similarity is essentially two set operations. The intersection
        of two neightbours divide by the union of two neighbours.

        Parameters
        ----------
        setA : Set
            neighbours for one node
        setB : Set
            neighbours for another node

        Returns
        -------
        float
            the similarity score
        """
        numerator = len(setA.intersection(setB))
        denominator = len(setA.union(setB))
        return numerator / denominator

    def preferential(self, setA: Set, SetB: Set) -> float:
        """It's called preferential attachment method. This method is based
        on exprimental experience. It's essentially tells us the similar nodes
        are have similar number of neighbours.

        Parameters
        ----------
        setA : Set
            neighbours for one node
        setB : Set
            neighbours for another node

        Returns
        -------
        float
            the similarity score
        """
        return len(setA) * len(SetB)

    def adar_similarity(self, setA: Set, setB: Set) -> float:
        """adar/adamic similarity is the similar as method of jaccard_similarity
        the difference between them is that adar/adamic similarity adds a
        penalty term when one neighbour is a big figure of the whole network
        For example, Bill Gates.

        Parameters
        ----------
        setA : Set
            neighbours for one node
        setB : Set
            neighbours for another node

        Returns
        -------
        float
            the similarity score
        """
        commons: Set = setA.intersection(setB)
        return reduce(operator.add, map(lambda x: 1/math.log(x),
                                        map(self._count_neighbours,
                                            commons)), 0.0)

    def _count_neighbours(self, node: str) -> int:
        """
        a helper method to count number of neighours
        """
        neighbours: List[str] = self.graph.get_out_adj_list()[node]
        return len(neighbours)

    def compute_proximity_score(self, pair: Tuple[str, str, str], measure: Measure) -> Tuple[str, str, str, float]:
        """The entry method for calculate similarity score, what it does is
        actually called different similarity measure functions defined above

        Parameters
        ----------
        pair : Tuple[str, str, str]
            the given edge (src_node, dst_node, label)
        measure : Measure
            different measurements (Adar, Jaccard, Preferential)

        Returns
        -------
        Tuple[str, str, str, float]
            the edge with score attached
        """
        nodeA, nodeB, label = pair
        score = self.measures[measure](
            set(self.negibours[nodeA]), set(self.negibours[nodeB]))
        return (nodeA, nodeB, label, score)
