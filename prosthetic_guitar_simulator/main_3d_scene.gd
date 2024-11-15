extends Node

var songData
var processed_song

#use for changing dynamics only (tempororary until implementing dynamics based on velocity of fingers)
@onready var guitar_sounds_node = $".GuitarPlayer/GuitarPlayer/Guitar/GuitarSounds"

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	#Extracts the songData into the form {element_name: [{attribute_name: attribute}, {data_name/child_name: data/child}]} 
	#if it's the measures or notes scope, measures use the naming "m#,node_name" while if also in the note scope inside a measure, 
	#the convention is "m#,n#,node_name"
	songData = $MusicXMLParser.parse_music_XML()	
	$MusicXMLParser/MusicXMLParserTest.test_XML_parse(songData)
	
	#processed_song = process_song_data()
	
	#play_song(processed_song)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	handle_cams()
	pass

func handle_cams():
	var cameras = [
		get_node("Cameras/MainCamera"),
		get_node("Cameras/FreeLookCam"),
		get_node("Cameras/GuitarNeckCamera"),
		get_node("Cameras/GuitarNeckCamera2"),
		get_node("Cameras/GuitarNeckCamera3"),
		get_node("Cameras/GuitarNeckCamera4"),
		get_node("Cameras/GuitarNeckCamera5"),
		get_node("Cameras/GuitarNeckCamera6"),
		get_node("Cameras/GuitarNeckCamera7"),
		get_node("Cameras/GuitarNeckCamera8")
	]
	
	if Input.is_action_just_pressed("cycleCam"):
		for i in range(cameras.size()):
			if cameras[i].is_current():
				cameras[i].clear_current(true)
				# Set the next camera in the array as the current one, looping back to the first camera
				var next_index = (i + 1) % cameras.size()
				cameras[next_index].make_current()
				break

#make song data usable by the guitar player and make it more sequential.
func process_song_data():
		#measure booleans
	var attributes = false #if attributes are detected
	var direction = false #if direction elements are detected
	for element in songData.keys():
		
		#all elements that are measure and note specific should be extracted here in order.
		if element.contains("measure"): #start of a new measure
			pass
	pass

#now with the processed song data, play the song by controlling the guitar player
func play_song():
	pass
	
#inside attributes, divisions tells you how many divisions there are in a basic beat unit (ex: quarter note divisions for 4:4 time)
#then, duration data tells you how many divisions there are in the note (so how long to play it)
#to get the length of a single division, take per-minute (bmp) in direction tag and do
# 60seconds/(per-minute * divisions) = seconds per division.
#then for duration in seconds, do
# seconds to play note = duration * seconds per division
func note_duration_in_sec(per_minute: int, divisions: int, duration: int):
	var seconds_per_division = 60/(per_minute * divisions)
	var seconds_to_play = seconds_per_division * duration
	return seconds_to_play
