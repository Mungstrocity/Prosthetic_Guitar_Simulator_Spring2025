extends Node3D

#useful website to help with notes on a guitar. remember no fret has all the default notes 
#(low6->E2 (means octave 2 with fret not held), A2, D3, G3, B3, E4) each fret towards
#guitar base goes a half step higher in pitch, each fret towards the string tighteners goes a step lower.
#fret 12 is an octave higher than default pitches. every 12 frets is similar
#https://fretmap.app/scales/c-major-scale/position-5

#maybe i'll select the next notes based on which selection of notes gets a minimal total distance from each other, 
#then i will get the average note for that selection, and choose the note which has the lowest distance on this average note 
#to the previously found and played average note


#there will be an analyzer function for chosing fingers for each beat (multi note and single note ones) which is described below
#analyze the next notes to see how many notes need to be played at the same time
#make a target grouping for all notes to be played at the same time
#start with the lowest pitch note (of the notes about to be played at the same time in one beat) 
#check the finger - note count weight dict to see if from previous notes in the measure it's not one of the 
#higher weights for a finger in this measure,
#and if so, see if another finger can play that note by checking num notes played at once, else if another can't, assign the target anyways
#check it's note count (which represents the weighting of preference to move that finger or not, 
#the higher the note count in the measure, the lower the preference to move that finger from it's position, 
#and the more priority is given to moving higher pitch fingers if it's possible to still play all the other notes without moving) 
#in the measure passed in from the measure analyzer and if it's greater than 1, 
#assign a chosen finger to the measure analyzer dict to associate it with the weight, usually index finger since it's the lowest note, 
#and get all possible positions of it down the neck. 
#Then move to the next finger middle and choose the next lowest note (if there is one available to be played at the same time), 
#and pick all the positions down the neck for the next note 
#with the condition that they can only be higher or the same fret as the index frets with a max spacing down the neck of 2 additonal frets. 
#Then do the same for the next fingers. then once all the fingers have all those possible postions, find the fingering group with 
#the minimal total distance between it's average note, and the previous played average note (or fret1 if first note)
#also note (3 fret spacing max) and return that array or dict of the chosen fingering for that multi-note. 
#return it in a dict of stringnum?: fretnum?
# or even better just return a dict with the finger number as the key, then the target string number and fret number as another dict inside.

#But there is also a measure analyzer dict which will count the number of note occurances during the measure, 
#and it will try to map the same fingers to the same notes over and over based on number of reocurrances 
#and if it's a higher or lower pitch (for choosing right finger to play it) while spreading out the burden of other frets 
#to other fingers

#(maybe pass in a finger type as well since not all fingers can play all strings 
#(how i have it set up right now anyways) Then based on that finger type, return the possible positions in an dict for that finger)

#function to return the list of possible target nodes based on the passed in note parameters
#im thinking about doing a path finding algorithm or something to where you start with a note, then get all possible targets,
#then if you have more notes you are playing at the same time, you would pass in the array of an array of the previous note's targets
#then based on all the targets, you would find the most optimal targets to use with each other based on lowest minimal distances
#simulated annealing basically. (I might have to change this slightly and just go with a biased selection becuase that might take too much time)
func get_left_finger_targets(hover: bool, octave: int = 3, pitch: String = "C", alter: int = 0):
	match octave:
		2: #  S6: E2-F0 to B2-F7
			# S5: A2-F0 to B2-F2
			match pitch:
				"C":
					match alter:
						-1: # flat pitch alter
							
							pass
						1: # sharp pitch alter
							
							pass
						_: #handles no alter, or other unimplemented alters like natural alter or double alters (aka: just play regular pitch)
							
							pass
					pass
				"D":
					
					pass
				"E":
					
					pass
				"F":
					
					pass
				"G":
					
					pass
				"A":
					
					pass
				"B":
					
					pass
				_:
					#Shouldn't get here error
					assert(false, "Error: Note Pitch Not Available.")
					pass
			pass
		3: #  S6: C3-F8 to B3-F19
			# S5: C3-F3 to B3-F14 
			# S4: D3-F0 to B3-F9 
			# S3: G3-F0 to B3-F4 
			# S2: B3-F0
			
			pass
		4: #  S6: C4-F20, 
			# S5: C4-F15 to F4-F20 
			# S4: C4-F10 to A#4-F20 
			# S3: C4-F5 to B4-F16 
			# S2: C4-F1 to B4-F12 
			# S1: E4-F0 to B4-F7
			
			pass
		5: #  S3: C5-F17 to D#5-F20 
			# S2: C5-F13 to G5-F20 
			# S1: C5-F8 to B5-F19
			
			pass
		6: #  S1: C6-F20
			
			pass
		_:
			#any other octaves are not playable on the guitar so if uplayable higher pick highest notes possible, else lowest possible.
			if(octave >= 6): #play on highest possible ocatve on the guitar
				
				pass
			elif(octave <= 2): #play on lowest possible ocatve on guitar
				
				pass
			pass

func get_right_finger_target(guitar_string: int, hover: bool, other_note_targets: Array):
	match guitar_string:
		1:
			
			pass
		2:
			pass
		3:
			pass
		4:
			pass
		5:
			pass
		6:
			pass
		_:
			pass
