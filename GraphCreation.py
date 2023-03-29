"""
Implements the graph object using cleaned data.
Graph will contain songs with vertices being their Jaccard Similarity Index.

Functions to note:
- create_graph(list[Song]) : use this to instantiate and return a graph given a list of songs.
"""

from Classes import Song, Graph, Node


# Dictates how far apart ATTRIBUTE values have to be deemed "similar"
SIMILARITY_THRESHOLD = 0.05

# Dictates what proportion of attributes must be similar for SONGS to be deemed similar
JACCARD_THRESHHOLD = 0.8


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


def find_edges_for_node(compared_song: Song, songs: list[Song]) -> dict[int]:
    """Returns ids of songs where vertics should be connected to compared_song"""
    similar_song_ids = {}  # dict of song.id : jaccard_similarity

    for song in songs:
        jaccard = calc_song_jaccard_index(song, compared_song)
        if jaccard >= JACCARD_THRESHHOLD:
            similar_song_ids[song.id] = jaccard

    return similar_song_ids


def add_song_edges(graph: Graph, compared_song: Song, similar_song_ids: dict[int]) -> None:
    """
    Add edges around compared_song's node to graph.
    Edges given by similar song ids (keys) with weights determined by their jaccard similarities (values).
    """
    for song_id in similar_song_ids:
        graph.add_edge(compared_song.id, song_id, similar_song_ids[song_id])


def populate_graph(graph: Graph, songs: list[Song]) -> None:
    """
    Adds all song nodes by mutating the given graph

    Note: WITHOUT edges
    """
    for song in songs:
        graph.nodes[song.id] = Node(song, {})


def create_graph(songs: list[Song]) -> Graph:
    """
    Returns a graph for the given list of songs, including their vertices.
    Graph weight represents similarity.
    """
    graph = Graph()
    similar_song_ids = {}

    populate_graph(graph, songs)

    for i in range(len(songs)):
        compared_song = songs[i]
        songs_to_compare = [songs[j] for j in range(i + 1, len(songs))]

        similar_song_ids = find_edges_for_node(compared_song, songs_to_compare)
        add_song_edges(graph, compared_song, similar_song_ids)

    return graph
