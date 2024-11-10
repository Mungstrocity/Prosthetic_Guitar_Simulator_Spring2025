extends Node

#video on godot sound players
#https://www.youtube.com/watch?v=h3_1dfPHXDg&ab_channel=GameDevArtisan

#interactive stream player:
#https://docs.godotengine.org/en/stable/classes/class_audiostreaminteractive.html

@onready var string_players = $"./Strings".get_children()

# I think i am going to have to pivot to not using collisions because they are not seeming to work right.

func play_note(string_name: String, fret_name: String):
	# E2, A2, D3, G3, B3, E4
	print("playing note!")
	var basic_note_dict = {"S1": "E4", "S2": "B3", "S3": "G3", "S4": "D3", "S5": "A2", "S6": "E2"} #no frets held down, only the string
	var modified_note_dict = {"S1": {"F1": "F4", "F2": "F#4", "F3": "G4", "F4": "G#4", "F5": "A4", "F6": "A#4", "F7": "B4", "F8": "C5", "F9": "C#5", "F10": "D5", "F11": "D#5", "F12": "E5", "F13": "F5", "F14": "F#5", "F15": "G5", "F16": "G#5", "F17": "A5", "F18": "A#5", "F19": "B5", "F20": "C6"}, \
							"S2": {"F1": "C4", "F2": "C#4", "F3": "D4", "F4": "D#4", "F5": "E4", "F6": "F4", "F7": "F#4", "F8": "G4", "F9": "G#4", "F10": "A4", "F11": "A#4", "F12": "B4", "F13": "C5", "F14": "C#5", "F15": "D5", "F16": "D#5", "F17": "E5", "F18": "F5", "F19": "F#5", "F20": "G5"}, \
							"S3": {"F1": "G#3", "F2": "A3", "F3": "A#3", "F4": "B3", "F5": "C4", "F6": "C#4", "F7": "D4", "F8": "D#4", "F9": "E4", "F10": "F4", "F11": "F#4", "F12": "G4", "F13": "G#4", "F14": "A4", "F15": "A#4", "F16": "B4", "F17": "C5", "F18": "C#5", "F19": "D5", "F20": "D#5"}, \
							"S4": {"F1": "D#3", "F2": "E3", "F3": "F3", "F4": "F#3", "F5": "G3", "F6": "G#3", "F7": "A3", "F8": "A#3", "F9": "B3", "F10": "C4", "F11": "C#4", "F12": "D4", "F13": "D#4", "F14": "E4", "F15": "F4", "F16": "F#4", "F17": "G4", "F18": "G#4", "F19": "A4", "F20": "A#4"}, \
							"S5": {"F1": "A#2", "F2": "B2", "F3": "C3", "F4": "C#3", "F5": "D3", "F6": "D#3", "F7": "E3", "F8": "F3", "F9": "F#3", "F10": "G3", "F11": "G#3", "F12": "A3", "F13": "A#3", "F14": "B3", "F15": "C4", "F16": "C#4", "F17": "D4", "F18": "D#4", "F19": "E4", "F20": "F4"}, \
							"S6": {"F1": "F2", "F2": "F#2", "F3": "G2", "F4": "G#2", "F5": "A2", "F6": "A#2", "F7": "B2", "F8": "C3", "F9": "C#3", "F10": "D3", "F11": "D#3", "F12": "E3", "F13": "F3", "F14": "F#3", "F15": "G3", "F16": "G#3", "F17": "A3", "F18": "A#3", "F19": "B3", "F20": "C4"}}
	var fret_modifier = false
	if !fret_name.is_empty():
		fret_modifier = true
	if fret_modifier:
		#each string plays in its own audio bus, so each note will play until another note on that string is switched to or it fades out.
		for string in string_players:
			if string.name == string_name: #compare the audiostreamplayer's name to the string collider's name
				#string["parameters/switch_to_clip"] = modified_note_dict[string.name][fret_name]
				string.play()
				string.get_stream_playback().switch_to_clip_by_name(modified_note_dict[string.name][fret_name])
				return
		
	else:
		for string in string_players:
			if string.name == string_name: #compare the audiostreamplayer's name to the string collider's name
				#string["parameters/switch_to_clip"] = basic_note_dict[string.name]
				string.play()
				string.get_stream_playback().switch_to_clip_by_name(basic_note_dict[string.name])
				return
	#Shouldn't get here error
	assert(false, "Error: Couldn't play note.")
	return
