extends CharacterBody3D

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
#


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Set left hand IK targets to corresponding guitar targets
	get_left_ik_target(Finger.INDEX).set_finger_target(get_left_target(Finger.INDEX, 6, 10, true)) # example for string 6, fret 10
	get_left_ik_target(Finger.MIDDLE).set_finger_target(get_left_target(Finger.MIDDLE, 5, 10, true)) # example for string 5, fret 10
	get_left_ik_target(Finger.RING).set_finger_target(get_left_target(Finger.RING, 4, 11, true)) # example for string 4, fret 11
	get_left_ik_target(Finger.PINKY).set_finger_target(get_left_target(Finger.PINKY, 3, 11, true)) # example for string 3, fret 11

	# Set right hand IK targets to corresponding guitar targets (string only)
	get_right_ik_target(Finger.INDEX).set_finger_target(get_right_target(Finger.INDEX, 5, true)) # example for string 5
	get_right_ik_target(Finger.MIDDLE).set_finger_target(get_right_target(Finger.MIDDLE, 4, true)) # example for string 4
	get_right_ik_target(Finger.RING).set_finger_target(get_right_target(Finger.RING, 3, true)) # example for string 3
	get_right_ik_target(Finger.PINKY).set_finger_target(get_right_target(Finger.PINKY, 2, true)) # example for string 2
	get_right_ik_target(Finger.THUMB).set_finger_target(get_right_target(Finger.THUMB, 6, true)) # example for string 6
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#so i think i am going to get the notes here, and send the notes to the fingers here as i step through the song.
#I will also need to make about 10 animations for the frets (focus more on the upper fret ones with more space between) 
#and i will select the animation based on the smallest distance from the middle string on each fret to the average 
#note position for each strum. each finger will then select it's note based on minimum distance traveled or on inital hand placement.
#strums of the right hand will also be initialized here based on the notes passed to the left hand.
func _process(delta: float) -> void:
	pass

func get_closest_fret_animation():
	#get the base animation which is closest to the average note to be played
	pass

# Base paths for left and right hands
@onready var left_finger_iktarget = $"Armature/Skeleton3D/LCollar_Attach/LUpperArm_Attach/LLowerArm_Attach/LHand_Attach"
@onready var right_finger_iktarget = $"Armature/Skeleton3D/RCollar_Attach/RUpperArm_Attach/RLowerArm_Attach/RHand_Attach"

@onready var left_finger_hover_gtarget = $"Guitar/LFingers/Hover"
@onready var left_finger_target_gtarget = $"Guitar/LFingers/Target"

@onready var right_finger_hover_gtarget = $"Guitar/RFingers/Hover"
@onready var right_finger_target_gtarget = $"Guitar/RFingers/Target"

# Constants for easy indexing
enum Finger { INDEX, MIDDLE, RING, PINKY, THUMB }

# Functions to get IK targets
func get_left_ik_target(finger: Finger) -> Node:
	return left_finger_iktarget.get_child(int(finger))

func get_right_ik_target(finger: Finger) -> Node:
	return right_finger_iktarget.get_child(int(finger))

func get_left_target(finger: Finger, string_num: int, fret_num: int, hover: bool = false) -> Node:
	var target_root =  left_finger_hover_gtarget if hover else left_finger_target_gtarget
	return target_root.get_child(string_num - 1).get_child(fret_num - 1)

func get_right_target(finger: Finger, string_num: int, hover: bool = false) -> Node:
	var target_root =  right_finger_hover_gtarget if hover else right_finger_target_gtarget
	return target_root.get_child(string_num - 1)
