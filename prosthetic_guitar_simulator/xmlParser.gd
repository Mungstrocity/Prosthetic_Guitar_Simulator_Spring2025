@tool
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
	var parent_name = ""
	var node_data
	var num_measures = 0
	var num_notes = 0
	var next_is_sibling = false
	var in_measure_scope = false
	var in_note_scope = false
	while parser.read() != ERR_FILE_EOF:
		if parser.get_node_type() == XMLParser.NODE_ELEMENT:
			if !next_is_sibling:
				parent_name = node_name #retaining parent value from previous iteration else parent doesn't change from last one
			node_name = parser.get_node_name()
			if node_name == "measure":
				in_measure_scope = true
				num_measures += 1
				num_notes = 0 #should reset number of notes when in new measure
			if node_name == "note":
				in_note_scope = true
				num_notes += 1
			if in_note_scope: #also should be in measure scope
				node_name = "m" + str(num_measures) + "," + "n" + str(num_notes) + "," + node_name
			elif in_measure_scope:
				node_name = "m" + str(num_measures) + "," + "n" + str(num_notes) + "," + node_name
			var attributes_dict = {}
			var child_or_data_dict = {}
			for idx in range(parser.get_attribute_count()):
				attributes_dict[parser.get_attribute_name(idx)] = parser.get_attribute_value(idx)
			songData[node_name] = [attributes_dict, child_or_data_dict] #add attributes to the key value pair of the element
			if(!parent_name.is_empty()): #checks for the first node which has no parent
				songData[parent_name][1][node_name] = songData[node_name] #add the current elementname to the parent element's child_or_data_dict dictionary in index 1
			print("The ", node_name, " element has the following attributes: ", attributes_dict)
		elif parser.get_node_type() == XMLParser.NODE_TEXT:
			node_data = parser.get_node_data()
			if(!node_data.strip_edges().is_empty()):
				#should check if attributes have been assigned making it size 1. there shouldn't be a second element in a leaf node (no child nodes)
				if songData[node_name].size() == 1:
					songData[node_name].append({"data": node_data})
				print(node_name, " data is: ", node_data)
		elif parser.get_node_type() == XMLParser.NODE_ELEMENT_END:
			# End of an element node next will be a sibling of the previous
			next_is_sibling = true
			if node_name == "measure": #exiting scope
				in_measure_scope = false
			if node_name == "note": #exiting scope
				in_note_scope = false
	return songData
