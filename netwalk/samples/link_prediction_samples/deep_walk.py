#
# The demo for deepwalk algorithm
#
# @Author: Terry Pan
# @Date: Thu Jun 18 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Thu Jun 18 2020 3:45:14 PM
#
from gensim.models.callbacks import CallbackAny2Vec
import multiprocessing
from typing import (
    List,
    Tuple,
)
from netwalk.utils.misc import (
    link_prediction_eval,
    top_n_rank,
    calc_similarity_from_validation_set,
    get_edge_without_score
)
from netwalk.utils.graph import Graph
from netwalk.algorithms\
    .link_prediction\
    .deepwalk import Deepwalk
from netwalk.algorithms\
    .link_prediction\
    .walk_strategy import Walk
import gensim


class callback(CallbackAny2Vec):
    """
    Callback to print loss and accuracy after each epoch.
    """

    def __init__(self, valid_set):
        self.epoch = 0
        self.loss_to_be_substracted = 0
        self.validation_set = valid_set

    def helper(self, model):
        res: List[Tuple[str, str, str]
                  ] = get_edge_without_score(
                      top_n_rank(
                          calc_similarity_from_validation_set(
                              self.validation_set,
                              model.similarity
                          ), 100))
        return link_prediction_eval(res)

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        new_loss = loss - self.loss_to_be_substracted
        self.loss_to_be_substracted = loss
        accuracy = self.helper(model)
        print('Loss and Accuracy after epoch {}: {}  |  {}'.format(self.epoch,
                                                                   new_loss,
                                                                   accuracy))
        self.epoch += 1


def deep_walk_application(train_set: Graph,
                          valid_set: List[Tuple[str, str, str]],
                          test_set: List[Tuple[str, str, str]]):
    """the demo for deepwalk algorithm

    Parameters
    ----------
    train_set : Graph
        the training set
    valid_set : List[Tuple[str, str, str]]
        validation set
    test_set : List[Tuple[str, str, str]]
        testing set
    """
    random_walk_params = {
        'walk_length': 5,
        'iteration': 100,
        'strategy': Walk.BFS
    }
    sentences = Deepwalk(train_set, **random_walk_params)
    hyper_params = {
        'min_count': 1,
        'workers': multiprocessing.cpu_count(),
        'iter': 30,
        'seed': 10,
        'sg': 1,
        'window': 4,
        'size': 100,
        'compute_loss': True,
        'callbacks': [callback(valid_set)]
    }
    _ = gensim.models.Word2Vec(sentences, **hyper_params)
