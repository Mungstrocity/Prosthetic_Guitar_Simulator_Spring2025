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

#maybe i'll select the next notes based on which selection of notes gets a minimal total distance from each other, 
#then i will get the average note for that selection, and choose the note which has the lowest distance on this average note 
#to the previously found and played average note

#(maybe pass in a finger type as well since not all fingers can play all strings 
#(how i have it set up right now anyways) Then based on that finger type, return the possible positions in an dict for that finger)
