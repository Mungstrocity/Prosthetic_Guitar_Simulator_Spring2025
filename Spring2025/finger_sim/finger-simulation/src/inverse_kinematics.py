from math import acos, atan2, cos, sin, pi

class InverseKinematics:
    def __init__(self, segment_lengths):
        self.segment_lengths = segment_lengths
        self.joint_angles = [pi / 2] * len(segment_lengths)

    def calculate_angles(self, target_position):
        x, y = target_position
        total_length = sum(self.segment_lengths)

        if (x**2 + y**2) ** 0.5 > total_length:
            raise ValueError("Target position is out of reach")

        # Calculate angles using inverse kinematics
        for i in reversed(range(len(self.segment_lengths))):
            if i == len(self.segment_lengths) - 1:
                self.joint_angles[i] = self._calculate_angle(x, y, self.segment_lengths[i], i)
            else:
                x -= self.segment_lengths[i] * cos(self.joint_angles[i + 1])
                y -= self.segment_lengths[i] * sin(self.joint_angles[i + 1])
                self.joint_angles[i] = self._calculate_angle(x, y, self.segment_lengths[i], i)
        
        return self.joint_angles

    def _calculate_angle(self, x, y, length, index):
        ratio = length / ((x**2 + y**2) ** 0.5)
        # Ensure the ratio is within the valid range for acos
        ratio = max(min(ratio, 1), -1)
        angle = atan2(y, x) - acos(ratio)
        # Limit the angle to 0 to 90 degrees for the first segment
        if index == 0:
            return max(min(angle, pi / 2), 0)
        # Limit the angle to less than or equal to the angle on segment 1 and greater than segment 1 angle - 120 degrees
        elif index == 1:
            relative_angle = angle - self.joint_angles[index - 1]
            limited_angle = max(min(relative_angle, pi / 2), -2 * pi / 3)
            return limited_angle + self.joint_angles[index - 1]
        # Limit the angle to less than or equal to the angle on segment 2 and greater than segment 2 angle - 80 degrees
        else:
            relative_angle = angle - self.joint_angles[index - 1]
            limited_angle = max(min(relative_angle, self.joint_angles[index - 1]), self.joint_angles[index - 1] - 4 * pi / 9)
            return limited_angle + self.joint_angles[index - 1]

    def update_joint_positions(self):
        positions = []
        x, y = 0, 0
        for angle, length in zip(self.joint_angles, self.segment_lengths):
            x += length * cos(angle)
            y += length * sin(angle)
            positions.append((x, y))
        return positions