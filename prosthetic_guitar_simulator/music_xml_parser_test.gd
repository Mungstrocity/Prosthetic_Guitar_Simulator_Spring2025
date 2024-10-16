extends Node


func test_XML_parse(songData: Dictionary):
	print("\n\n**********TEST***********\n")
	#print("Song Data Elements: ")
	#print(songData.keys())

	#if songData["m1,n0,beat-unit"].has("data"):
		#print(songData["m1,n0,beat-unit"]["data"])
	#print(songData["m1,n0,measure"].keys())

	#divisions per note_type
	var note_length_div = songData["-m1,+n0,divisions"]["data"]
	#is it a quarter-note, half-note, etc...
	var note_type = songData["-m1,+n0,beat-unit"]["data"]
	#how many of the note type occurs in one minute.
	var bpm = songData["-m1,+n0,per-minute"]["data"]
	#list of the time signature, ex: [4,4]
	var timesig = [songData["-m1,+n0,beats"]["data"],songData["-m1,+n0,beat-type"]["data"]]
	#the clef the song starts playing in ex: G
	var clef = songData["-m1,+n0,sign"]["data"] #G cleff is treble cleff, and most common. honestly shouldn't need to worry about this as step and octave should still tell everything you need.
	print(songData["num_measures"])
	print(songData["-m1,+n0,num_notes"])
	print(songData["-m16,+n0,num_notes"])
	for element in songData.keys():
		if element.contains(""):
			#all elements that are measure and note specific should be extracted here in order.
			if element.contains("divisions"):
				
				pass
