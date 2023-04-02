"""
Main running file!
"""

from GraphCreation import create_graph, save_graph, load_graph
import os

SAVED_GRAPH_FILEPATH = "song_graph"


def __main__():
    if os.path.exists(SAVED_GRAPH_FILEPATH):
        graph = load_graph(SAVED_GRAPH_FILEPATH)
    else:
        # GET DATA HERE
        songs = []

        graph = create_graph(songs)

    # RUN LOOP
    is_running = True
    while is_running:
        # USE GRAPH TO MAP, ETC
        pass

    # SAVE GRAPH BEFORE TERMINATE PROGRAM
    save_graph(graph, SAVED_GRAPH_FILEPATH)
