"""
Project for CSC111
"""
from __future__ import annotations
from typing import Any

class Song:
    """
    A class to represent the songs.
    """
    def __init__(self, ac: float, dance: float, energy: float,
                 ins: float, live: float, speech: float):
        self.ac = ac
        self.dance = dance
        self.energy = energy
        self.ins = ins
        self.live = live
        self.speech = speech

class Graph:
    """
    A class to represent all the songs
    """
    nodes: list[Nodes]

    def __init__(self):
        self.nodes = []

    def add_song(self, song: Song):
        """
        Add a song to the graph
        """
        self.nodes.append(song)

    def get_songs(self):
        """
        Return the songs in this graph
        """
        return self.nodes

    def __len__(self):
        return len(self.nodes)

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
