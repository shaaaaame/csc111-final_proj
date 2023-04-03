"""
Main running file!
"""

from GraphCreation import save_graph, load_graph, SAVED_GRAPH_FILEPATH
from spoti import song_search_id
from DisplaySongMap import run
from Classes import Song, Node


if __name__ == "__main__":

    # LOAD GRAPH
    print("Loading...")
    graph = load_graph("song_graph_v2.json")

    # USER INPUT
    user_song_name = input("Enter song name: ")
    user_song_id = song_search_id(user_song_name)
    print(user_song_id)

    while user_song_id not in graph.nodes:
        user_song_name = input("Song not in graph! Enter another song name: ")
        user_song_id = song_search_id(user_song_name)

    # RUN LOOP
    run(graph, user_song_id)

    # # SAVE GRAPH BEFORE TERMINATE PROGRAM
    # save_graph(graph, SAVED_GRAPH_FILEPATH)
