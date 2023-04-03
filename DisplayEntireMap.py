import pygame
from typing import Tuple
from Classes import Graph, Node, Song, read_csv

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize pygame
pygame.init()

# Set the width and height of the screen (in pixels)
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the caption of the window
pygame.display.set_caption("Graph as Map")


# Define a function to convert the coordinates of a node to the corresponding pixel position on the screen
def node_pos_to_pixel_pos(node_pos: Tuple[float, float]) -> Tuple[int, int]:
    """
    # todo
    """
    x = int(node_pos[0] * 100 + 400)
    y = int(-node_pos[1] * 100 + 300)
    return (x, y)


# Define a function to draw a node on the screen
def draw_node(node: Node) -> None:
    """
    # todo
    """
    pos = node_pos_to_pixel_pos(node.item.get_attribute()['tempo'], node.item.get_attribute()['val'])
    pygame.draw.circle(screen, GRAY, pos, 10)
    font = pygame.font.Font(None, 20)
    text = font.render(node.item.name, True, BLACK)
    text_rect = text.get_rect(center=pos)
    screen.blit(text, text_rect)


# Define a function to draw an edge on the screen
def draw_edge(node1: Node, node2: Node, weight: float) -> None:
    """
    # todo
    """
    pos1 = node_pos_to_pixel_pos(node1.item.get_attribute()['tempo'], node1.item.get_attribute()['val'])
    pos2 = node_pos_to_pixel_pos(node2.item.get_attribute()['tempo'], node2.item.get_attribute()['val'])
    pygame.draw.line(screen, RED, pos1, pos2, int(weight))


# Load the songs from the CSV file
songs = read_csv("songs.csv")

# Create a graph and add the nodes and edges
graph = Graph()
for song in songs:
    graph.add_node(song)

for node1 in graph.nodes.values():
    for node2, weight in node1.neighbours.items():
        graph.add_edge(node1.item.id, node2.item.id, weight)

# Draw the nodes and edges on the screen
screen.fill(WHITE)
for node in graph.nodes.values():
    draw_node(node)
    for neighbour, weight in node.neighbours.items():
        if node.item.id < neighbour.item.id:
            draw_edge(node, neighbour, weight)

# Update the screen
pygame.display.update()

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit pygame
pygame.quit()
