extends Node

@onready var anim = $"../"
@onready var gp = $"../../"

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	anim.play("guitarPoses/Larm_fret10")
	anim.play("guitarPoses/Rarm_pickPos1")
	pass # Replace with function body.

	# Set left hand IK targets to corresponding guitar targets
	#gp.get_left_ik_target(gp.Finger.INDEX).set_finger_target(gp.get_left_target(gp.Finger.INDEX, 6, 10, true)) # example for string 6, fret 10
	#gp.get_left_ik_target(gp.Finger.MIDDLE).set_finger_target(gp.get_left_target(gp.Finger.MIDDLE, 5, 10, true)) # example for string 5, fret 10
	#gp.get_left_ik_target(gp.Finger.RING).set_finger_target(gp.get_left_target(gp.Finger.RING, 4, 11, true)) # example for string 4, fret 11
	#gp.get_left_ik_target(gp.Finger.PINKY).set_finger_target(gp.get_left_target(gp.Finger.PINKY, 3, 11, true)) # example for string 3, fret 11

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if !Input.is_action_pressed("ctrl") && Input.is_action_pressed("fret1"):
		anim.play("guitarPoses/Larm_fret1")
		if(!anim.is_playing()):
			anim.stop()
	if !Input.is_action_pressed("ctrl") && Input.is_action_pressed("fret5"):
		anim.play("guitarPoses/Larm_fret5")
		if(!anim.is_playing()):
			anim.stop()
	if !Input.is_action_pressed("ctrl") && Input.is_action_pressed("fret10"):
		anim.play("guitarPoses/Larm_fret10")
		if(!anim.is_playing()):
			anim.stop()
	if !Input.is_action_pressed("ctrl") && Input.is_action_pressed("fret16"):
		anim.play("guitarPoses/Larm_fret16")
		if(!anim.is_playing()):
			anim.stop()
	if !Input.is_action_pressed("ctrl") && Input.is_action_pressed("fret20"):
		anim.play("guitarPoses/Larm_fret20")	
		if(!anim.is_playing()):
			anim.stop()
	if Input.is_action_just_pressed("playS1"):
		gp.get_right_ik_target(gp.Finger.PINKY).set_finger_target(gp.get_right_target(gp.Finger.PINKY, 1, false)) # example for string 2
		pass
	if Input.is_action_just_released("playS1"):
		gp.get_right_ik_target(gp.Finger.PINKY).set_finger_target(gp.get_right_target(gp.Finger.PINKY, 1, true)) # example for string 2
		pass
	if Input.is_action_just_pressed("playS2"):
		gp.get_right_ik_target(gp.Finger.PINKY).set_finger_target(gp.get_right_target(gp.Finger.PINKY, 2, false)) # example for string 2
		pass
	if Input.is_action_just_released("playS2"):
		gp.get_right_ik_target(gp.Finger.PINKY).set_finger_target(gp.get_right_target(gp.Finger.PINKY, 2, true)) # example for string 2
		pass
	if Input.is_action_just_pressed("playS3"):
		gp.get_right_ik_target(gp.Finger.RING).set_finger_target(gp.get_right_target(gp.Finger.RING, 3, false)) # example for string 3
		pass
	if Input.is_action_just_released("playS3"):
		gp.get_right_ik_target(gp.Finger.RING).set_finger_target(gp.get_right_target(gp.Finger.RING, 3, true)) # example for string 3
		pass
	if Input.is_action_just_pressed("playS4"):
		gp.get_right_ik_target(gp.Finger.MIDDLE).set_finger_target(gp.get_right_target(gp.Finger.MIDDLE, 4, false)) # example for string 4
		pass
	if Input.is_action_just_released("playS4"):
		gp.get_right_ik_target(gp.Finger.MIDDLE).set_finger_target(gp.get_right_target(gp.Finger.MIDDLE, 4, true)) # example for string 4
		pass
	if Input.is_action_just_pressed("playS5"):
		gp.get_right_ik_target(gp.Finger.INDEX).set_finger_target(gp.get_right_target(gp.Finger.INDEX, 5, false)) # example for string 5
		pass
	if Input.is_action_just_released("playS5"):
		gp.get_right_ik_target(gp.Finger.INDEX).set_finger_target(gp.get_right_target(gp.Finger.INDEX, 5, true)) # example for string 5
		pass
	if Input.is_action_just_pressed("playS6"):
		gp.get_right_ik_target(gp.Finger.THUMB).set_finger_target(gp.get_right_target(gp.Finger.THUMB, 6, false)) # example for string 6
		pass
	if Input.is_action_just_released("playS6"):
		gp.get_right_ik_target(gp.Finger.THUMB).set_finger_target(gp.get_right_target(gp.Finger.THUMB, 6, true)) # example for string 6
		pass
	
	
	pass
