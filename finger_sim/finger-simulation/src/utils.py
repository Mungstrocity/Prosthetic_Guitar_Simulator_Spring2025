import pygame
import math

def draw_line(surface, start_pos, end_pos, color, width=1):
    pygame.draw.line(surface, color, start_pos, end_pos, width)

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)