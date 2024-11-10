extends Node3D

@export var follow_per: float = 1.0  # Speed for position following
@export var rotation_per: float = 1.0  # Speed for rotation following

@export var target: Node3D  # Assign the target node

func _process(delta: float) -> void:
	if target:
		# Interpolate position towards target position
		global_position = global_position.lerp(target.global_position, follow_per)
		
		# Interpolate rotation towards target rotation
		rotation_degrees.x = lerp_angle(global_rotation_degrees.x, target.rotation_degrees.x, rotation_per)
		rotation_degrees.y = lerp_angle(global_rotation_degrees.y, target.rotation_degrees.y, rotation_per)
		rotation_degrees.z = lerp_angle(global_rotation_degrees.z, target.rotation_degrees.z, rotation_per)
