"""Backward compat wrapper"""
from .builder import build_graph, ego_graph
from .traversal import bfs_nodes, neighbors
from .metrics import connected_components, degree, density_of_ego
__all__=["build_graph","neighbors","connected_components","degree","ego_graph"]
