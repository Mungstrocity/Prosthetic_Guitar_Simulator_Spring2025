extends SkeletonIK3D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Apply half IK effect
	set_influence(0.7)
	#start processing IK
	start()
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
