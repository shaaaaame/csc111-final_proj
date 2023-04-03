"""
Generate a visualized map of the songs graph.
"""
import pygame
import math
from Classes import Graph
from typing import List, Tuple

display_width = 800
display_height = 600

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Song Map")

draw = True

zoom = 6.0
offset = [0, 0]
node_radius = 10
font_size = 24
distance_multiplier = 10
node_to_pos = {}


def graph_to_screen(position, zoom):
    """
    Return a position in the screen coordinate system from a position in the graph coordinate system.
    """
    x, y = position
    x = int((x + offset[0]) * zoom)
    y = int((y + offset[1]) * zoom)
    return (x, y)


def get_positions(nodes, n) -> List[Tuple[float, float]]:
    """
    Return a position in the graph coordinate system for each node.
    """
    columns = round(math.sqrt(n))

    rows = math.ceil(n / columns)
    positions = []
    for i in range(len(nodes)):
        row = i // columns
        column = i % columns
        x = column / (columns - 1) * distance_multiplier * (n / 2)
        y = row / (rows - 1) * distance_multiplier * (n / 2)
        positions.append((x, y))
    return positions


def draw_nodes(zoom, nodes, n):
    """
    Draw the songs (nodes of the graph).
    """
    positions = get_positions(nodes, n)

    # determine maximum length of song name
    max_len = max([len(node.item.name) for node in nodes])
    node_font_size = font_size * (node_radius / max_len)

    for node in nodes:
        position = positions.pop(0)
        x, y = graph_to_screen(position, zoom)

        if 0 <= x <= display_width and 0 <= y <= display_height:
            # draw node
            pygame.draw.circle(screen, pygame.Color(176, 155, 199), (x, y), int(node_radius * zoom))

            # add text to node
            font = pygame.font.SysFont(None, int(node_font_size * zoom))
            text = font.render(node.item.name, True, pygame.Color(255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            screen.blit(text, text_rect)

        node_to_pos[node] = position


def draw_edges(zoom, nodes):
    """
    Draw the connections between songs (edges of the graph).
    """
    edge_colour = pygame.Color(173, 216, 230)

    # avoid repeats
    drawn_edges = set()

    for node in nodes:
        for neighbour in node.neighbours:
            start = graph_to_screen(node_to_pos.get(node), zoom)
            end = graph_to_screen(node_to_pos.get(neighbour), zoom)

            if (start, end) and (end, start) not in drawn_edges:
                size = max(int(1 * zoom), 1)
                pygame.draw.line(screen, edge_colour, start, end, size)
                drawn_edges.add((start, end))


def display_graph(draw, zoom, nodes, n):
    """
    Display the map to the user.
    """
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
            offset[0] += 5 / zoom
        if keys[pygame.K_RIGHT]:
            offset[0] -= 5 / zoom
        if keys[pygame.K_UP]:
            offset[1] += 5 / zoom
        if keys[pygame.K_DOWN]:
            offset[1] -= 5 / zoom

        screen.fill(pygame.Color(36, 52, 108))
        draw_edges(zoom, nodes)
        draw_nodes(zoom, nodes, n)

    pygame.quit()


def run(graph: Graph):
    """
    Display the map.
    """
    nodes = graph.get_nodes()
    n = len(nodes)

    draw_nodes(zoom, nodes, n)
    draw_edges(zoom, nodes)
    display_graph(draw, zoom, nodes, n)
