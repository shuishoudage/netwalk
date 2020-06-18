#
# Enum of walk strategies
#
# @Author: Terry Pan
# @Date: Wed Jun 17 2020
# @Email: pttdev123@gmail.com
# @Last modified by: Terry Pan
# @Last modified time: Wed Jun 17 2020 4:33:53 PM
#
import enum

"""
Walk strategies for random walk
"""


class Walk(enum.Enum):
    BFS = 1
    DFS = 2
    BFS_DFS = 3
