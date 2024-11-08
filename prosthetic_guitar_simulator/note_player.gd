extends Node

#video on godot sound players
#https://www.youtube.com/watch?v=h3_1dfPHXDg&ab_channel=GameDevArtisan

#interactive stream player:
#https://docs.godotengine.org/en/stable/classes/class_audiostreaminteractive.html

# A list to store the active AudioStreamPlayer nodes for polyphony
var active_notes: Array = []

# Configurable parameters
@export var sustain_time: float = 1.0  # Default sustain time in seconds
@export var volume_db: float = -6.0    # Default volume in dB

# Load your audio samples here
@export var note_streams: Array = []

func _ready():
	# Create an AudioStreamPlayer for each note in note_streams
	for note_stream in note_streams:
		var player = AudioStreamPlayer.new()
		player.stream = note_stream
		player.volume_db = volume_db
		add_child(player)
		play_note(1)

func _process(delta: float) -> void:
	#play_note(1)
	pass

# Function to play a note
func play_note(index: int) -> void:
	# Ensure index is valid
	if index < 0 or index >= note_streams.size():
		return
	
	var player = get_child(index) as AudioStreamPlayer
	
	# Reset player if it's already playing (for retriggering)
	if player.playing:
		player.stop()
	
	# Adjust volume and play
	player.volume_db = volume_db
	player.play()
	
	# Schedule to stop the note after the sustain time
	await get_tree().create_timer(sustain_time).timeout
	player.stop()

# Function to adjust sustain time
func set_sustain_time(seconds: float) -> void:
	sustain_time = seconds

# Function to adjust volume
func set_volume_db(db: float) -> void:
	volume_db = db
	for player in get_children():
		if player is AudioStreamPlayer:
			player.volume_db = volume_db

# Function to play multiple notes simultaneously
func play_multiple_notes(indices: Array) -> void:
	for index in indices:
		play_note(index)
