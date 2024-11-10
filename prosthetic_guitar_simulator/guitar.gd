extends Node3D

#useful website to help with notes on a guitar. remember no fret has all the default notes 
#(low6->E2 (means octave 2 with fret not held), A2, D3, G3, B3, E4) each fret towards
#guitar base goes a half step higher in pitch, each fret towards the string tighteners goes a step lower.
#fret 12 is an octave higher than default pitches. every 12 frets is similar
#https://fretmap.app/scales/c-major-scale/position-5

#function to return the list of possible target nodes based on the passed in note parameters
#im thinking about doing a path finding algorithm or something to where you start with a note, then get all possible targets,
#then if you have more notes you are playing at the same time, you would pass in the array of an array of the previous note's targets
#then based on all the targets, you would find the most optimal targets to use with each other based on lowest minimal distances
#simulated annealing basically. (I might have to change this slightly and just go with a biased selection becuase that might take too much time)
func get_poss_gneck_targets(hover: bool, octave: int = 3, pitch: String = "C", alter: int = 0):
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

func get_guitar_pick_target(guitar_string: int, hover: bool, other_note_targets: Array):
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
