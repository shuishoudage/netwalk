#
# The demo for pagerank algorithm
#
# @Author: Terry Pan
# @Date: Thu Jun 18 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Thu Jun 18 2020 3:52:51 PM
#
from typing import Tuple, List, Dict, Union
from netwalk.algorithms.centrality.pageRank import PageRank
from netwalk.utils.misc import file_to_graph


def page_rank_application(file_loc: str) \
        -> Tuple[Dict[str, float], Union[List[str], List[Tuple[str, float]]]]:
    graph = file_to_graph(file_loc)

    page_rank = PageRank(graph)
    weights = page_rank.run_page_rank_algorithm()
    top_10_central_nodes = page_rank.get_top_n_centrality_nodes(
        weights, 10, False)
    return weights, top_10_central_nodes
