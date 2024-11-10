extends Control  # The root of your main menu

#starts the simulation
func _on_start_button_pressed() -> void:
	#Extracts the songData into the form {element_name: [{attribute_name: attribute}, {data_name/child_name: data/child}]} 
	#if it's the measures or notes scope, measures use the naming "m#,node_name" while if also in the note scope inside a measure, 
	#the convention is "m#,n#,node_name"
	var songData = $MusicXMLParser.parse_music_XML()	
	
	# Change to the new 3D scene
	get_tree().change_scene_to_file("res://Main3dScene.tscn")
	
	#$MusicXMLParser/MusicXMLParserTest.test_XML_parse(songData)

	
