"""
Generate a map of similar songs based on user's song input.
"""
from __future__ import annotations

import pygame
import math

from Classes import Node, Graph

display_width = 800
display_height = 600

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Song Map")

draw = True

zoom = 1.0
offset = [0, 0]
central_node = ""
node_radius = 10
font_size = 24
distance_multiplier = 850


def graph_to_screen(position) -> tuple[float, float]:
    """
    Return a position in the screen coordinate system from a position in the graph coordinate system.
    """
    global zoom

    x, y = position
    x = int((x + offset[0]) * zoom)
    y = int((y + offset[1]) * zoom)
    # x = max(min(x, display_width), 0)
    # y = max(min(y, display_height), 0)
    return (x, y)


def calc_distances(song_node: Node) -> dict[str, float]:
    """Determine distances from central node. Returns song_id: distance"""
    global distance_multiplier

    distances = {}
    for neighbour_id, similarity in song_node.neighbours.items():
        if neighbour_id == song_node.item.id:
            distances[neighbour_id] = 0.0
        else:
            distances[neighbour_id] = max(50.0, (1 - similarity) * distance_multiplier)
    return distances


def display_label(label: str, node_position: tuple[float, float]) -> None:
    """Displays the label under each node, one word per line."""
    font = pygame.font.SysFont(None, 24)

    # split words so that only 1 word per line
    label = label.split(" ")
    text = [font.render(text_part, True, pygame.Color(255, 255, 255)) for text_part in label]

    for i in range(len(text)):
        text_rect = text[i].get_rect()
        text_rect.x = node_position[0] - text_rect.width / 2
        text_rect.y = node_position[1] + int(font_size * i * 0.75)
        screen.blit(text[i], text_rect)


def draw_node(graph: Graph, song_node: Node, position: tuple[float, float],
              angle_range: tuple[float, float], visited: set[str], depth: int) -> None:
    """Draws a node, and recursively calls itself to draw nodes up to depth away from current node."""
    global zoom

    song_data = get_data(graph, song_node)

    if 0 <= position[0] <= display_width and 0 <= position[1] <= display_height:
        # draw center node
        pygame.draw.circle(screen, pygame.Color(138, 177, 207), position, int(15 * zoom))

        # display label
        display_label(song_node.item.name, position)

        # determine distances of neighbour nodes from central node
        distances = calc_distances(song_node)
        distances = {s: distances[s] for s in distances if graph.nodes[s].item.name not in visited}

        # sort nodes by distance
        sorted_nodes = sorted(distances.keys(), key=lambda s: distances[s])

        # draw nodes
        for i, song in enumerate(sorted_nodes):
            angle_space = max(0.524, angle_range[1] - angle_range[0] / len(distances))
            neighbour_node = graph.nodes[song]
            if neighbour_node.item.name in visited:
                continue
            distance = distances[song]
            angle = (i * angle_space / (len(distances))) + angle_range[0]

            x = position[0] + distance * math.cos(angle)
            y = position[1] + distance * math.sin(angle)
            x, y = graph_to_screen((x, y))

            if depth > 0:

                # draw edges
                edge_color = pygame.Color(89, 101, 164)
                distance = math.sqrt((position[0] - x) ** 2 + (position[1] - y) ** 2)
                if distance != 0:
                    dx = (position[0] - x) / distance
                    dy = (position[1] - y) / distance
                    start = (int(position[0] - dx * 20), int(position[1] - dy * 20))
                    end = (int(x + dx * node_radius), int(y + dy * node_radius))
                    pygame.draw.line(screen, edge_color, start, end, int(3 * zoom))

                visited.add(neighbour_node.item.name)
                draw_node(graph, neighbour_node, (x, y), (angle - 1, angle + 1), visited, depth - 1)


def draw_graph(screen, user_song_node: Node, graph: Graph, depth: int) -> None:
    """
    Draw the graph/map such that songs with a higher jaccard similarity index are drawn closer to the central node.
    """
    global zoom

    song_data = get_data(graph, user_song_node)
    screen.fill(pygame.Color(36, 52, 108))

    center = (int(display_width / 2), int(display_height / 2))
    center = graph_to_screen(center)

    draw_node(graph, user_song_node, center, (0, 2*math.pi), {user_song_node.item.name}, depth)


def display_graph(draw, user_song_node, graph, depth: int) -> None:
    """
    Display the map to the user.
    """
    global zoom

    while draw:
        # update
        pygame.display.flip()

        # user interaction
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                draw = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom *= 1.1
                elif event.button == 5:
                    zoom /= 1.1

        # scrolling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            offset[0] += 1 / zoom
        if keys[pygame.K_RIGHT]:
            offset[0] -= 1 / zoom
        if keys[pygame.K_UP]:
            offset[1] += 1 / zoom
        if keys[pygame.K_DOWN]:
            offset[1] -= 1 / zoom

        draw_graph(screen, user_song_node, graph, depth)

    pygame.quit()


def get_data(graph: Graph, user_node: Node) -> dict[str, float]:
    """
    Take in node data and return a dictionary of {song names: similarity to user's song}
    """
    similar_songs = {}

    for neighbour_song_id in user_node.neighbours:
        neighbour_node = graph.nodes[neighbour_song_id]
        similar_songs[neighbour_node.item.name] = user_node.neighbours[neighbour_song_id]

    return similar_songs


# def search_song(user_input, nodes: list[Node]):
#     """
#     Find the user's song, if it exists.
#     """
#     for node in nodes:
#         if node.item.name == user_input:
#             return node
#
#     # handle case where song is not in dataset
#     print(user_input + " was not found in the dataset.")


def run(graph: Graph, user_song_id: str):
    # SEARCH SONG AND GET DATA
    user_song_node = graph.nodes[user_song_id]

    # DISPLAY GRAPH
    central_node = user_song_node
    depth = int(input("Enter depth (maximum we recommend is 3, but you can go beyond that. It just won't be nice): "))
    draw_graph(screen, user_song_node, graph, depth)
    display_graph(draw, user_song_node, graph, depth)
