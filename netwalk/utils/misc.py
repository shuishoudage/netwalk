#
# Misc helper tools for application
#
# @Author: Terry Pan
# @Date: Wed Jun 17 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Wed Jun 17 2020 2:43:55 PM
#
from typing import List, Tuple, Union, Callable
from random import choice
from netwalk.utils.graph import UndiGraph, DiGraph
from netwalk.utils.reader import FileReader
import os


def calc_similarity_from_validation_set(valid_set: List[Tuple[str, str, str]],
                                        similarity_func: Callable) -> \
        List[Tuple[str, str, str, float]]:
    """Calculate the similarity for two nodes by given a similarity function,
    this tool is for neighbourhood based link prediction

    Parameters
    ----------
    List[Tuple[str, str, str]]
        valid_set: validation set, the given data structure should be
        src_node, dest_node, label

    Callable
        similarity_func: the given similarity function (ex. cosine similarity)

    Returns
    -------
    List[Tuple[str, str, str, float]]
        res: the res with (src_node, dst_node, label, score)
    """
    res: List[Tuple[str, str, str, float]] = []
    for node in valid_set:
        res.append((node[0], node[1], node[2],
                    similarity_func(node[0], node[1])))
    return res


def get_dataset_from_file(file: str, label: str = '') -> \
        List[Tuple[str, str, str]]:
    """return a list of edges with format (src_node, dst_node, label)
    by given the location of a file. When the edge of given data file has no
    label attached, the label is setup as empty

    Parameters
    ----------
    str
        file: file locatoin

    str
        label: the label for given dataset

    Returns
    -------
    List[Tuple[str, str, str]]
        res: the res with (src_node, dst_node, label)
    """
    res: List[Tuple[str, str, str]] = []
    with open(file, 'r') as f:
        for line in f.readlines():
            edge = line.strip().split()
            res.append((edge[0], edge[1], label))
    return res


def file_writer(file_loc: str, res: List[Tuple[str, str, str]]):
    """write the given data to a file by given file location

    Parameters
    ----------
    str
        file_loc: file locatoin

    List[Tuple[str, str, str]]
        res: the data with format (src_node, des_node, label)
    """
    with open(file_loc, 'w') as f:
        for node in res:
            f.write(node[0] + " " + node[1] + os.linesep)


def format_print(weights: Union[List[str], List[Tuple[str, float]]]):
    title = ("node", "weight")
    print(f'|{title[0]:5}|\t{title[1]:8}|')
    print('|-------------|-------------|')
    for k, v in weights:
        print(f'|{k:5} | {v:12} |')
    print()


def file_to_graph(file: str, digraph: bool = False) -> \
        Union[DiGraph, UndiGraph]:
    """read a dataset by given file name then convert the dataset to a
    digraph or undigraph instance

    Parameters
    ----------
    str
        file: file locatoin

    bool
        digraph: the default graph type is undigraph. However, when setting this
        value as True, the returned graph type becomes digraph

    Returns
    -------
    Union[DiGraph, UndiGraph]
        return either digraph or undigraph
    """
    txt_reader = FileReader(file)
    graph: Union[DiGraph, UndiGraph] = DiGraph() if digraph else UndiGraph()
    for record in txt_reader.get_data():
        graph.add_edge((record[0], record[1]))
    return graph


def link_prediction_eval(nodes: List[Tuple[str, str, str]]) -> float:
    """evaluation for link prediction result

    Parameters
    ----------
    nodes : List[Tuple[str, str, str]]
        the predicted data set with format (src_node, dst_node, label)

    Returns
    -------
    float
        the accuracy of the result

    Notes
    -----
    currently only using accuracy as the measurements. more measurements
    methods can be added later on (ex. F1, Recall, etc.)
    """
    corrected = sum([int(node[2]) for node in nodes])
    return corrected / len(nodes)


def get_edge_without_score(rank: List[Tuple[str, str, str, float]]) -> \
        List[Tuple[str, str, str]]:
    """by given the rank of dataset, return the dataset without score, this
    function is for reporting purpose (when audience only want to know the
    connections)

    Parameters
    ----------
    rank : List[Tuple[str, str, str, float]]
        the given connections with score, the format is (src_node, dst_node,
        label, score)

    Returns
    -------
    List[Tuple[str, str, str]]
        return the truncated connection
    """
    return list(map(lambda node: (node[0], node[1], node[2]), rank))


def top_n_rank(scores: List[Tuple[str, str, str, float]], n: int = None) -> \
        List[Tuple[str, str, str, float]]:
    """return the top n edges

    Parameters
    ----------
    scores : List[Tuple[str, str, str, float]]
        edges with score attached
    n : int, default None
        the top n edges, the caller wanted

    Returns
    -------
    List[Tuple[str, str, str, float]]
        top n edges
    """
    if n is not None:
        return sorted(scores, key=lambda x: x[3], reverse=True)[:n]
    return sorted(scores, key=lambda x: x[3], reverse=True)


def generate_non_connection_data(nodes: List[str],
                                 connection: List[Tuple[str, str]],
                                 size: int) -> List[Tuple[str, str]]:
    """Generate fake data without connections

    Parameters
    ----------
    nodes : List[str]
        a list of nodes in the graph
    connection : List[Tuple[str, str]]
        the connection we have inside the graph
    size : int
        how many rows of dataset the caller wanted

    Returns
    -------
    List[Tuple[str, str]]
        edges that not in connection.
    """
    res: List[Tuple[str, str]] = []
    for _ in range(size):
        nodeA = choice(nodes)
        nodeB = choice(nodes)
        while nodeA == nodeB:
            nodeB = choice(nodes)

        if (nodeA, nodeB) not in connection:
            res.append((nodeA, nodeB))

    return res
