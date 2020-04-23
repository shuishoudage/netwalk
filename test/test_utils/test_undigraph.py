import unittest
from parameterized import parameterized
from netwalk.utils.graph import UndiGraph


class UndiGraphTest(unittest.TestCase):
    def setUp(self):
        self.graph = UndiGraph()

    def tearDown(self):
        del self.graph

    @parameterized.expand([
        ([
            ("1", "2"),
            ("1", "3")
        ], {"1": ["2", "3"], "2":["1"], "3":["1"]}),

        ([
            ("1", "2"),
        ], {"1": ["2"], "2":["1"]}),

        ([
            ("1", "2"),
            ("1", "3"),
            ("1", "1"),
        ], {"1": ["2", "3", "1"], "2":["1"], "3":["1"]}),

        ([
            ("1", "2"),
            ("2", "3"),
            ("3", "1"),
        ], {
            "1": ["2", "3"],
            "2": ["1", "3"],
            "3": ["2", "1"],
        }),
        ([
            ("1", "2"),
            ("1", "3"),
            ("1", "4"),
        ], {
            "1": ["2", "3", "4"],
            "2": ["1"],
            "3": ["1"],
            "4": ["1"],
        }),
    ])
    def test_get_adj_list(self, args, expected):
        for arg in args:
            self.graph.add_edge(arg)
        self.assertDictEqual(self.graph.get_out_adj_list(), expected)

    @parameterized.expand([
        ("", TypeError),
        (None, TypeError),
        (("none",), ValueError),
        ((1, 2), TypeError),
    ])
    def test_add_edge_exceptions(self, arg, expected):
        with self.assertRaises(expected):
            self.graph.add_edge(arg)
