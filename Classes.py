"""
Project for CSC111
"""
from __future__ import annotations
from typing import Any


class Song:
    """
    A class to represent the songs.
    """
    def __init__(self, id: int, name: str, ac: float, dance: float, energy: float,
                 ins: float, live: float, speech: float, tempo: float, valence: float):
        self.id = id
        self.name = name
        self.ac = ac
        self.dance = dance
        self.energy = energy
        self.ins = ins
        self.live = live
        self.speech = speech
        self.tempo = tempo
        self.val = valence


class Graph:
    """
    A class to represent all the songs.

    Instance Attributes:
    - nodes: a dictionary mapping a song id number to it's node

    """
    nodes: dict[int, Node]

    def __init__(self):
        self.nodes = {}

    def add_song(self, song: Song):
        """
        Add a song to the graph
        """
        self.nodes[song.id] = Node(song, set())

    def get_songs(self):
        """
        Return the songs in this graph
        """
        return self.nodes

    def __len__(self):
        return len(self.nodes)

    def add_edge(self, id1: Any, id2: Any) -> None:
        """Add an edge between the two vertices with the given id number in this graph.

        Raise a ValueError if id1 or id2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if id1 in self.nodes and id2 in self.nodes:
            v1 = self.nodes[id1]
            v2 = self.nodes[id2]

            # Add the new edge
            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError


class Node:
    """A vertex in a graph.

        Instance Attributes:
            - item: The data stored in this vertex.
            - neighbours: The vertices that are adjacent to this vertex.

        Representation Invariants:
            - self not in self.neighbours
            - all(self in u.neighbours for u in self.neighbours)
        """
    item: Song
    neighbours: set[Node]

    def __init__(self, item: Song, neighbours: set[Node]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours

    def get_connected_component(self, visited: set[Node]) -> set:
        """Return a set of all ITEMS connected to self by a path that does not use
        any vertices in visited.

        The items of the vertices in visited CANNOT appear in the returned set.

        Preconditions:
            - self not in visited
        """
        vertexes_so_far = {self.item}
        visited.add(self)
        for vertex in self.neighbours:
            if vertex not in visited:
                vertexes_so_far |= vertex.get_connected_component(visited)
        return vertexes_so_far

# import csv
#
#
# class Song:
#     """
#     A class to represent the songs.
#     """
#     def __init__(self, id: int, ac: float, dance: float, energy: float,
#                  ins: float, live: float, speech: float, tempo: float, val: float):
#         self.id = id
#         self.ac = ac
#         self.dance = dance
#         self.energy = energy
#         self.ins = ins
#         self.live = live
#         self.speech = speech
#         self.tempo = tempo
#         self.val = val
#
#
# class Graph:
#     """
#     A class to represent all the songs
#     """
#     nodes: list[Song]
#
#     def __init__(self):
#         self.nodes = []
#
#     def add_song(self, song: Song):
#         """
#         Add a song to the graph
#         """
#         self.nodes.append(song)
#
#     def get_songs(self):
#         """
#         Return the songs in this graph
#         """
#         return self.nodes
#
#     def __len__(self):
#         return len(self.nodes)
#
#
# def read_csv(csv_file: str):
#     """
#     Read the given csv_file and add to the graph
#     """
#     graph = Graph()
#     with open(csv_file) as file:
#         reader = csv.reader(file)
#         header = next(file)
#         for row in reader:
#             id = int(row[0])
#             ac = float(row[1])
#             dance = float(row[2])
#             energy = float(row[3])
#             ins = float(row[4])
#             live = float(row[5])
#             speech = float(row[6])
#             tempo = float(row[7])
#             val = float(row[8])
#
#             song = Song(id, ac, dance, energy, ins, live, speech, tempo, val)
#             graph.add_song(song)
#     return graph
#
#
# read_csv("test_echo.csv")
