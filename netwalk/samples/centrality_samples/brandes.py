#
# The demo for brandes algorithm
#
# @Author: Terry Pan
# @Date: Thu Jun 18 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Thu Jun 18 2020 3:52:26 PM
#
from typing import Tuple, List, Dict, Union
from netwalk.algorithms.centrality.brandes import Brandes
from netwalk.utils.misc import file_to_graph


def betweenness_application(file_loc: str) \
        -> Tuple[Dict[str, float], Union[List[str], List[Tuple[str, float]]]]:
    graph = file_to_graph(file_loc)
    b = Brandes(graph)
    b.run_brandes_algorithm()
    weights = b.get_betweenness()
    top_10_betweenness_nodes = b.get_top_n_betweenness(weights, 10, False)
    return weights, top_10_betweenness_nodes
