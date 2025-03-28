extends Node3D

#script attached to the finger IK targets

#target Node3D on the guitar frets, will be assigned by code dynamically during song based on distances from targets and other notes to play
var finger_target: Node3D 
# minimum allowable distance from the finger ik target to the guitar target.
#@export var finger_target_dist: float = 0.0001 

var finger_moving = false

func _ready() -> void:
	pass

func _process(delta: float) -> void:
	#if ik finger target global pos is not equal to the finger target (within half a cm) on the guitar and it's distance is <= finger target distance move
	if finger_target != null && !finger_moving && (global_position.distance_to(finger_target.global_position)) != 0.0:
		move_finger()
	pass

func set_finger_target(target: Node3D):
	finger_target = target

func move_finger():
	#var scaling_factor = 0.1 #scalar to how much you want the half way point to move upward in between movements.
	
	var target_pos = finger_target.global_position
	#var half_way = (global_position + finger_target.global_position) / 2
	
	finger_moving = true
	var t = get_tree().create_tween()
	
	t.connect("finished", Callable(self, "_on_tween_complete"))
	
	#t.tween_property(self, 'global_position', half_way + (owner.basis.y * scaling_factor), 0.1) #basis.y is 1 meter vector, 0.1 is duration
	#t.tween_property(self, 'global_position', half_way + (global_basis.z * scaling_factor), 0.1) #basis.z is 1 meter vector, 0.1 is duration
	
	#0.05 is the speed that fingers move to the target, they move their in 0.05 seconds, i find it looks a bit fast and that 0.1 is the smoothest, but 0.4 seconds is too long to have to wait.
	t.tween_property(self, 'global_position', target_pos, 0.05)
	
func _on_tween_complete():
	finger_moving = false
