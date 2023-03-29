"""
Implements the graph object using cleaned data
Graph will contain songs with vertices being their Jaccard Similarity Index

"""

from Graph import Graph
from Node import Node
from Classes import Song


# Dictates how far apart attribute values have to be deemed "similar"
SIMILARITY_THRESHOLD = 0.05


def calc_song_jaccard_index(song1: Song, song2: Song) -> float:
    """Calculates Jaccard Similarity given two songs"""
    def is_similar(attr1: float, attr2: float) -> bool:
        """Returns whether two attributes are similar enough using the SIMILARITY_THRESHOLD"""

        if attr1 - SIMILARITY_THRESHOLD <= attr2 <= attr1 + SIMILARITY_THRESHOLD:
            return True
        return False

    attributes1 = song1.get_attribute()
    attributes2 = song2.get_attribute()
    similar_so_far = 0

    for key in attributes1:
        if is_similar(attributes1[key], attributes2[key]):
            similar_so_far += 1

    return similar_so_far / len(attributes1)


def create_vertices_for_node(compared_song: Song, songs: list[Song]) -> dict[int]:



def create_graph(songs: list[Song]) -> Graph:
    graph = Graph()
