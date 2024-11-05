extends Node

@onready var anim = $"../"

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	anim.play("guitarPoses/Larm_fret10")
	anim.play("guitarPoses/Rarm_pickPos1")
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if Input.is_action_pressed("fret1"):
		anim.play("guitarPoses/Larm_fret1")
		if(!anim.is_playing()):
			anim.stop()
	if Input.is_action_pressed("fret5"):
		anim.play("guitarPoses/Larm_fret5")
		if(!anim.is_playing()):
			anim.stop()
	if Input.is_action_pressed("fret10"):
		anim.play("guitarPoses/Larm_fret10")
		if(!anim.is_playing()):
			anim.stop()
	if Input.is_action_pressed("fret16"):
		anim.play("guitarPoses/Larm_fret16")
		if(!anim.is_playing()):
			anim.stop()
	if Input.is_action_pressed("fret20"):
		anim.play("guitarPoses/Larm_fret20")	
		if(!anim.is_playing()):
			anim.stop()
		
	pass
