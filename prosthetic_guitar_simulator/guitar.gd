extends RigidBody3D

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

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

#useful website to help with notes on a guitar. remember no fret has all the default notes 
#(low6->E2 (means octave 2 with fret not held), A2, D3, G3, B3, E4) each fret towards
#guitar base goes a half step higher in pitch, each fret towards the string tighteners goes a step lower.
#fret 12 is an octave higher than default pitches. every 12 frets is similar
#https://fretmap.app/scales/c-major-scale/position-5

#function to return the list of possible target nodes based on the passed in note parameters
#im thinking about doing a path finding algorithm or something to where you start with a note, then get all possible targets,
#then if you have more notes you are playing at the same time, you would pass in the array of an array of the previous note's targets
#then based on all the targets, you would find the most optimal targets to use with each other based on lowest minimal distances
#simulated annealing basically. (I might have to change this slightly and just go with a biased selection becuase that might take too much time)
func get_poss_gneck_targets(octave: int, pitch: String, alter: int, hover: bool):
	match octave:
		0: #Not playable on the guitar just play it on octave 2 and 3
			pass
		1: #Not playable on the guitar just play it on octave 2 and 3
			#left off on string 3 FIXME
			pass
		2: # S6: E2-F0 to B2-F7, S5: A2-F0 to B2-F2
			pass
		3: # S6: C3-F8 to B3-F19, S5: C3-F3 to B3-F14 S4: D3-F0 to B3-F9
			pass
		4: # S6: C4-F20, S5: C4-F15 to F4-F20 S4: C4-F10 to A#4-F20
			pass
		5:
			pass
		6: #   S1: C6-F20
			pass
		_:
			pass

func get_guitar_pick_target(guitar_string: int, hover: bool, other_note_targets: Array):
	match guitar_string:
		1:
			
			pass
		2:
			pass
		3:
			pass
		4:
			pass
		5:
			pass
		6:
			pass
		_:
			pass
