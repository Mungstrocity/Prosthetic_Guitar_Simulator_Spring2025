extends SkeletonIK3D

#script attached to the IK nodes

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Apply half IK effect
	set_influence(1.0)
	#start processing IK
	start()
	pass # Replace with function body.
