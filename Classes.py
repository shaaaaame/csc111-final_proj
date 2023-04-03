"""
Project for CSC111
"""
from __future__ import annotations
from typing import Any
import csv


class Song:
    """
    A class to represent the songs.
    """
    def __init__(self, id: str, name: str, ac: float, dance: float, energy: float,
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

    def get_attribute(self):
        """
        Return a dict of attributes
        """
        attributes = {}
        attributes['ac'] = self.ac
        attributes['dance'] = self.dance
        attributes['energy'] = self.energy
        attributes['ins'] = self.ins
        attributes['live'] = self.live
        attributes['speech'] = self.speech
        attributes['tempo'] = self.tempo
        attributes['val'] = self.val
        return attributes


class Graph:
    """
    A class to represent all the songs.

    Instance Attributes:
    - nodes: a dictionary mapping a song id number to it's node

    """
    nodes: dict[str, Node]

    def __init__(self):
        self.nodes = {}

    def add_node(self, song: Song):
        """
        Add a node to the graph
        """
        self.nodes[song.id] = Node(song, {})

    def get_nodes(self) -> list[Node]:
        """
        Return the nodes in this graph
        """
        nodes_so_far = []
        for node in self.nodes:
            nodes_so_far.append(self.nodes[node])
        return nodes_so_far

    def __len__(self):
        return len(self.nodes)

    def add_edge(self, id1: Any, id2: Any, weight: float) -> None:
        """Add an edge between the two vertices with the given id number in this graph.

        Raise a ValueError if id1 or id2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if id1 in self.nodes and id2 in self.nodes:
            v1 = self.nodes[id1]
            v2 = self.nodes[id2]

            # Add the new edge
            v1.neighbours[id2] = weight
            v2.neighbours[id1] = weight
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
    neighbours: dict[str, float]  # song_id : weight (similarity)

    def __init__(self, item: Song, neighbours: dict[str, float]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours

    def get_item(self) -> Song:
        """Returns the item stored in this node"""
        return self.item


def read_csv(csv_file: str) -> list[Song]:
    """
    Read the given csv_file and add to the graph
    """
    songs = []
    with open(csv_file, errors='ignore') as file:
        reader = csv.reader(file)
        header = next(file)
        for row in reader:
            id = row[0]
            name = row[1]
            ac = float(row[6])
            dance = float(row[3])
            energy = float(row[4])
            ins = float(row[7])
            live = float(row[8])
            speech = float(row[5])
            tempo = float(row[10])
            val = float(row[9])

            song = Song(id, name, ac, dance, energy, ins, live, speech, tempo, val)
            songs.append(song)

    return songs
