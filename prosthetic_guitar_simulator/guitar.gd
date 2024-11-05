extends RigidBody3D

#useful website to help with notes on a guitar. remember no fret has all the default notes 
#(low6->E2 (means octave 2 with fret not held), A2, D3, G3, B3, E4) each fret towards
#guitar base goes a half step higher in pitch, each fret towards the string tighteners goes a step lower.
#fret 12 is an octave higher than default pitches. every 12 frets is similar
#https://fretmap.app/scales/c-major-scale/position-5


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func get_guitar_target(target_path: NodePath):
	var target: Node3D = get_node(target_path)
	return target

#function to get the average position of the notes that the player must play at the same time. useful for positioning the hand closest to notes
func avg_note_position(note_positions: Array):
	var avg_note_position = Vector3()
	for note_position in note_positions:
		avg_note_position += note_position
	return avg_note_position

#FIXME this one is not going to work, it will need modification to allow for hand to actually get to position properly...
func get_lower_arm_target(note_position: Vector3):
	var min_distance = 100000.0 #could be bad if this is not max always...
	var closest_position = Vector3()
	#get the minimum distance between the avg note position and the hand targets and return that hand target.
	for node in $LowerArm_Target.get_children():
		var distance = note_position - node.position
		if min_distance > distance:
			min_distance = distance
			closest_position = node.position
	return closest_position

func get_hand_target(avg_note_position: Vector3):
	var min_distance = 100000.0 #could be bad if this is not max always...
	var closest_position = Vector3()
	#get the minimum distance between the avg note position and the hand targets and return that hand target.
	for node in $LHand_Target.get_children():
		var distance = avg_note_position - node.position
		if min_distance > distance:
			min_distance = distance
			closest_position = node.position
	return closest_position
	
func get_all_children(node) -> Array:
	var nodes : Array = []
	for N in node.get_children():
		if N.get_child_count() > 0:
			nodes.append(N)
			nodes.append_array(get_all_children(N))
		else:
			nodes.append(N)
	return nodes
