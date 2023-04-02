"""
Generate a map of similar songs based on user's song input.
"""
import pygame
import math
from Classes import Node

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
distance_multiplier = 450


def graph_to_screen(position):
    """
    Return a position in the screen coordinate system from a position in the graph coordinate system.
    """
    x, y = position
    x = int((x + offset[0]) * zoom)
    y = int((y + offset[1]) * zoom)
    x = max(min(x, display_width), 0)
    y = max(min(y, display_height), 0)
    return (x, y)


def draw_graph(screen, song_data):
    """
    Draw the graph/map such that songs with a higher jaccard similarity index are drawn closer to the central node.
    """
    screen.fill(pygame.Color(36, 52, 108))

    center = (display_width / 2, display_height / 2)
    center = graph_to_screen(center)
    if 0 <= center[0] <= display_width and 0 <= center[1] <= display_height:
        pygame.draw.circle(screen, pygame.Color(138, 177, 207), center, int(15 * zoom))
        font = pygame.font.SysFont(None, int(24 * zoom))
        text = font.render(central_node, True, pygame.Color(255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (center[0], center[1] + int(20 * zoom))
        screen.blit(text, text_rect)

        # determine distances of nodes from central node
        distances = {}
        for song, similarity in song_data.items():
            if song == central_node:
                distances[song] = 0
            else:
                distances[song] = (1 - similarity) * distance_multiplier

        # sort nodes by distance
        sorted_nodes = sorted(song_data.keys(), key=lambda s: distances[s])

        # draw nodes
        angle_step = 2 * math.pi / (len(song_data) - 1)
        for i, song in enumerate(sorted_nodes):
            if song == central_node:
                continue
            distance = distances[song]
            angle = i * angle_step
            x = center[0] + distance * math.cos(angle)
            y = center[1] + distance * math.sin(angle)
            x, y = graph_to_screen((x, y))
            if 0 <= x <= display_width and 0 <= y <= display_height:
                pygame.draw.circle(screen, pygame.Color(176, 155, 199), (x, y), int(node_radius * zoom))
                font = pygame.font.SysFont(None, int(font_size * zoom))
                text = font.render(song, True, pygame.Color(255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = (x, y + int(20 * zoom))
                screen.blit(text, text_rect)

            # draw edges
            edge_color = pygame.Color(89, 101, 164)
            distance = math.sqrt((center[0] - x) ** 2 + (center[1] - y) ** 2)
            if distance != 0:
                dx = (center[0] - x) / distance
                dy = (center[1] - y) / distance
                start = (int(center[0] - dx * 20), int(center[1] - dy * 20))
                end = (int(x + dx * node_radius), int(y + dy * node_radius))
                pygame.draw.line(screen, edge_color, start, end, int(3 * zoom))


def display_graph(draw, zoom, song_data):
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

        draw_graph(screen, song_data)

    pygame.quit()


def get_data(user_song):
    """
    Take in node data and return a dictionary of {song names: similarity to user's song}
    """
    similar_songs = {}
    for n, w in user_song.neighbours.items():
        similar_songs[n.item.name] = w

    return similar_songs


def search_song(user_input, nodes: list[Node]):
    """
    Find the user's song, if it exists.
    """
    for node in nodes:
        if node.item.name == user_input:
            return node

    # handle case where song is not in dataset
    print(user_input + " was not found in the dataset.")


# def run():
#     user_input = input("Type the name of a song: ")
#     user_song = search_song(user_input, (Nodes data))  # todo
#     song_data = get_data(user_song)
#     central_node = user_song.item.name
#     draw_graph(screen, song_data)
#     display_graph(draw, zoom, song_data)
