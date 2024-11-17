extends ResourcePreloader

#read and parse the music xml file useing godot XML parser to get the number of total quarter note beats (inlcuding rests) in the song, tempo,
#notes (inlcuding their length*take length as a fraction of quarternote length and convert to seconds*, 
#pitch *convert this to guitar string and fret, if accidental sharp or flat convert to regular notes*, 
#and position in the song the start time and end time in seconds from song start), 
#add dynamics support. 

#parsed parts should include musicXML dynamics, pitch(inlcudes note and octave), measure maybe? (again probly good for looking ahead?)
#duration (not sure about what this means...) and type of beat (quarter, eighth, etc...),
#notations maybe? (tell you if the notes are tied to others or not... should be useful for looking ahead
#the only notes that need to be looked ahead at are probably eighths or quicker until you get to really fast tempos)

#function to parse the musicXML based on the Godot XMLParser class
#parses info into a dictionary songData{name, [{attributeName, attribute}, childName/leafData]}
func parse_music_XML():
	var parser = XMLParser.new()
	#song data should store 
	var songData = {}
	parser.open("res://Assets/InputFiles/input.xml")
	var node_name = ""
	var node_data
	var num_measures = 0
	var num_notes = 0
	var in_measure_scope = false
	var in_note_scope = false
	var in_backup_scope = false
	var tempName
	while parser.read() != ERR_FILE_EOF:
		if parser.get_node_type() == XMLParser.NODE_ELEMENT:
			node_name = parser.get_node_name()
			if node_name == "measure":
				in_measure_scope = true
				num_measures += 1
				tempName = "-m" + str(num_measures-1) + "," + "+n" + str(0) + ",num_notes" #creates a node which keeps track of the number of notes per measure
				songData[tempName] = {"data":num_notes} #stores the number of notes in the previous measure
				num_notes = 0 #should reset number of notes when in new measure
			if node_name == "note":
				in_note_scope = true
				num_notes += 1
			if node_name == "backup":
				in_backup_scope = true
			if in_backup_scope:
				node_name = "-m" + str(num_measures) + "," + "+n" + str(num_notes) + "," + "b" + "," + node_name
			elif in_note_scope: #also should be in measure scope
				node_name = "-m" + str(num_measures) + "," + "+n" + str(num_notes) + "," + node_name
			elif in_measure_scope:
				node_name = "-m" + str(num_measures) + "," + "+n" + str(num_notes) + "," + node_name
			var attributes_dict = {}
			for idx in range(parser.get_attribute_count()):
				attributes_dict[parser.get_attribute_name(idx)] = parser.get_attribute_value(idx)
			songData[node_name] = attributes_dict #add attributes to the key value pair of the element
			#print("The ", node_name, " element has the following attributes: ", attributes_dict)
		elif parser.get_node_type() == XMLParser.NODE_TEXT:
			node_data = parser.get_node_data()
			if(!node_data.strip_edges().is_empty()):
				print(node_name)
				songData[node_name]["data"] = node_data #add the data stored in the element to the attributes dictionary
				#print(node_name, " data is: ", node_data)
		elif parser.get_node_type() == XMLParser.NODE_ELEMENT_END:
			node_name = parser.get_node_name()
			if node_name == "measure": #exiting scope
				in_measure_scope = false
			if node_name == "note": #exiting scope
				in_note_scope = false
			if node_name == "backup": #exiting scope
				in_backup_scope = false
	#before exiting, return the number of measures and notes of the last measure as well by adding them to the dictionary.
	tempName = "-m" + str(num_measures) + "," + "+n" + str(0) + ",num_notes" #creates a node which keeps track of the number of notes per measure
	songData[tempName] = {"data":num_notes} #stores the number of notes in the previous measure
	songData["num_measures"] = {"data":num_measures}
	return songData
