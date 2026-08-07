# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

import rustworkx


class TestLocalClustering(unittest.TestCase):
    def test_local_clustering(self):
        graph = rustworkx.PyGraph()
        graph.add_nodes_from(list(range(5)))
        graph.add_edges_from_no_data([(0, 1), (1, 2), (0, 2), (0, 3), (2, 3), (3, 4)])
        res = rustworkx.graph_local_clustering(graph)
        self.assertEqual([res[i] for i in range(5)], [2 / 3, 1.0, 2 / 3, 1 / 3, 0.0])

    def test_local_clustering_triangle(self):
        graph = rustworkx.PyGraph()
        graph.add_nodes_from(list(range(3)))
        graph.add_edges_from_no_data([(0, 1), (0, 2), (1, 2)])
        res = rustworkx.graph_local_clustering(graph)
        self.assertEqual(dict(res.items()), {0: 1.0, 1: 1.0, 2: 1.0})

    def test_local_clustering_star(self):
        graph = rustworkx.PyGraph()
        graph.add_nodes_from(list(range(5)))
        graph.add_edges_from_no_data([(0, 1), (0, 2), (0, 3), (0, 4)])
        res = rustworkx.graph_local_clustering(graph)
        self.assertEqual([res[i] for i in range(5)], [0.0] * 5)

    def test_local_clustering_empty(self):
        graph = rustworkx.PyGraph()
        res = rustworkx.graph_local_clustering(graph)
        self.assertEqual(len(res), 0)

    def test_local_clustering_removed_node(self):
        # keys track actual node indices, even with holes from removals
        graph = rustworkx.PyGraph()
        graph.add_nodes_from(list(range(4)))
        graph.add_edges_from_no_data([(0, 1), (1, 2), (0, 2), (2, 3)])
        graph.remove_node(1)
        res = rustworkx.graph_local_clustering(graph)
        self.assertEqual(set(res.keys()), {0, 2, 3})
        # triangle 0-1-2 broken by removing node 1; no triangles remain
        self.assertEqual([res[i] for i in (0, 2, 3)], [0.0, 0.0, 0.0])
