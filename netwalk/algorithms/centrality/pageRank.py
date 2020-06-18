#
# Summary of your module
#
# @Author: Terry Pan
# @Date: Thu Jun 18 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Thu Jun 18 2020 2:32:51 PM
#
from typing import Dict, List, Union, Tuple
from netwalk.utils.graph import Graph, DiGraph, UndiGraph
import copy

"""
PageRank Algorithm implementation

Pagerank follows the similar idea in thesis system. The more valuable paper
get more citations from other papers. What is more, When a famous paper
references another not famous paper, that not famous paper becomes important
as well.
"""


class PageRank:
    def __init__(self, graph: Graph,
                 threshold: float = 1.0e-6,
                 max_iter: int = 100,
                 alpha: float = 0.85):
        """create a pagerank algorithm. argument graph provided here will be
        used as source and argument threshold is used to determine when to stop
        the power interation

        Parameters
        ----------
        graph : Graph
            data source. A concrete object, either undigraph or digraph
        threshold : float, default 1.0e-6
            the threshold to determine when to stop iteration
        max_iter : int, default 100
            max iteration of this algorithm
        alpha : float, default 0.85
            controlling term
        """
        self.__graph = graph
        self.__threshold = threshold
        self.__max_iter = max_iter
        self.__alpha = alpha

    def _get_page_rank_of_adj_nodes(self) -> Dict[str, int]:
        """
        get the page rank of adjacent nodes
        """
        adj_list = self.__graph.get_out_adj_list()
        return dict(zip(adj_list.keys(),
                        map(len, adj_list.values())))

    def _get_init_weight(self) -> Dict[str, float]:
        """
        the initial weight, which is 1/total_nodes
        """
        nodes = self.__graph.get_nodes()
        weight = 1 / self.__graph.get_nodes_count()
        return {node: weight for node in nodes}

    def get_top_n_centrality_nodes(self, weights: Dict[str, float],
                                   n: int = 10,
                                   with_measure: bool = False) \
            -> Union[List[str], List[Tuple[str, float]]]:
        """
        return top n central nodes, if with_measure set to True, the
        centrality value will be also returned
        """
        if not isinstance(n, int):
            raise TypeError("n must be integer")
        if n <= 0 or n > self.__graph.get_nodes_count():
            raise ValueError(
                "n must be greater than zero and less than total nodes")
        soreted_weights = sorted(weights.items(),
                                 key=lambda kv: kv[1],
                                 reverse=True)
        top_n = soreted_weights[:n]
        if with_measure:
            return top_n
        return [node[0] for node in top_n]

    def page_rank_for_undigraph_alg(self) -> Dict[str, float]:
        """
        Using power iteration to calculate page rank algorithm
        """
        # initialize weights, set all to 1.0
        init_weights: Dict[str, float] = {
            node: 1.0 for node in self.__graph.get_nodes()}
        # page_rank_of_adj_nodes = self._get_page_rank_of_adj_nodes()
        adj_list = self.__graph.get_out_adj_list()

        while self.__max_iter:
            # old_weight is the previous weights before iteration
            old_weights = copy.deepcopy(init_weights)
            # update init_weight
            for adj_node, _ in init_weights.items():
                # using old_weights to update new_weights, if using current
                # weights to update new_weights, each iteration will cause
                # the weights of denpendent nodes change, which causes
                # mistakes
                # this is essentially \alpha * A.T * old_weights + (1-\alpha)
                new_weight: float = 0.0
                for n in adj_list[adj_node]:
                    new_weight += (1/len(adj_list[n]))

                init_weights[adj_node] = self.__alpha * \
                    new_weight * old_weights[adj_node] + (1-self.__alpha)

            if sum([abs(old_weights[n]-init_weights[n]) for n in old_weights])\
                    < self.__threshold * self.__graph.get_nodes_count():
                break
            self.__max_iter -= 1
        return init_weights

    def page_rank_for_digraph_alg(self) -> Dict[str, float]:
        """
        the core of page rank algorithms

        return the centrality weights for each nodes
        """
        init_weights = self._get_init_weight()
        page_rank_of_adj_nodes = self._get_page_rank_of_adj_nodes()
        adj_list = self.__graph.get_in_adj_list()
        num_of_nodes = self.__graph.get_nodes_count()

        while self.__max_iter:
            # old_weight is the previous weights before iteration
            old_weights = copy.deepcopy(init_weights)
            # update init_weight
            for node, weight in init_weights.items():
                new_weights: float = 0.0
                for adj_node in adj_list[node]:
                    # using old_weights to update new_weights, if using current
                    # weights to update new_weights, each iteration will cause
                    # the weights of denpendent nodes change, which causes
                    # mistakes
                    new_weights += old_weights[adj_node] / \
                        page_rank_of_adj_nodes[adj_node]

                init_weights[node] = new_weights

            if sum([abs(old_weights[n]-init_weights[n]) for n in old_weights])\
                    < self.__threshold * num_of_nodes:
                break
            self.__max_iter -= 1
        return init_weights

    def run_page_rank_algorithm(self) -> Dict[str, float]:
        """
        the core of page rank algorithms

        return the centrality weights for each nodes
        """
        if isinstance(self.__graph, DiGraph):
            return self.page_rank_for_digraph_alg()
        elif isinstance(self.__graph, UndiGraph):
            return self.page_rank_for_undigraph_alg()
        else:
            raise ValueError("unsupported graph type")
