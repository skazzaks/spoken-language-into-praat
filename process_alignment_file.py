#!/usr/bin/python
# -*- coding: utf-8 -*-


# Author: Devon Fritz
# process_alignment_file.py
# This script takes in a prf file (which can be output with sclite) and, for the
# provided input words, gives detailed information about their transcriptions.
from __future__ import division
import sys
import re
import os.path

# Regular expression to detect all asterisk words (e.g. *****)
regex_only_ast = re.compile("^\**$")

def error_out(msg):
    sys.exit(msg + """ Exiting.
                Usage:  process_alignment_file.py <input file> [opt: word1 word2] """)


# Handles the storing of a sentence in the data structure
# The main work of the program is done here
def handle_sentence(f, words, speaker, word_dict):
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()

    ref = f.readline().lower().split()[1:]
    hyp = f.readline().lower().split()[1:]
    ht1 = f.readline().split()[1:]
    ht2 = f.readline().split()[1:]

       # print "Sentence"
    #print "REF" + str(ref)
    #print "HYP:" + str(hyp)
    #print "Lengths: " + str(len(ref)) + ", " + str(len(hyp)) + ", " + str(len(ht1)) + ", " + str(len(ht2)) + "\n\n"
        
    # Now that we are the section we care about, 
    for w in words:
        u = word_dict[w]['utterances']
        #print word_dict[w]
       
        for i, j in enumerate(ref):
            # We found the index of the word we are looking for - now we can use this
            # index in the rest of the structures
            if j == w:
                index = i
                word_dict[w]['total_usages'] += 1

                if hyp[i] == w:
                    word_dict[w]['correct_usages'] += 1
          
                s = ""
                if i is not 0:
                    s += ref[i-1]
                else:
                    s += "_"

                s+= " " + ref[i] + " " 

                if i is not (len(ref) - 1):
                    s += ref[i+1]
                else:
                    s += "_"

                # To get the times, we need to count the number of *** entries that were before this point, since they have no corresponding time units
                blanks = 0
                #print i

                time1 = ""
                time2 = ""
        
                r = regex_only_ast.match(hyp[i])

                if not regex_only_ast.match(hyp[i]):
                    for hypw in hyp[:i]:
                        if regex_only_ast.match(hypw):
                            blanks += 1
                            
                    time1 = ht1[i - blanks]
                    time2 = ht2[i - blanks]
                   
                
                
                u.append({'speaker': speaker, 'hyp_word': hyp[i], 'time1' : time1, 'time2' : time2, 'trigram' : s})
               # sys.exit()
                #print(u)
    


if len(sys.argv) < 3:
    error_out("Incorrect Parameters!")
    
# First, let's read in from the commandline
inputfile = sys.argv[1]

if not os.path.isfile(inputfile):
    error_out("Input file is not valid!")

words = []

for a in sys.argv[2:]:
    words.append(a.lower())
    
# Now, let's process each word
# Open the file and go through each line, building up the output file
with open(inputfile) as f:   
    # This structure holds all of the relevant information that we want to print out later
    word_dict = {}
    speaker = ''
    # A regex for the line that has the speaker information 
    regex_speaker_line = re.compile("^Speaker sentences\s+(\d).*")
    # A regex for the line that has the REF sentence
    #regex_REF_line = re.compile("^REF:(.*)")
    # A regex for the line that has the Hypothesis sentence
    #regex_HYP_line = re.compile("^HYP:(.*)")
    # A regex for the line that has the start times of the utterances
    #regex_HT1_line = re.compile("^H_T1:(.*)")
    # A regex for the line that has the end times of the utterances
    #regex_HT2_line = re.compile("^H_T2:(.*)")

    for w in words:
        word_dict[w] = {'total_usages' : 0, 'correct_usages' : 0, 'utterances': []}
    while 1:
        l = f.readline()
        if not l:
            break
    
         # Once we match the speaker line we can read in the other lines
        r = regex_speaker_line.match(l)
        
        if r:
            # We found a new match, so we have a new sentence
            # Add 1 to speaker to make it non-0 based
            speaker = int(r.group(1)) + 1
            handle_sentence(f, words, speaker, word_dict)

# Now that everything is done, let's write information to output
with open(inputfile+".post", "w") as w:
    print word_dict
    for key in word_dict:
        l = len("Word: " + key)
        w.write("Word: " + key + "\n")
        w.write("-" * l + "\n\n")
        w.write("Total Correct: " + str(word_dict[key]['correct_usages']) + "\tTotal Occurrences: " + str(word_dict[key]['total_usages']))
        w.write("\tPercentage Correct: " + str(word_dict[key]['correct_usages']/ word_dict[key]['total_usages']))
        w.write("\nReplacements: \n")

        for e in word_dict[key]['utterances']:
            if key != e['hyp_word']:
                s = "\t" + e['hyp_word']
                if e['time1'] != "":
                    s += "\t" + str(e['time1']) + " - " + str(e['time2'])

                s += "\tSpeaker: " + str(e['speaker']) + "\n"

                
                
                w.write(s)
        w.write("\n\n")

        w.write("Trigrams of failures: \n");

        for e in word_dict[key]['utterances']:
            if key != e['hyp_word']:
                w.write("\t" + e['trigram'] + "\n")
        
            
