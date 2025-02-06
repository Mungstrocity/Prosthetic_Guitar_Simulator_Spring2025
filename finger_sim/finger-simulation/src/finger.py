from math import cos, sin

class Finger:
    def __init__(self, segments, lengths):
        self.segments = segments
        self.lengths = lengths
        self.joint_positions = [(0, 0)] * (segments + 1)
        self.initial_positions = [(0, 0)] * (segments + 1)

    def draw(self, screen):
        for i in range(self.segments):
            start_pos = self.joint_positions[i]
            end_pos = self.joint_positions[i + 1]
            self.draw_line(screen, start_pos, end_pos)

    def update_positions(self, angles, origin):
        self.joint_positions[0] = origin
        self.initial_positions[0] = origin
        for i in range(self.segments):
            if i == 0:
                self.joint_positions[i + 1] = (
                    int(origin[0] + self.lengths[i] * cos(angles[i])),
                    int(origin[1] - self.lengths[i] * sin(angles[i]))  # Adjust for standard orientation
                )
                self.initial_positions[i + 1] = self.joint_positions[i + 1]
            else:
                x = int(self.joint_positions[i][0] + self.lengths[i] * cos(sum(angles[:i + 1])))
                y = int(self.joint_positions[i][1] - self.lengths[i] * sin(sum(angles[:i + 1])))  # Adjust for standard orientation
                self.joint_positions[i + 1] = (x, y)
                self.initial_positions[i + 1] = self.joint_positions[i + 1]

    def draw_line(self, screen, start, end):
        import pygame
        pygame.draw.line(screen, (0, 0, 0), start, end, 5)