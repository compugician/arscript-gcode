import numpy
import itertools
import re

def gcode():

#first check to see if you have the relevant files in the right places
    if raw_input("This file assumes that you have created within the same directory as the one from which this script is running, the following EMPTY files: teststrokeout.txt, teststrokexyz.txt and teststrokeg.txt.\n Please check to see if all these files exist in the right directory (if you are running this script from your shell, type 'pwd' into your shell and afterwards I'd suggest 'vim -m FILENAME', where FILENAME is replaced by 'teststrokeout.txt' (no quotes) or something. After opening up the file, type ESC and then :x to save and exit the file.).\n Type 'yes' (no quotes) to proceed: ") != 'yes':
        print "Please create these files and then proceed. This program will now quit."
        quit()

#writes out strokeevent lines to teststrokeout.txt  
    with open(raw_input("Please specify the input file WITH the extension, e.g. stroke.txt. Thie file MUST be a .arscript file converted into .txt form and MUST be in the same directory as the one from which this file roughparser.py is running: ")) as f:
        with open("teststrokeout.txt", "w") as f1:
            for line in f:
                if "</StrokeHeader>" in line: 
                    for line in f:
                        if "Loc:" in line:      
                            f1.write(line)

#writes out all xy coordinates into teststrokexyz.txt   
    with open("teststrokeout.txt", "r+") as f: 
        with open("teststrokexyz.txt", "w") as f1: 
            for line in f:
                split = line.split()
                if "Pr:" in split:
                    for word in split: 
                        if "(" in word or ")" in word:
                            f1.write(word)   
                    pressure = split[split.index("Pr:")+1]
                    f1.write("," + pressure + ",")   
    
#converts the xy coordinates into a list of numbers, from which i subtract each xy entry from its previous entry and then convert the resulting xy coordinates into gcode
    with open("teststrokexyz.txt", "r+") as f:
        fdata = f.read() 
        with open("squareg4.txt", "w") as f1: 
            tuplist = filter(None, re.split("[, )(]+", fdata))
            tupl = []

            for word in tuplist: 
                tupl.append(word)
            tupG = []

            for a in tupl: 
                tupG.append(float(a))   
            gX = tupG[0::3]
            gY = tupG[1::3]
            gZ = tupG[2::3]
            print len(gZ)
            for z in range(len(gZ)):
                f1.write("G01 X" + str(gX[z]) + " Y" + str(gY[z]) + " Z" + str(gZ[z])+ " F2500\n")
    print "The script has output gcode to teststrokeg.txt." 
gcode()

