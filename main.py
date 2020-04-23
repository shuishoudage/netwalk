from netwalk.utils.reader import FileReader
from netwalk.utils.graph import UndiGraph, DiGraph
from netwalk.algorithms.centrality.pageRank import PageRank
from netwalk.algorithms.centrality.brandes import Brandes
# import matplotlib.pyplot as plt
from typing import (
    Dict,
    List,
    Tuple,
    Union
)
import networkx as nx


def format_print(weights: Union[List[str], List[Tuple[str, float]]]):
    title = ("node", "weight")
    print(f'|{title[0]:5}|\t{title[1]:8}|')
    print('|-------------|-------------|')
    for k, v in weights:
        print(f'|{k:5} | {v:12} |')
    print()


def page_rank_application(file_loc: str) \
        -> Tuple[Dict[str, float], Union[List[str], List[Tuple[str, float]]]]:
    txt_reader = FileReader(file_loc)
    graph = UndiGraph()
    # build undirected graph
    for record in txt_reader.get_data():
        graph.add_edge((record[0], record[1]))

    page_rank = PageRank(graph)
    weights = page_rank.run_page_rank_algorithm()
    top_10_central_nodes = page_rank.get_top_n_centrality_nodes(
        weights, 10, False)
    return weights, top_10_central_nodes


def betweenness_application(file_loc: str) \
        -> Tuple[Dict[str, float], Union[List[str], List[Tuple[str, float]]]]:
    txt_reader = FileReader(file_loc)
    graph = UndiGraph()
    # build undirected graph
    for record in txt_reader.get_data():
        graph.add_edge((record[0], record[1]))
    b = Brandes(graph)
    b.run_brandes_algorithm()
    weights = b.get_betweenness()
    top_10_betweenness_nodes = b.get_top_n_betweenness(weights, 10, False)
    return weights, top_10_betweenness_nodes


def networkx_pagerank(file_loc: str):
    txt_reader = FileReader(file_loc)
    graph = nx.Graph()
    # build undirected graph
    for record in txt_reader.get_data():
        graph.add_edge(*record)

    res = nx.pagerank(graph)

    fin = sorted(res.items(), key=lambda i: i[1], reverse=True)[:10]
    format_print(fin)


if __name__ == "__main__":
    file_loc = "./asset/data.txt"

    weights, top_10 = betweenness_application(file_loc)

    for node in top_10:
        print(node, end=" ")
    print()

    weights, top_10 = page_rank_application(file_loc)
    for node in top_10:
        print(node, end=" ")
    print()
