extends Node

@onready var anim = $"../"
@onready var gp = $"../../"
@onready var printer = gp.lhand_dict

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
var fret_presses = [false, false, false, false]
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
	if Input.is_action_just_released("fretpress1"):
		if fret_presses[0] == false:
			fret_presses[0] = true
			gp.get_left_ik_target(gp.Finger.INDEX).set_finger_target(gp.get_left_target(gp.Finger.INDEX, 5, 10, false)) # example for string 6, fret 10
		else:
			fret_presses[0] = false
			gp.get_left_ik_target(gp.Finger.INDEX).set_finger_target(gp.get_left_target(gp.Finger.INDEX, 5, 10, true)) # example for string 6, fret 10

		pass
	if Input.is_action_just_released("fretpress2"):
		if fret_presses[1] == false:
			fret_presses[1] = true
			gp.get_left_ik_target(gp.Finger.MIDDLE).set_finger_target(gp.get_left_target(gp.Finger.MIDDLE, 5, 11, false)) # example for string 5, fret 10
		else:
			fret_presses[1] = false
			gp.get_left_ik_target(gp.Finger.MIDDLE).set_finger_target(gp.get_left_target(gp.Finger.MIDDLE, 5, 11, true)) # example for string 5, fret 10

		pass
	if Input.is_action_just_released("fretpress3"):
		if fret_presses[2] == false:
			fret_presses[2] = true
			gp.get_left_ik_target(gp.Finger.RING).set_finger_target(gp.get_left_target(gp.Finger.RING, 2, 11, false)) # example for string 4, fret 11
		else:
			fret_presses[2] = false
			gp.get_left_ik_target(gp.Finger.RING).set_finger_target(gp.get_left_target(gp.Finger.RING, 2, 11, true)) # example for string 4, fret 11
		pass
	if Input.is_action_just_released("fretpress4"):
		if fret_presses[3] == false:
			fret_presses[3] = true
			gp.get_left_ik_target(gp.Finger.PINKY).set_finger_target(gp.get_left_target(gp.Finger.PINKY, 1, 11, false)) # example for string 3, fret 11		
		else:
			fret_presses[3] = false
			gp.get_left_ik_target(gp.Finger.PINKY).set_finger_target(gp.get_left_target(gp.Finger.PINKY, 1, 11, true)) # example for string 3, fret 11		
		pass
	if Input.is_action_just_pressed("strum_up"):
		for finger in 5:
			gp.get_right_ik_target(finger).set_finger_target(gp.get_right_target(finger, 6-(finger), false))
			await get_tree().create_timer(0.1).timeout
			gp.get_right_ik_target(finger).set_finger_target(gp.get_right_target(finger, 6-(finger), true))
		#dont forget the final string!
		gp.get_right_ik_target(4).set_finger_target(gp.get_right_target(4, 1, false))
		await get_tree().create_timer(0.1).timeout
		gp.get_right_ik_target(4).set_finger_target(gp.get_right_target(4, 2, true))
		pass
	if Input.is_action_just_pressed("strum_down"):
		gp.get_right_ik_target(4).set_finger_target(gp.get_right_target(4, 1, false))
		await get_tree().create_timer(0.1).timeout
		gp.get_right_ik_target(4).set_finger_target(gp.get_right_target(4, 1, true))
		for finger in 5:
			gp.get_right_ik_target(4-finger).set_finger_target(gp.get_right_target(4-finger, 2+(finger), false))
			await get_tree().create_timer(0.1).timeout
			gp.get_right_ik_target(4-finger).set_finger_target(gp.get_right_target(4-finger, 2+(finger), true))
		pass
	if Input.is_action_just_pressed("print"):
		print(printer)
	pass
