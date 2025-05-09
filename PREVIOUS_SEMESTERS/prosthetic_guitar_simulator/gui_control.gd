extends Control  # The root of your main menu

#starts the simulation
func _on_start_button_pressed() -> void:
	
	# Change to the new 3D scene
	get_tree().change_scene_to_file("res://Main3dScene.tscn")
	

	
