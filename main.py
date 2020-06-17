#
# The entry place to demonstrate different applications
# Where, applications were encapsulated into samples folder.
#
# @Author: Terry Pan
# @Date: Wed Jun 17 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Wed Jun 17 2020 3:28:40 PM
#
import os
from netwalk.utils.misc import (
    file_to_graph,
    get_dataset_from_file
)
from netwalk.utils.graph import Graph
from netwalk.samples.link_prediction_samples.deep_walk import (
    deep_walk_application
)
from netwalk.samples.link_prediction_samples.neighborhood_based import (
    neighbourhood_application
)
from typing import List, Tuple


if __name__ == "__main__":
    # the project root location
    project_root: str = os.path.dirname(os.path.abspath(__file__))

    # locations for different datasets
    assets_loc: str = "assets"
    train_file: str = os.path.join(project_root, assets_loc, "training.txt")
    neg: str = os.path.join(project_root, assets_loc, "val_negative.txt")
    pos: str = os.path.join(project_root, assets_loc, "val_positive.txt")
    test: str = os.path.join(project_root, assets_loc, "test.txt")

    # create training, validation, testing dataset in desired format
    train_set: Graph = file_to_graph(train_file)
    validate_set: List[Tuple[str, str, str]] = get_dataset_from_file(neg, '0')\
        + get_dataset_from_file(pos, '1')
    test_set = get_dataset_from_file(test)

    print("Neighbourhood based methods")
    neighbourhood_application(train_set, validate_set)
    print()
    print("Deep walk")
    deep_walk_application(train_set, validate_set, test_set)
