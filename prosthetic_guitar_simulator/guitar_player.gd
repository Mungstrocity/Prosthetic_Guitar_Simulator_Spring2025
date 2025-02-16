extends Node3D

@export var player_move_speed = 5.0

#main guitar player script.

#read and parse the music xml file useing godot XML parser to get the number of total quarter note beats (inlcuding rests) in the song, tempo,
#notes (inlcuding their length*take length as a fraction of quarternote length and convert to seconds*, 
#pitch *convert this to guitar string and fret, if accidental sharp or flat convert to regular notes*, 
#and position in the song the start time and end time in seconds from song start), 
#add dynamics support. 

#parsed parts should include musicXML dynamics, pitch(inlcudes note and octave), measure maybe? (again probly good for looking ahead?)
#duration (not sure about what this means...) and type of beat (quarter, eighth, etc...),
#notations maybe? (tell you if the notes are tied to others or not... should be useful for looking ahead
#the only notes that need to be looked ahead at are probably checking for chords, eighths or quicker until you get to really fast tempos)

#audio could use the output midi file instead of generated music worst case. but it would be piano music...

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Set left hand IK targets to corresponding guitar targets
	get_left_ik_target(Finger.INDEX).set_finger_target(get_left_target(6, 10, true)) # example for string 6, fret 10
	get_left_ik_target(Finger.MIDDLE).set_finger_target(get_left_target(5, 10, true)) # example for string 5, fret 10
	get_left_ik_target(Finger.RING).set_finger_target(get_left_target(4, 11, true)) # example for string 4, fret 11
	get_left_ik_target(Finger.PINKY).set_finger_target(get_left_target(3, 11, true)) # example for string 3, fret 11

	# Set right hand IK targets to corresponding guitar targets (string only)
	get_right_ik_target(Finger.INDEX).set_finger_target(get_right_target(5, true)) # example for string 5
	get_right_ik_target(Finger.MIDDLE).set_finger_target(get_right_target(4, true)) # example for string 4
	get_right_ik_target(Finger.RING).set_finger_target(get_right_target(3, true)) # example for string 3
	get_right_ik_target(Finger.PINKY).set_finger_target(get_right_target(2, true)) # example for string 2
	get_right_ik_target(Finger.THUMB).set_finger_target(get_right_target(6, true)) # example for string 6
	
	# Connect signals for each string and fret collider to their respective handlers
	for i in righthand_string_colliders.size():
		righthand_string_colliders[i].connect("body_shape_entered", _on_right_finger_pick.bind(righthand_string_colliders[i]))

	for i in lefthand_string_colliders.size():
		lefthand_string_colliders[i].connect("body_shape_entered", _on_left_finger_press.bind(lefthand_string_colliders[i]))
		lefthand_string_colliders[i].connect("body_shape_exited", _on_left_finger_release.bind(lefthand_string_colliders[i]))
	
	for i in fret_colliders.size():
		fret_colliders[i].connect("body_shape_entered", _on_fret_collison.bind(fret_colliders[i]))
		fret_colliders[i].connect("body_shape_exited", _on_fret_release.bind(fret_colliders[i]))

# Called every frame. 'delta' is the elapsed time since the previous frame.
#so i think i am going to get the notes here, and send the notes to the fingers here as i step through the song.
#I will also need to make about 10 animations for the frets (focus more on the upper fret ones with more space between) 
#and i will select the animation based on the smallest distance from the middle string on each fret to the average 
#note position for each strum. each finger will then select it's note based on minimum distance traveled or on inital hand placement.
#strums of the right hand will also be initialized here based on the notes passed to the left hand.

func get_closest_fret_animation():
	#get the base animation which is closest to the average note to be played
	pass

# Base paths for left and right hands
@onready var left_finger_iktarget = $"Armature/Skeleton3D/LCollar_Attach/LUpperArm_Attach/LLowerArm_Attach/LHand_Attach/Target"
@onready var right_finger_iktarget = $"Armature/Skeleton3D/RCollar_Attach/RUpperArm_Attach/RLowerArm_Attach/RHand_Attach/Target"

@onready var left_finger_hover_gtarget = $"Guitar/LFingers/Hover"
@onready var left_finger_target_gtarget = $"Guitar/LFingers/Target"

@onready var right_finger_hover_gtarget = $"Guitar/RFingers/Hover"
@onready var right_finger_target_gtarget = $"Guitar/RFingers/Target"

# Constants for easy indexing
enum Finger { THUMB, INDEX, MIDDLE, RING, PINKY }

# Functions to get IK finger targets
func get_left_ik_target(finger) -> Node:
	return left_finger_iktarget.get_child(int(finger))

func get_right_ik_target(finger) -> Node:
	return right_finger_iktarget.get_child(int(finger))

#functions to get the guitar finger targets
func get_left_target(string_num: int, fret_num: int, hover: bool = false) -> Node:
	var target_root =  left_finger_hover_gtarget if hover else left_finger_target_gtarget
	return target_root.get_child(string_num - 1).get_child(fret_num - 1)

func get_right_target(string_num: int, hover: bool = false) -> Node:
	var target_root =  right_finger_hover_gtarget if hover else right_finger_target_gtarget
	return target_root.get_child(string_num - 1)

@onready var guitar = $"./Guitar"
@onready var guitar_sounds = $"./Guitar/GuitarSounds"
@onready var lefthand_string_colliders = guitar.get_child(1).get_child(1).get_children()
@onready var righthand_string_colliders = guitar.get_child(1).get_child(0).get_children()
@onready var fret_colliders = guitar.get_child(2).get_children()

#function to get the average position of the note 3D node targets that the player must play at the same time. useful for positioning the hand closest to notes
func get_avg_note_position(note_positions: Array) -> Vector3:
	var num_notes = note_positions.size()
	if num_notes == 0:
		return Vector3.ZERO  # Return a default position if no notes are provided

	var avg_note_position = Vector3.ZERO
	for note in note_positions:
		avg_note_position += note.global_transform.origin  # Assuming `note` is a 3D node

	avg_note_position /= float(num_notes)
	return avg_note_position
	
func get_avg_fret_from_notes(chosen_notes_array):
	var avg_fret = 0
	var num_notes = chosen_notes_array.size()
	for note in chosen_notes_array.size():
		if chosen_notes_array[note]["fret"] == 0: #no left press required; open string
			num_notes -= 1
			continue #skip this and don't put it into the calculation
		avg_fret += chosen_notes_array[note]["fret"]
	if num_notes != 0:
		avg_fret /= num_notes
	else:
		avg_fret = 0 #avg fret doesn't matter becauase no notes need the left hand
	return avg_fret
	
func get_lowest_fret_from_notes(chosen_notes_array):
	var lowest_fret = 0
	var num_notes = chosen_notes_array.size()
	for note in chosen_notes_array.size():
		if chosen_notes_array[note]["fret"] == 0: #no left press required; open string
			num_notes -= 1
			continue #skip this and don't assign it
		lowest_fret = chosen_notes_array[note]["fret"]
		break #first one should be lowest fret so get out of here
	if num_notes == 0: #counter for non-openstring notes, so if only open string notes
		lowest_fret = 0 #lowest fret doesn't matter becauase no notes need the left hand
	return lowest_fret
	

#array is of this type possible_positions[position][dict_key] inside the dict there are keys, string, fret. 
#The right hand will use the string associated with the note
#get an array of all possible positions in the guitar for that pitch and octave on the guitar
const STRING_TUNINGS = [
	{"string": 6, "note": "E", "octave": 2}, # E2
	{"string": 5, "note": "A", "octave": 2}, # A2
	{"string": 4, "note": "D", "octave": 3}, # D3
	{"string": 3, "note": "G", "octave": 3}, # G3
	{"string": 2, "note": "B", "octave": 3}, # B3
	{"string": 1, "note": "E", "octave": 4}  # E4
]

const SEMITONES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Convert a note (pitch, octave, alter) to a MIDI number
func note_to_midi(pitch: String, octave: int, alter: int) -> int:
	var base_index = SEMITONES.find(pitch)
	if base_index == -1:
		assert(false, "Invalid pitch: %s" % pitch)
	return (octave + 1) * 12 + base_index + alter

# Convert a MIDI number to a note (pitch, octave)
func midi_to_note(midi: int) -> Dictionary:
	var pitch = SEMITONES[midi % 12]
	var octave = (midi / 12) - 1
	return {"pitch": pitch, "octave": octave}

# Generate all possible positions for a note
func get_pos_finger_positions(octave: int, pitch: String, alter: int) -> Array:
	var target_midi = note_to_midi(pitch, octave, alter)
	var possible_positions = []

	for tuning in STRING_TUNINGS:
		var string_open_midi = note_to_midi(tuning["note"], tuning["octave"], 0)
		var fret = target_midi - string_open_midi
		if fret >= 0 && fret <= 20: # Assuming 20 frets
			possible_positions.append({"string": tuning["string"], "fret": fret})
	
	return add_finger_targets_to_array(possible_positions)

func add_finger_targets_to_array(possible_finger_positions):
	for pos_position in possible_finger_positions.size():
		var string = int(possible_finger_positions[pos_position]["string"])
		var fret = int(possible_finger_positions[pos_position]["fret"])
		possible_finger_positions[pos_position]["left-hover"] = get_left_target(string,fret,true)
		possible_finger_positions[pos_position]["left"] = get_left_target(string,fret,false)
		possible_finger_positions[pos_position]["right-hover"] = get_right_target(string,true)
		possible_finger_positions[pos_position]["right"] = get_right_target(string, false)
	return possible_finger_positions

#there will be an analyzer function for chosing fingers for each beat (multi note and single note ones) which is described below
#analyze the next notes to see how many notes need to be played at the same time
#make a target grouping for all notes to be played at the same time
#start with the lowest pitch note (of the notes about to be played at the same time in one beat) 
#check the finger - note count weight dict to see if from previous notes in the measure it's not one of the 
#higher weights for a finger in this measure,
#and if so, see if another finger can play that note by checking num notes played at once, else if another can't, assign the target anyways
#check it's note count (which represents the weighting of preference to move that finger or not, 
#the higher the note count in the measure, the lower the preference to move that finger from it's position, 
#and the more priority is given to moving higher pitch fingers if it's possible to still play all the other notes without moving) 
#in the measure passed in from the measure analyzer and if it's greater than 1, 
#assign a chosen finger to the measure analyzer dict to associate it with the weight, usually index finger since it's the lowest note, 
#and get all possible positions of it down the neck. 
#Then move to the next finger middle and choose the next lowest note (if there is one available to be played at the same time), 
#and pick all the positions down the neck for the next note 
#with the condition that they can only be higher or the same fret as the index frets with a max spacing down the neck of 2 additonal frets. 
#Then do the same for the next fingers. then once all the fingers have all those possible postions, find the fingering group with 
#the minimal total distance between it's average note, and the previous played average note (or fret1 if first note)
#also note (3 fret spacing max) and return that array or dict of the chosen fingering for that multi-note. 
#return it in a dict of stringnum?: fretnum?
# or even better just return a dict with the finger number as the key, then the target string number and fret number as another dict inside.

func select_finger_targets(note_array, prev_avg_fret: int = 10): #gets an array of the notes needed to be played in a beat
	var available_fingers = { #dictionary to store which fingers are used or not
		"INDEX": true,
		"MIDDLE": true,
		"RING": true,
		"PINKY": true
	}
	var num_notes = note_array.size()
	var lowest_note_in_group #for checking to make sure all subsequent notes are no more than 2 frets higher than this and none lower to make sure hand can play
	var num_possible_groups = 1
	var groups = [] #array to store all the note groupings
	var groups_valid = [] #stores booleans telling you if the group is a valid group or not
	for group in num_possible_groups: #iterate at min 1 time, depending on what the value gets set to later
		for note in num_notes:
			var note_possible_positions
			if note_array[note].has("octave") && note_array[note].has("step"): #check to make sure it's a note and not a rest etc.
				if note_array[note].has("alter"): #some notes don't have an alter element
					note_possible_positions = get_pos_finger_positions(note_array[note]["octave"], note_array[note]["step"], note_array[note]["alter"])
				else: #no alter so just put 0
					note_possible_positions = get_pos_finger_positions(note_array[note]["octave"], note_array[note]["step"], 0)
			else:# note doesn't have octave or step, probably not a note, might be a rest etc.
				push_warning("Warning: Note doesn't have an octave for choosing fingers. Might be a rest note?")
				continue #still might be more notes in beat so keep checking
			if note == 0: #first note, it's sorted so the first note is the lowest in the beat
				if note_possible_positions == null || note_possible_positions.size() == 0:
					break #no notes to play in beat, likey a rest beat
				num_possible_groups = note_possible_positions.size() #max number of groups can be the maxium number of lowest note positions
				for grp in num_possible_groups:
					groups_valid.append(true) #append the number of groups with true values as all groups start as valid groups.
				lowest_note_in_group = note_possible_positions[group] #get the lowest note position info for the group that it is on.
				groups.append([lowest_note_in_group])
			else:
				var found_pos = false
				for pos in note_possible_positions.size():
					if note_possible_positions[pos]["fret"] <= lowest_note_in_group["fret"] + 2 && note_possible_positions[pos]["fret"] >= lowest_note_in_group["fret"]:
						groups[group].append(note_possible_positions[pos]) #append the note to the group
						found_pos = true
						break
				if !found_pos: #if you didn't find a valid position for a note, then the group won't work. set the group to be invalid, then break from the inner loop.
					groups_valid[group] = false
					break #break out of the inner loop to process the next group
	#might have to check for duplicate notes in group?
	
	#now see how many groups are left and choose which group is best one, and return it. use previous avg_fret if available else use default value 10
	var closest_group_to_last_beat
	var min_fret_dist = 20 #set to max
	for group in groups.size():
		if groups_valid[group] == true:
			var dist = abs(prev_avg_fret - groups[group][0]["fret"])
			if dist <= min_fret_dist: #get the lowest note in the group and compare it to last avg_fret to find min
				closest_group_to_last_beat = groups[group]
				min_fret_dist = dist
				
	if closest_group_to_last_beat == null:
		push_warning("Warning: No Groups found, might need to expand finger mapping conditions.")
		print(groups)
	return closest_group_to_last_beat
#i don't think i have time to implement this right now.
#But there is also a measure analyzer dict which will count the number of note occurances during the measure, 
#and it will try to map the same fingers to the same notes over and over based on number of reocurrances 
#and if it's a higher or lower pitch (for choosing right finger to play it) while spreading out the burden of other frets 
#to other fingers

#define dicts to keep finger: string (or fret) pairs for right hand checks
var lhand_dict = {}

func _on_right_finger_pick(_body_rid: RID, _finger_collider_node: Node3D, _body_shape_index: int, _local_shape_index: int, string_collider_node):
	#print("got right finger signal!")
	#print(string_collider_node.name)
	#print(_finger_collider_node.name)
	for finger in lhand_dict.keys():
		#check for errors where the finger has only a fret or only a string etc...
		if !(lhand_dict[finger].has("string") && lhand_dict[finger].has("fret")):
			if !(lhand_dict[finger].has("string")):
				push_warning(str("Finger: ", finger, " Doesn't have a stored string but is still in the lhand_dict!"))
			if !(lhand_dict[finger].has("fret")):
				push_warning(str("Finger: ", finger, " Doesn't have a stored fret but is still in the lhand_dict!"))
			continue #the finger doesn't have a string or fret collision, shouldn't be needed tho because it removes uncoliding fingers.
		
		#check for modified notes with the left fingers
		if lhand_dict[finger]["string"] == string_collider_node.name && lhand_dict[finger].has("fret"):
			
			#Also check if the fret is a higher number in the case of the same string being pressed down with two fingers!
			var finger_string_dict = {} #check dict
			var finger_press_collision = false
			for finger_ in lhand_dict.keys():
				if !lhand_dict[finger_].has("string"):
					#check to make sure it has string element, it should but due to collisions buggin out it might not
					push_warning("Skipping collision check due to no string element in dictionary.")
					continue #if not, jump to the next finger, effectively ignoring bugged one
				if finger_string_dict.has(lhand_dict[finger_]["string"]): #means there is two left hand fingers pressing the same string
					#do check to find which fret is greater on the string, and the greater one, put in the dict
					finger_press_collision = true
					var present_finger = finger_string_dict[lhand_dict[finger_]["string"]] #returns the finger in the check dictionary
					var checking_finger = finger_ #returns the finger we are iterating through
					print("present_finger" + present_finger)
					print("checking_finger" + checking_finger)
					# now check which one is a greater fret value to keep
					if present_finger < checking_finger:
						# checking finger fret value is a larger fret so replace present finger
						finger_string_dict[lhand_dict[finger_]["string"]] = checking_finger
				else: # populate the check dictionary when no collision is detected
					#puts the string as the key, and the finger_ as the value
					finger_string_dict[lhand_dict[finger_]["string"]] = finger_
			
			if finger_press_collision:
				#see which fingers collided, and which ones are still in the check dict,
				#if the finger value is not still in the check dict, don't play the note
				var string_key = finger_string_dict.find_key(str(finger))
				print(string_key)
				if (string_key != null): #key is found in the check dict for the associated finger value
					#play note
					print(finger_string_dict)
					guitar_sounds.play_note(string_collider_node.name, lhand_dict[finger_string_dict[string_key]]["fret"]) #play the highest note finger in the string
					return
				else:
					#don't play note because it is lower fret than another and was overwritten and continue looping through other fingers
					continue
			#the note will be modified before play based on the left hand
			guitar_sounds.play_note(string_collider_node.name, lhand_dict[finger]["fret"])
			return
	#if you got through and there wasn't a left hand string that matched, play basic note
	guitar_sounds.play_note(string_collider_node.name, "")
	return
	
func _on_left_finger_press(_body_rid: RID, finger_collider_node: Node3D, _body_shape_index: int, _local_shape_index: int, string_collider_node):
	print("\ngot left string press signal!")
	print(string_collider_node.name)
	print(finger_collider_node.name)
	if !lhand_dict.has(finger_collider_node.name):
		lhand_dict[finger_collider_node.name] = {}
	lhand_dict[finger_collider_node.name]["string"] = string_collider_node.name
	return
	
func _on_left_finger_release(_body_rid: RID, finger_collider_node: Node3D, _body_shape_index: int, _local_shape_index: int, _string_collider_node):
	print("\ngot left string release signal!")
	if(lhand_dict.has(finger_collider_node.name)):
		lhand_dict[finger_collider_node.name].erase("string")
		if lhand_dict[finger_collider_node.name].is_empty(): #check if it's the last one
			lhand_dict.erase(finger_collider_node.name)
	return 
	
func _on_fret_collison(_body_rid: RID, finger_collider_node: Node3D, _body_shape_index: int, _local_shape_index: int, fret_collider_node):
	print("\ngot fret press signal!")
	print(fret_collider_node.name)
	print(finger_collider_node.name)
	if !lhand_dict.has(finger_collider_node.name):
		lhand_dict[finger_collider_node.name] = {}
	lhand_dict[finger_collider_node.name]["fret"] = fret_collider_node.name
	return
	
func _on_fret_release(_body_rid: RID, finger_collider_node: Node3D, _body_shape_index: int, _local_shape_index: int, _fret_collider_node):
	print("\ngot fret release signal!")
	if(lhand_dict.has(finger_collider_node.name)):
		lhand_dict[finger_collider_node.name].erase("fret")
		if lhand_dict[finger_collider_node.name].is_empty(): #check if it's the last one
			lhand_dict.erase(finger_collider_node.name)
	return 
