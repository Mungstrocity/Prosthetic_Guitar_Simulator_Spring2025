extends Marker3D

#target Node3D on the guitar frets, will be assigned by code dynamically based on avg note distance for played note
var lower_arm_target: Node3D 
#distance from the lowerarm ik target to the lowerarm guitar target which only the lowerarm will move, if greater than this, move upperarm? (might just use ik for whole arm).
@export var lower_arm_target_dist: float = 0.5 

func _process(delta: float) -> void:
	#if ik finger target global pos is not equal to the finger target (within half a cm) on the guitar and it's distance is <= finger target distance move
	if abs(global_position.distance_to(lower_arm_target.global_position)) >= 0.005 && abs(global_position.distance_to(lower_arm_target.global_position)) <= lower_arm_target_dist:
		move_arm()

func move_arm():
	
	var target_pos = lower_arm_target.global_position
	
	var t = get_tree().create_tween()
	#no movement besides the straight line needed for hand.
	t.tween_property(self, 'global_position', target_pos, 0.1)
