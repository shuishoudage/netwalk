import unittest
from netwalk.utils.graph import Graph
from parameterized import parameterized


class GraphTest(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def tearDown(self):
        del self.graph

    def test_count_nodes(self):
        self.assertTrue(isinstance(self.graph.get_nodes_count(), int))

    @parameterized.expand([
        ("", ValueError),
        (10, TypeError),
        (None, TypeError),
    ])
    def test_add_node_exceptions(self, arg, expected):
        with self.assertRaises(ValueError):
            _ = self.graph.add_node("")

    @parameterized.expand([
        (["1"], 1),
        (["1", "2"], 2),
        (["1", "2", "1"], 2),
    ])
    def test_add_node(self, args, expected):
        for arg in args:
            self.graph.add_node(arg)

        self.assertEqual(expected, self.graph.get_nodes_count())
