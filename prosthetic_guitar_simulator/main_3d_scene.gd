extends Node

var songDict
var processed_song

#use for changing dynamics only (tempororary until implementing dynamics based on velocity of fingers)
@onready var guitar_sounds_node = $"./GuitarPlayer/Guitar/GuitarSounds"
@onready var guitar_player = $"./GuitarPlayer"
@onready var guitar = $"./GuitarPlayer/Guitar"
@onready var anim = $"./GuitarPlayer/AnimationPlayer"

var preset_music_list = {
	"load_input": "res://input.xml",
	"load_mary": "res://Assets/InputFiles/mary.xml",
	"load_teapot": "res://Assets/InputFiles/teapot.xml",
	"load_silent": "res://Assets/InputFiles/silentAbridged.xml",
	"load_wellerman": "res://Assets/InputFiles/The_Wellerman.xml",
	"load_fur_elise": "res://Assets/InputFiles/Fr_EliseBetterAbr.xml",
	"load_moonlight": "res://Assets/InputFiles/Moonlight_Sonata.xml",
	"load_ave_maria": "res://Assets/InputFiles/Ave_Maria.xml"
}

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	#Extracts the songData into the form {element_name: [{attribute_name: attribute}, {data_name/child_name: data/child}]} 
	#if it's the measures or notes scope, measures use the naming "m#,node_name" while if also in the note scope inside a measure, 
	#the convention is "m#,n#,node_name"
	
	load_song(preset_music_list["load_input"]) #load default song 

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	handle_cams()
	if Input.is_action_just_pressed("play_song"): #plays the loaded song ctrl + p
		play_song(processed_song)
	if Input.is_action_just_pressed("load_input"):
		load_song(preset_music_list["load_input"])
	if Input.is_action_just_pressed("load_mary"):
		load_song(preset_music_list["load_mary"])
	if Input.is_action_just_pressed("load_silent"):
		load_song(preset_music_list["load_silent"])
	#if Input.is_action_just_pressed("load_wellerman"):
		#load_song(preset_music_list["load_wellerman"])
	if Input.is_action_just_pressed("load_teapot"):
		load_song(preset_music_list["load_teapot"])
	#if Input.is_action_just_pressed("load_fur_elise"):
		#load_song(preset_music_list["load_fur_elise"])
	#if Input.is_action_just_pressed("load_moonlight"):
		#load_song(preset_music_list["load_moonlight"])
	if Input.is_action_just_pressed("load_ave_maria"):
		load_song(preset_music_list["load_ave_maria"])

func load_song(input_file_string):
	if processed_song != null: #clear out old song
		processed_song.clear()
	songDict = $MusicXMLParser.parse_music_XML(input_file_string)	
	processed_song = process_song_data(songDict)
	songDict.clear()

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
func process_song_data(songData: Dictionary):	
	#measure booleans
	var attributes = false #if attributes are detected in the measure
	var direction = false #if direction elements are detected in the measure
	var measure_number = 0 #measure number currently on starting at 0
	var note_beat = 0 #note beat currently on in parse
	var note_in_beat = 0 #current note inside the note beat
	var current_dynamics = 75.0 #default to forte (loud)
	var current_divisions_per_unit = 10080 #use a default value
	var num_beat_units_in_measure = 1 #assume 1 default
	var current_bpm = 60 #default value
	var backup = false #bool to check if inside the backup element tag when parsing
	var current_division_pos = 0
	var last_division_pos = 0
	var start_parsing = false
	
	#the array that holds measures and those measures hold an array of note beats (which can contain multiple notes at once in an embedded array of the individual notes sorted by 
	#lowest to highest note) and each note array contains a dictionary which has it's pitch, octave, alter, dynamics, division position in measure, and duration in seconds because of function (sustain length)
	#NOTE measures in the array are numbered starting at 0, but everywhere else they start at 1
	#ex: song_info[measure_num][ordered_note_beat_num][low_high_ordered_notes][note_info_dict]
	var song_info = [] #this is an array of measures, (plus other data you can access)
	
	#var multi_notes_in_measure = false
	for element in songData.keys():
		print(element)
		#all elements that are measure and note specific should be extracted here in order.
		if element.contains("measure") && !element.contains("num_measures"): #start of a new measure so add it to the array
			start_parsing = true #got to the first part of the actual song so start parsing now
			#put a new array of note beats inside the measure array
			song_info.append([]) #to access this measure array do song_info[measure_number]
			pass
		if start_parsing && element.contains("note") && !element.contains("num_notes") && !element.contains("actual-notes") && !element.contains("normal-notes"):
			attributes = false #don't enter attributes checker again for this measure
			direction = false #same as above
			backup = false
			#put a new array of notes inside the note beat array (for now, don't worry about sorting to be in ascending order of pitch and octave)
			if typeof(song_info[measure_number]) == TYPE_ARRAY && song_info[measure_number].size() > 0: #means there are note beats already in the measure
				for note_beat_index in song_info[measure_number].size(): #iterate through note beats to get the position that the next beat should go for backups
					var temp_note_in_beat = song_info[measure_number][note_beat_index].size() -1 #get last note in the beat
					while !song_info[measure_number][note_beat_index][temp_note_in_beat].has("div_start_pos"): #last note doesn't have these, it should, so get rid of this note, and try again.
						push_warning("Warning: Found a weird ghost note, Bug work around executing...")
						song_info[measure_number][note_beat_index].remove_at(temp_note_in_beat) #remove the junk node
						if temp_note_in_beat != 0:
							temp_note_in_beat -= 1 #decrement to the previous index and try again
					if current_division_pos == song_info[measure_number][note_beat_index][temp_note_in_beat]["div_start_pos"]: #place note beat on
						#perfect match with division posistion
						#append new note dict inside the current note beat
						song_info[measure_number][note_beat_index].append({})
						break
					elif current_division_pos < song_info[measure_number][note_beat_index][temp_note_in_beat]["div_start_pos"]: #place note beat after
						#means the last note_beat one was the note_beat you need to put the next beat after
						if !(song_info[measure_number].size() > note_beat_index + 1): #if the last one was the last note beat in the measure then append
							song_info[measure_number].append([])
							#now append a new note dict
							song_info[measure_number][note_beat_index+1].append({})
						else: #else insert
							song_info[measure_number].insert(note_beat_index, []) #insert new note beat at current position
							#now append a new note dict at current index
							song_info[measure_number][note_beat_index].append({})
						break
					elif current_division_pos > song_info[measure_number][note_beat_index][temp_note_in_beat]["div_start_pos"]: #place note beat before
						if !(song_info[measure_number].size() > note_beat_index + 1): #if the last one was the last note beat in the measure then append
							song_info[measure_number].append([])
							#now append a new note dict
							song_info[measure_number][note_beat_index+1].append({})
						else: #else more notes to check
							continue
						break
			else: #no notebeats present in the measure
				song_info[measure_number].append([]) #create new note beats
				#put a new dictionary of note information inside the notes array for a beat (assumes at first it's in a different note beat)
				song_info[measure_number][note_beat].append({})
			
			if !songData[element].is_empty() && songData[element].has("dynamics"): #check for dynamics in the note attributes
				current_dynamics = float(songData[element]["dynamics"])
			song_info[measure_number][note_beat][note_in_beat]["dynamics"] = current_dynamics #set dynamics (uses default if not specified)
		if start_parsing && attributes || element.contains("attributes"):
			attributes = true #check these until getting to the notes portion
			if element.contains("divisions"): #divisions per note_type
				current_divisions_per_unit = int(songData[element]["data"]) #set division resolution if it changes
				pass
			#attributes -> time signature elements ex: 3:4 time 3 is beats, 4 is beat-type
			if element.contains("beats"): #num of beats per measure
				#need to know this one for num of beat counts (if playing multiple notes at once)
				num_beat_units_in_measure = int(songData[element]["data"])
				pass
		if start_parsing && direction || element.contains("direction"):
			direction = true #check these until getting to the notes portion
			#attributes -> key elements
			if element.contains("per-minute"): #number of beats per minute, tempo
				#get the bpm
				current_bpm = int(songData[element]["data"])
				pass
		if start_parsing && element.contains("chord"): #will have the n# of the current note
			#<chord/> element tells you that the current pitch is played at the same time as the previous pitch and that they will be sustained for the same amount of time
			#print(element)
			#inside the note already, and have set a dynamics element if there is one.
			var temp_note_beat = song_info[measure_number].pop_back() #gets the current note beat array and all it's information contained within
			note_beat -= 1 #go back to the previous note beat and make it the current one
			song_info[measure_number][note_beat].append_array(temp_note_beat) #combines the notes in current note beat with the temp note beat
			note_in_beat = song_info[measure_number][note_beat].size() -1 #gets the last note index in the beat array
			
			var temp_pos = last_division_pos
			last_division_pos = current_division_pos #keep track of previous position
			current_division_pos = temp_pos #get backup from the previous measure position variable
			pass
		if start_parsing && element.contains("backup"):
			backup = true
		if start_parsing && backup && element.contains("duration"): #This should be checked for first when reading measures! will have the same n# as the previous note
			#<backup><duration>30240</duration><backup/> tells you how far back in the measure to backup, 
			#and can be used for entering notes that will be played at the same time as other notes with different sustain lengths
			#if there is a backup in the measure, there will also be a <voice>1</voice> or <voice>2</voice> element inside note which can help too
			#print(element)
			#should subtract from notebeat var based on how many divisions back in beats it specifies. this one should be easier
			var backup_in_divisions = int(songData[element]["data"])
			
			#should be a whole number and not have to worry about adding a new note beat entirely on a backup, 
			#but could be an issue in the future if songs do backup in non-whole number incrememnts
			var backup_in_notebeats = float(backup_in_divisions)/float(current_divisions_per_unit)
			if !is_equal_approx(backup_in_notebeats, roundf(backup_in_notebeats)):
				push_warning("Warning: Note backup tag for multi-note playing encountered a fractional backup. Fix needed.")
			backup_in_notebeats = roundi(backup_in_notebeats) #convert back to int value for safety after rounding if needed
			last_division_pos = current_division_pos #keep track of previous position
			current_division_pos -= int(songData[element]["data"]) #subtract backup from the measure position variable
			
			for beat in song_info[measure_number].size():
				var temp_note_in_beat = song_info[measure_number][beat].size() -1 #get last note in the beat
				if current_division_pos == song_info[measure_number][beat][temp_note_in_beat]["div_start_pos"]: #place note beat on
					#perfect match with division posistion
					#append new note dict inside the current note beat
					note_beat = beat
					break
				elif current_division_pos < song_info[measure_number][beat][temp_note_in_beat]["div_start_pos"]: #place note beat after
					#means the last note_beat one was the note_beat you need to put the next beat after
					if !(song_info[measure_number].size() > beat + 1): #if the last one was the last note beat in the measure then append
						note_beat = beat + 1
						pass
					else: #else insert
						note_beat = beat
						pass
					break
				elif current_division_pos > song_info[measure_number][beat][temp_note_in_beat]["div_start_pos"]: #place note beat before
					if !(song_info[measure_number].size() > beat + 1): #if the last one was the last note beat in the measure then append
						note_beat = beat + 1
						pass
					else: #else more notes to check
						continue
					break
			note_in_beat = song_info[measure_number][note_beat].size() #gets the last note index in the beat array of the new notebeat
			pass
		
		if start_parsing && element.contains("octave"):
			#middle c is on octave 4 on treble clef (G)!
			#print(element)
			#print(songData[element])
			song_info[measure_number][note_beat][note_in_beat]["octave"] = int(songData[element]["data"])
			pass
		if start_parsing && element.contains("step"):
			#middle c is on octave 4 on treble clef (G)!
			#print(element)
			#print(songData[element])
			song_info[measure_number][note_beat][note_in_beat]["step"] = songData[element]["data"]
			pass
		if start_parsing && element.contains("alter"):
			#inside <pitch> <alter>1</alter> indicates an accidental 1 note up ex: if it was F, it will become F# if -1 it would go down.
			#remember, between e and f, and b and c, there are not intermediary notes! ex: an f flat would be e! or a b# would be c!
			#print(element)
			#print(songData[element])
			song_info[measure_number][note_beat][note_in_beat]["alter"] = int(songData[element]["data"])
			pass
		if start_parsing && !backup && element.contains("duration"):
			#print(element)
			#print(songData[element])
			var duration = int(songData[element]["data"])
			song_info[measure_number][note_beat][note_in_beat]["duration"] = duration #set duration of note
			song_info[measure_number][note_beat][note_in_beat]["duration_sec"] = note_duration_in_sec(current_bpm, current_divisions_per_unit, duration) #set duration of note
			#store measure position data for easier parsing
			song_info[measure_number][note_beat][note_in_beat]["div_start_pos"] = current_division_pos
			last_division_pos = current_division_pos #keep track of previous position
			current_division_pos += duration #add duration to the measure position variable
			pass
		if start_parsing && element.contains("type") && !element.contains("beat-type") && !element.contains("direction-type") && !element.contains("normal-type") && !element.contains("tuplet-type"): #good place to signal the end of a note since all notes have one. we don't really need type info tho
			note_beat += 1 #iterate to the next note beat at the end of every note
			if song_info[measure_number].size() > note_beat: #next note beat exists already
				note_in_beat = song_info[measure_number][note_beat].size() -1 #get the index of the last note in the beat
			else:
				note_in_beat = 0 #no note beat exists, so no notes either, start index from 0 for next note
		if start_parsing && element.contains("num_notes"): #good place to signal the end of a measure
			#sort notes in beats before finished
			for beat in song_info[measure_number].size():
				song_info[measure_number][beat].sort_custom(sort_notes)
			#set beat count back to 0
			note_beat = 0 #because end of measure reached, so prepare for next one
			note_in_beat = 0
			measure_number += 1
			current_division_pos = 0
			last_division_pos = 0
		songData.erase(element) #clean up as you iterate through
	return song_info

#now with the processed song data, play the song by controlling the guitar player
func play_song(song_array: Array):
	print(song_array)
	var num_measures = song_array.size()
	for measure in num_measures:
		var num_beats = song_array[measure].size()
		for beat in num_beats:
			
			var note_array = song_array[measure][beat]
			
			#NOTE total play beat process will take about a 0.3 seconds delay minimum.
			var min_play_duration = 100.0 #set minimum play duration between notes to a crazy value like 100.0 seconds
			for note_beat in note_array.size(): #find the minimum play duration of a note in a note beat to find the time between this and the next note
				if !note_array[note_beat].has("duration_sec"):
					push_warning("Warning: Found a weird ghost note, need to fix in song-info parser...")
					continue #skip this one a weird zero array
				if note_array[note_beat]["duration_sec"] < min_play_duration:
					min_play_duration = note_array[note_beat]["duration_sec"] #set the new duration in seconds
			min_play_duration -= 0.2 #subtract off the approximate bias from playing the notes
					
			#returns an array of the chosen finger position dictionaries containing target info for each finger index to pinky in that order
			var selected_note_targets = guitar_player.select_finger_targets(note_array)
			if selected_note_targets == null: #just a rest beat, so don't move hands but still wait the amount of time required.
				await get_tree().create_timer(min_play_duration + 0.2).timeout #add .3 back since we didn't play anything this time
				continue #now go to next beat
			var lowest_fret = guitar_player.get_lowest_fret_from_notes(selected_note_targets)
			if lowest_fret == 0: #means don't worry about moving the hand from last time
				pass
			elif anim.animations.has(lowest_fret):
				anim.play(anim.animations[lowest_fret]) #select the ideal position for the beat for the left arm
				anim.play("guitarPoses/Rarm_pickPos1")
			else:
				lowest_fret -= 1 #get the next closest fret if there isn't a programmed arm location
				anim.play(anim.animations[lowest_fret])
				anim.play("guitarPoses/Rarm_pickPos1")
			#get number of notes in chosen array and iterate through setting the fingers to hover over them if they are targets, 
			#if the finger doesn't have a target, use a defualt target for the avg fret
			#remember enum Finger { THUMB, INDEX, MIDDLE, RING, PINKY }
			var num_notes_in_beat = selected_note_targets.size()
			var left_targets = get_left_finger_notes(selected_note_targets)
			var num_left_notes = left_targets.size()
			for finger in 4: #Set left fingers first to hover (no hover needed since right hand plays) only 4 fingers are set thumb is left out
				if num_left_notes > finger: #set left finger targets for needed notes
					guitar_player.get_left_ik_target(finger + 1).set_finger_target(left_targets[finger]["left-hover"]) #start with index finger
				else: #else set a default note hover for uneeded notes so fingers don't break and look weird
					var unused_finger_fret = lowest_fret + 1
					if unused_finger_fret > 20:
						unused_finger_fret -= 1
					#guitar_player.get_left_ik_target(finger + 1).set_finger_target(guitar_player.get_left_target(6-finger, unused_finger_fret, true)) #set unused left fingers to lowest_fret and add two to get them out of the way and default string for that finger
					guitar_player.get_left_ik_target(finger + 1).set_finger_target(guitar_player.get_left_target(6, unused_finger_fret, true)) #set unused left fingers to lowest_fret and add two to get them out of the way and default string for that finger
			
			#takes about 0.1 seconds or more to set left hover targets
			await get_tree().create_timer(0.05).timeout
			
			for finger in 4: #Set left fingers now to press only 4 fingers are set thumb is left out
				if num_left_notes > finger: #set left finger targets for needed notes
					guitar_player.get_left_ik_target(finger + 1).set_finger_target(left_targets[finger]["left"]) #start with index finger
				else: #else set a default note hover for uneeded notes so fingers don't break and look weird
					var unused_finger_fret = lowest_fret + 1
			if num_notes_in_beat < 6: #only have to set up hover targets if its not a full strum but picking
				for finger in 5: #Set right fingers first to hover all 5 fingers are set
					if num_notes_in_beat > finger: #set right finger targets for needed notes
						guitar_player.get_right_ik_target(finger).set_finger_target(selected_note_targets[finger]["right-hover"])
					else: #else set a default note hover for uneeded notes so fingers don't break and look weird
						guitar_player.get_right_ik_target(finger).set_finger_target(guitar_player.get_right_target(6-finger, true)) #set unused right fingers to default string for that finger
			
			#takes about 0.1 seconds or more to set left targets and right hover targets
			await get_tree().create_timer(0.05).timeout #let fingers and arm tween in 0.1 seconds to positions
			
			#takes ~0.2 seconds to play
			if num_notes_in_beat < 6: #now play (this is picking version of right hand)
				var used_fingers_R = { #dictionary to store which fingers are used or not
					6: {"bool": false, "num": 0}, #thumb
					5: {"bool": false, "num": 1}, #index
					4: {"bool": false, "num": 2}, #middle
					3: {"bool": false, "num": 3}, #ring
					2: {"bool": false, "num": 4} #pinky
				}
				var used_strings = {
					6: false,
					5: false,
					4: false,
					3: false,
					2: false,
					1: false
				}
				for note in num_notes_in_beat: #Set used strings
					used_strings[selected_note_targets[note]["string"]] = true
				var string_pointer = 0
				var note_counter = 0
				for string in used_strings.keys():
					var finger_num = used_fingers_R[string+string_pointer]["num"]
					if used_strings[string]: #if string is used in beat
						used_fingers_R[string+string_pointer]["bool"] = true
						guitar_player.get_right_ik_target(finger_num).set_finger_target(selected_note_targets[note_counter]["right"]) #set right finger targets for needed notes
						note_counter += 1
					elif string_pointer != 1: #shift fingers down once if an unused string is encountered
						string_pointer += 1
					else: #else set a default note hover for uneeded notes so fingers don't break and look weird (keep them hovering if not playing a note)
						#guitar_player.get_right_ik_target(finger_num).set_finger_target(guitar_player.get_right_target(6-finger_num, true))
						pass
				await get_tree().create_timer(0.05).timeout #give fingers time to strike strings
				for finger in 5: #Set right fingers back to hover
					if num_notes_in_beat > finger: #set right finger targets for needed notes
						guitar_player.get_right_ik_target(finger).set_finger_target(selected_note_targets[finger]["right-hover"])
				await get_tree().create_timer(0.05).timeout #give fingers time to reset to hover
			
			#takes ~0.2 seconds to play
			if num_notes_in_beat == 6: #if playing all strings!
				#play a quick strum of all strings, takes ~0.2 seconds
				for finger in 5:
					guitar_player.get_right_ik_target(finger).set_finger_target(guitar_player.get_right_target(6-(finger), false))
				await get_tree().create_timer(0.05).timeout
				#dont forget the final string!
				guitar_player.get_right_ik_target(4).set_finger_target(guitar_player.get_right_target(1, false))
				await get_tree().create_timer(0.05).timeout
				for finger in 5:
					guitar_player.get_right_ik_target(finger).set_finger_target(guitar_player.get_right_target(6-(finger), true))
			
			await get_tree().create_timer(min_play_duration).timeout #wait until the next note should be played
	pass
	
func get_left_finger_notes(chosen_targets):
	var left_targets = []
	for target in chosen_targets.size():
		if chosen_targets[target]["fret"] == 0:
			continue
		else:
			left_targets.append(chosen_targets[target])
	return left_targets
	

#inside attributes, divisions tells you how many divisions there are in a basic beat unit (ex: quarter note divisions for 4:4 time)
#then, duration data tells you how many divisions there are in the note (so how long to play it)
#to get the length of a single division, take per-minute (bmp) in direction tag and do
# 60seconds/(per-minute * divisions) = seconds per division.
#then for duration in seconds, do
# seconds to play note = duration * seconds per division
func note_duration_in_sec(per_minute: int, divisions: int, duration: int):
	var seconds_per_division = 60.0/(float(per_minute) * float(divisions))
	var seconds_to_play = seconds_per_division * duration
	return seconds_to_play

# Sorts the notes by octave, then pitch step
#pass in the note dictionary and use the keys "octave" and "step" to compare
#call with song_info[measure_number][note_beat].sort_custom(sort_notes)
func sort_notes(a, b):
	#check if octaves is found (could be rest note)
	if !a.has("octave"):
		return false #move a element behind b (put rest notes at the back of array)
	if !b.has("octave"):
		return true #move a element behind b (put rest notes at the back of array)
	# Compare octaves first
	if a["octave"] != b["octave"]:
		return a["octave"] < b["octave"]
	# If octaves are the same, compare pitch steps
	return sort_pitch_steps(a["step"], b["step"])

# Helper function to sort pitch steps within an octave
func sort_pitch_steps(step_a, step_b):
	# Define the order of pitch steps
	var pitch_order = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}
	return pitch_order[step_a] < pitch_order[step_b]
