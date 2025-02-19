import pygame
from finger import Finger
from inverse_kinematics import InverseKinematics
from math import cos, sin, pi

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
INCH_TO_PIXEL = 100

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Finger Simulation")

# Create instances of Finger and InverseKinematics
segment_lengths = [1.75 * INCH_TO_PIXEL, 1 * INCH_TO_PIXEL, 0.625 * INCH_TO_PIXEL]  # Convert inches to pixels
finger = Finger(segments=3, lengths=segment_lengths)
ik = InverseKinematics(segment_lengths=segment_lengths)
max_reach = sum(segment_lengths)
origin = (WIDTH // 2, HEIGHT // 2)

# Initialize the finger in the straight-up position
initial_angles = [pi / 2, 0, 0]
finger.update_positions(initial_angles, origin)

# Marker positions
markers = [(origin[0] + (0.5 + i * 9/32) * INCH_TO_PIXEL, origin[1]) for i in range(6)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position and calculate joint angles
            target_pos = pygame.mouse.get_pos()
            print(f"Mouse clicked at: {target_pos}")
            relative_target_pos = (target_pos[0] - finger.joint_positions[-1][0], target_pos[1] - finger.joint_positions[-1][1])
            print(f"Origin: {finger.joint_positions}")
            print(f"Relative target position: {relative_target_pos}")
            
            try:
                angles = ik.calculate_angles(relative_target_pos)
                print(f"Calculated angles: {angles}")
                finger.update_positions(angles, origin)
            except ValueError:
                # If the target position is out of reach, do nothing
                print("Target position is out of reach")

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the range circle
    pygame.draw.circle(screen, (200, 200, 200), origin, max_reach, 1)

    # Draw the flat line and markers
    start_pos = markers[0]
    end_pos = markers[-1]
    pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)
    for marker in markers:
        pygame.draw.circle(screen, (255, 0, 0), marker, 5)

    # Draw the finger
    finger.draw(screen)

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()