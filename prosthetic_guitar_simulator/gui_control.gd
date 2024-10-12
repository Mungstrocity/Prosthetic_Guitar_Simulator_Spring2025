extends Control  # The root of your main menu

func _on_start_button_pressed() -> void:
	$MusicXMLParser.parseMusicXML()	
	# Change to the new 3D scene
	get_tree().change_scene_to_file("res://Main3dScene.tscn")
