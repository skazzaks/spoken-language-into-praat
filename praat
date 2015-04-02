# This script 
sound$ = Open long sound file: "Z:\home\devon\Dropbox\Lernen\Heidelberg\Zweites Semester\Spoken Language Translation\Hausarbeit\Daten\de\D01_Biotechnik_fr_alle_Rdiger_Trojo.sph"
name$ = "LongSound " + selected$ ("LongSound")
writeInfoLine: "Sound is ", name$
View
editor: name$
	Zoom: 42, 43
	Select: 42.001, 42.0003
	#Show intensity 
	test$ [0] = Get intensity
	writeInfoLine: "Value is ", test$[0]
	appendInfoLine: "Value is ", test$[0]
endeditor

#select all 
#Remove
