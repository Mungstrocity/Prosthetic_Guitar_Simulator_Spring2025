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
			if element.contains("chord"): #This should be checked for second when reading measures!
				#<chord/> element tells you that the current pitch is played at the same time as the previous pitch and that they will be sustained for the same amount of time
				pass
			if element.contains("backup"): #This should be checked for first when reading measures!
				#<backup><duration>30240</duration><backup/> tells you how far back in the measure to backup, 
				#and can be used for entering notes that will be played at the same time as other notes with different sustain lengths
				#if there is a backup in the measure, there will also be a <voice>1</voice> or <voice>2</voice> element inside note which can help too
				pass
			if element.contains("alter"):
				#inside <pitch> <alter>1</alter> indicates an accidental 1 note up ex: if it was F, it will become F# if -1 it would go down.
				#remember, between e and f, and b and c, there are not intermediary notes! ex: an f flat would be e! or a b# would be c!
				pass
			if element.contains("ocatve"):
				#middle c is on octave 4 on treble clef (G)!
				pass
