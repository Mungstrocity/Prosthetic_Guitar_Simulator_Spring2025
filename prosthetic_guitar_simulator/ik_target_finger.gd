extends Marker3D

#target Node3D on the guitar frets, will be assigned by code dynamically during song based on distances from targets and other notes to play
var finger_target: Node3D 
#distance from the finger ik target to the guitar target which only the finger will move, if greater than this, move hand.
@export var finger_target_dist: float = 0.05 

#target Node3D on the guitar frets, will be assigned by code dynamically based on avg note distance for played note
var hand_target: Node3D 
#distance from the hand ik target to the hand guitar target which only the hand will move, if greater than this, move lowerarm.
@export var hand_target_dist: float = 0.1 

#target Node3D on the guitar frets, will be assigned by code dynamically based on avg note distance for played note
var lower_arm_target: Node3D 
#distance from the lowerarm ik target to the lowerarm guitar target which only the lowerarm will move, if greater than this, move upperarm? (might just use ik for whole arm).
@export var lower_arm_target_dist: float = 0.5 

func _process(delta: float) -> void:
	#if ik finger target global pos is not equal to the finger target (within half a cm) on the guitar and it's distance is <= finger target distance move
	if abs(global_position.distance_to(finger_target.global_position)) >= 0.005 && abs(global_position.distance_to(finger_target.global_position)) <= finger_target_dist:
		move_finger()

func move_finger():
	var scaling_factor = 0.01 #scalar to how much you want the half way point to move upward in between movements.
	
	var target_pos = finger_target.global_position
	var half_way = (global_position + finger_target.global_position) / 2
	
	var t = get_tree().create_tween()
	#t.tween_property(self, 'global_position', half_way + (owner.basis.y * scaling_factor), 0.1) #basis.y is 1 meter vector, 0.1 is duration
	t.tween_property(self, 'global_position', half_way + (global_basis.z * scaling_factor), 0.1) #basis.z is 1 meter vector, 0.1 is duration
	t.tween_property(self, 'global_position', target_pos, 0.1)
