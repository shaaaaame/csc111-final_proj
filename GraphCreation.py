"""
Implements the graph object using cleaned data.
Graph will contain songs with vertices being their Jaccard Similarity Index.

Functions to note:
- create_graph(list[Song]) : use this to instantiate and return a graph given a list of songs.
"""

import jsonpickle
import json

from Classes import Song, Graph, Node, read_csv

# CSV that contains data to use
CSV_FILEPATH = "tracks_2020.csv"

# Filepath of where our serialised graph is to be stored
SAVED_GRAPH_FILEPATH = "song_graph_v2.json"

# Dictates how far apart ATTRIBUTE values between 2 songs need to be to deem them similar
SIMILARITY_THRESHOLD = 0.1

# Dictates what proportion of attributes must be similar for SONGS to be deemed similar
JACCARD_THRESHOLD = 0.75


def calc_song_jaccard_index(song1: Song, song2: Song) -> float:
    """Calculates and returns Jaccard Similarity given two songs"""
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


def add_edges_for_node(graph: Graph, compared_song: Song, songs: list[Song]) -> None:
    """Mutates graph to add edges of songs that are similar to compared_song"""

    for song in songs:
        jaccard = calc_song_jaccard_index(song, compared_song)
        if jaccard >= JACCARD_THRESHOLD:
            graph.add_edge(compared_song.id, song.id, jaccard)


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
    populate_graph(graph, songs)

    for i in range(len(songs)):
        print(i)
        compared_song = songs[i]
        songs_to_compare = [songs[j] for j in range(i + 1, len(songs))]

        add_edges_for_node(graph, compared_song, songs_to_compare)

    return graph


def save_graph(graph: Graph, file_name: str) -> None:
    """Saves the graph in serialised form given the graph to be saved and the file name it should be saved as."""
    file = open(file_name, 'w')
    json_text = jsonpickle.encode(graph)
    json.dump(json_text, file)

    print("Succesfully saved file.")
    file.close()
    return


def load_graph(file_name: str) -> Graph:
    """Loads the serialised form of graph given the file name."""
    try:
        file = open(file_name, 'r')
        json_text = json.load(file)
        graph = jsonpickle.decode(json_text)
        file.close()
        return graph
    except FileNotFoundError:
        print("Error loading file: file not found.")
        raise FileNotFoundError


if __name__ == "__main__":

    # THIS SCRIPT CREATES A NEW GRAPH FROM THE GIVEN CSV AND SERIALIZES THE OBJECT AS A JSON.
    # IT TAKES 30 MINUTES TO LOAD, DO NOT RUN THIS. ONLY RUN MAIN.
    songs = read_csv(CSV_FILEPATH)
    new_graph = create_graph(songs)
    save_graph(new_graph, SAVED_GRAPH_FILEPATH)
