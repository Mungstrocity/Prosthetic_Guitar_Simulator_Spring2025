extends Marker3D

#target Node3D on the guitar frets, will be assigned by code dynamically based on avg note distance for played note
var hand_target: Node3D 
#distance from the hand ik target to the hand guitar target which only the hand will move, if greater than this, move lowerarm.
@export var hand_target_dist: float = 0.1 

func _process(delta: float) -> void:
	#if ik finger target global pos is not equal to the finger target (within half a cm) on the guitar and it's distance is <= finger target distance move
	if abs(global_position.distance_to(hand_target.global_position)) >= 0.005 && abs(global_position.distance_to(hand_target.global_position)) <= hand_target_dist:
		move_hand()

func move_hand():
	
	var target_pos = hand_target.global_position
	
	var t = get_tree().create_tween()
	#no movement besides the straight line needed for hand.
	t.tween_property(self, 'global_position', target_pos, 0.2)
