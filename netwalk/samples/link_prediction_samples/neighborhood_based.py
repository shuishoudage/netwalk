#
# The demo for neighbourhood based algorithm
#
# @Author: Terry Pan
# @Date: Thu Jun 18 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Thu Jun 18 2020 3:47:40 PM
#
from typing import (
    List,
    Tuple,
)
from netwalk.algorithms.link_prediction.similarity_methods import Measure
from netwalk.utils.graph import Graph
from netwalk.utils.misc import (
    link_prediction_eval,
    top_n_rank,
    get_edge_without_score,
)
from netwalk.algorithms\
    .link_prediction\
    .neighbourhood_based_similarity import NeighbourhoodBasedSimilarity


def neighbourhood_application(train_set: Graph, validation_set: List[Tuple[str, str, str]]):
    """the demo for neighbourhood based algorithm

    Parameters
    ----------
    train_set : Graph
        the training set
    validation_set : List[Tuple[str, str, str]]
        the validation set

    Notes
    -----
    since neighbourhood based methods using memory based machine learning
    algorithm. Therefore, validation_set is essentially test set
    """
    for measure in Measure:
        scores = calc_similarity_by_measure(train_set, validation_set, measure)
        evalation = link_prediction_eval(
            get_edge_without_score(
                top_n_rank(scores, 100)))
        print('Accuracy for method {} is {}'.format(measure, evalation))


def calc_similarity_by_measure(train_set: Graph,
                               validation_set: List[Tuple[str, str, str]],
                               measure: Measure) -> \
        List[Tuple[str, str, str, float]]:
    """
    A helper function

    make the method neighbourhood_application calculating similarity easier
    """

    similarity = NeighbourhoodBasedSimilarity(train_set)
    scores: List[Tuple[str, str, str, float]] = []
    for pair in validation_set:
        scores.append(similarity.compute_proximity_score(
            (pair[0], pair[1], pair[2]), measure))

    return scores
