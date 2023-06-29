#
# spinal-tap.py
# Zhao Xin (Charles) Ong, 21450673
#
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from datetime import datetime
import numpy as np
import sys
import os
import random

# GLOBAL VARIABLES
SIZE = 500
SMALL_HEIGHT = 50

class Light():
    radius = 20                         # Light radius
    w = 20                              # Light beam's width
    
    def __init__(self, pos, colour="red", direc="down", inten=11, type="spot", hatch=""):
        self.pos = pos
        self.colour = colour
        self.direc = direc.lower()
        self.inten = inten * 1/11       # intensity will be 0 to 11, so we need to be converted to a range between 0 and 1
        self.type = type.lower()
        self.range = [self.pos+self.w, self.pos-self.w, self.inten]     # Light beam's range (left, right, intensity)
        self.hatch = hatch
        
        checkPos(self.pos)
        self.inten = checkInten(self.inten)
        self.hatch = checkHatch(self.hatch)
        
        # Setting light's range based on direction and type
        skew = [60,60]
        
        if self.direc == "left":
            skew[0] += 40
            skew[1] -= 40
        
        elif self.direc == "right":
            skew[0] -= 40
            skew[1] += 40
        
        if self.type == "laser":
            self.w = 5
            skew[0] = 0
            skew[1] = 0
            
        self.range[0] = self.pos - self.w - skew[0]
        self.range[1] = self.pos + self.w + skew[1]
        
        checkPos(self.range[0])
        checkPos(self.range[1])
        
    def plotLight(self, ax):
        if self.type == "laser":
            self.radius = 10
            
        circle1 = plt.Circle([self.pos,25],self.radius, facecolor=self.colour, alpha=self.inten, hatch=self.hatch)
        ax.add_patch(circle1)
        
    def plotLightStage(self, ax):
        # Light Base
        base = Polygon([(self.pos-self.w, SIZE-10),(self.pos+self.w, SIZE-10),(self.pos+self.w, SIZE),(self.pos-self.w, SIZE)], facecolor=self.colour,  alpha=self.inten, edgecolor = None, hatch=self.hatch)
        ax.add_patch(base)
        
        # Light Beam
        beam = Polygon([(self.pos-self.w,SIZE-10),(self.pos+self.w,SIZE-10),(self.range[1],0),(self.range[0],0)], facecolor=self.colour, alpha=self.inten, edgecolor = None, hatch=self.hatch)
        ax.add_patch(beam)
        
    def __str__(self):
        return str(self.pos) + ", " + self.colour 

class SmokeMachine():
    def __init__(self, pos, direc="up", inten=11, neigh="moore"):
        self.pos = pos
        self.direc = direc
        self.inten = inten * 1/11       # intensity will be 0 to 11, so it needs to be converted to a range between 0 and 1
        self.neigh = neigh.lower()      # diffusion type: either moore (m) or von neumann (vn)
        self.smokes = []
        self.step = 0
        self.last_length = 0
        self.max_steps = 3              # how many steps smokes can be expanded
        
        checkPos(self.pos)
        self.inten = checkInten(self.inten)
        
        if self.direc == "up":
            self.smokes.append([[self.pos-20, self.pos+20, self.pos+20, self.pos-20], [40, 40, 0, 0], self.inten])
        elif self.direc == "down":
            self.smokes.append([[self.pos-20, self.pos+20, self.pos+20, self.pos-20], [SIZE, SIZE, SIZE-40, SIZE-40], self.inten])
        else:
            print("WARNING: DIRECTION '" + str(direc) + "'IS NOT A VALID DIRECTION. THE DEFAULT 'up' WILL BE USED INSTEAD")
            self.direc = "up"
        
        if self.neigh != "m" and self.neigh != "vn":
            print("WARNING: DIFFUSION TYPE '" + str(direc) + "'IS NOT A VALID DIFFUSION TYPE. THE DEFAULT 'm' WILL BE USED INSTEAD")
            self.neigh = "m"
            
        
    def stepChange(self):
        
        self.step += 1
        curr_length = len(self.smokes)
        
        # Moore Neighbourhood
        if self.neigh == "m" and self.step < self.max_steps:
            for i in range(self.last_length,curr_length):
                # West
                if i < self.last_length + self.step or self.step == 1:
                    self.smokes.append([[self.smokes[i][0][0]-40, self.smokes[i][0][0], self.smokes[i][0][0], self.smokes[i][0][0]-40],[self.smokes[i][1][0], self.smokes[i][1][1], self.smokes[i][1][2], self.smokes[i][1][3]],self.smokes[i][2]*0.8])
                # North West or South West
                if i == self.last_length + (self.step-1) or self.step == 1:  
                    # North West
                    if self.direc == "up":
                        self.smokes.append([[self.smokes[i][0][0]-40, self.smokes[i][0][0], self.smokes[i][0][0], self.smokes[i][0][0]-40],[self.smokes[i][1][0]+40, self.smokes[i][1][1]+40, self.smokes[i][1][2]+40, self.smokes[i][1][3]+40],self.smokes[i][2]*0.8])
                    # South West
                    elif self.direc == "down":
                        self.smokes.append([[self.smokes[i][0][0]-40, self.smokes[i][0][0], self.smokes[i][0][0], self.smokes[i][0][0]-40],[self.smokes[i][1][0]-40, self.smokes[i][1][1]-40, self.smokes[i][1][2]-40, self.smokes[i][1][3]-40],self.smokes[i][2]*0.8])  
                # North or South
                if (i >= self.last_length + (self.step-1) and i <= self.last_length + (self.step-1) + (self.step-1)*2) or self.step == 1:   
                    # North
                    if self.direc == "up":
                        self.smokes.append([[self.smokes[i][0][0], self.smokes[i][0][1], self.smokes[i][0][2], self.smokes[i][0][3]],[self.smokes[i][1][0]+40, self.smokes[i][1][1]+40, self.smokes[i][1][2]+40, self.smokes[i][1][3]+40],self.smokes[i][2]*0.8])
                    # South
                    elif self.direc == "down":
                        self.smokes.append([[self.smokes[i][0][0], self.smokes[i][0][1], self.smokes[i][0][2], self.smokes[i][0][3]],[self.smokes[i][1][0]-40, self.smokes[i][1][1]-40, self.smokes[i][1][2]-40, self.smokes[i][1][3]-40],self.smokes[i][2]*0.8])            
                # North East or South East
                if i == self.last_length + (self.step-1) + (self.step-1)*2 or self.step == 1:
                    # North East
                    if self.direc == "up":
                        self.smokes.append([[self.smokes[i][0][1], self.smokes[i][0][1]+40, self.smokes[i][0][1]+40, self.smokes[i][0][1]],[self.smokes[i][1][0]+40, self.smokes[i][1][1]+40, self.smokes[i][1][2]+40, self.smokes[i][1][3]+40],self.smokes[i][2]*0.8])
                    # South East
                    elif self.direc == "down":
                        self.smokes.append([[self.smokes[i][0][1], self.smokes[i][0][1]+40, self.smokes[i][0][1]+40, self.smokes[i][0][1]],[self.smokes[i][1][0]-40, self.smokes[i][1][1]-40, self.smokes[i][1][2]-40, self.smokes[i][1][3]-40],self.smokes[i][2]*0.8])
                # East
                if i >= self.last_length + (self.step-1) + (self.step-1)*2 or self.step == 1:
                    self.smokes.append([[self.smokes[i][0][1], self.smokes[i][0][1]+40, self.smokes[i][0][1]+40, self.smokes[i][0][1]],[self.smokes[i][1][0], self.smokes[i][1][1], self.smokes[i][1][2], self.smokes[i][1][3]],self.smokes[i][2]*0.8])
                
        # Von Neumann Neighbourhood
        elif self.neigh == "vn" and self.step < self.max_steps:
            for i in range(self.last_length,curr_length):
                # West
                if i < self.last_length + self.step or self.step == 1:
                    self.smokes.append([[self.smokes[i][0][0]-40, self.smokes[i][0][0], self.smokes[i][0][0], self.smokes[i][0][0]-40],[self.smokes[i][1][0], self.smokes[i][1][1], self.smokes[i][1][2], self.smokes[i][1][3]],self.smokes[i][2]*0.8])
                # North or South
                if i == self.last_length + (self.step-1) or self.step == 1:   
                    # North
                    if self.direc == "up":
                        self.smokes.append([[self.smokes[i][0][0], self.smokes[i][0][1], self.smokes[i][0][2], self.smokes[i][0][3]],[self.smokes[i][1][0]+40, self.smokes[i][1][1]+40, self.smokes[i][1][2]+40, self.smokes[i][1][3]+40],self.smokes[i][2]*0.8])
                    # South
                    if self.direc == "down":
                        self.smokes.append([[self.smokes[i][0][0], self.smokes[i][0][1], self.smokes[i][0][2], self.smokes[i][0][3]],[self.smokes[i][1][0]-40, self.smokes[i][1][1]-40, self.smokes[i][1][2]-40, self.smokes[i][1][3]-40],self.smokes[i][2]*0.8])
                # East
                if i >= self.last_length + (self.step-1) or self.step == 1:
                    self.smokes.append([[self.smokes[i][0][1], self.smokes[i][0][1]+40, self.smokes[i][0][1]+40, self.smokes[i][0][1]],[self.smokes[i][1][0], self.smokes[i][1][1], self.smokes[i][1][2], self.smokes[i][1][3]],self.smokes[i][2]*0.8])
                
        self.last_length = curr_length
    
    def plotSmoke(self, ax, direction, timestep):
        fade = 1
        if timestep >= 3:
            fade = 2/timestep
        
        for i in self.smokes:
            if direction == "left" and i[0][0]-40 >= 0:
                i[0] = [x-40 for x in i[0]]
                
            elif direction == "right" and i[0][0]+40 <= SIZE-40:    
                i[0] = [x+40 for x in i[0]]
            
            ax.fill(i[0], i[1], color="gray", alpha=i[2]*fade)

    def __str__(self):
        return str(self.pos)+ ", " + str(self.direc)

class Prop():
    def __init__(self, pos, shape="square", move="y", hatch=""):
        self.pos = pos
        self.shape = shape
        self.col = (random.random(), random.random(), random.random())
        self.inten = 0.5                # Default intensity without lighting
        self.move = move.lower()
        self.hatch = hatch
        
        checkPos(self.pos)
        self.hatch = checkHatch(self.hatch)
        
        if move != "y" and move != "n":
            print("WARNING: MOVEMENT '" + str(self.move) + "'IS NOT A VALID MOVEMENT. THE DEFAULT 'y' WILL BE USED INSTEAD")
            self.move = "y"
     
    def plotProp(self, ax):
        if self.shape.lower() == "circle":
            ax.add_patch(plt.Circle([self.pos,20],20, facecolor=self.col, edgecolor="white", alpha=self.inten, hatch=self.hatch))
        elif self.shape.lower() == "triangle":
            ax.fill([self.pos, self.pos, self.pos+20, self.pos-20], [40, 40, 0, 0], facecolor=self.col, edgecolor="white", alpha=self.inten, hatch=self.hatch)
        elif self.shape.lower() == "square":
            ax.fill([self.pos-20, self.pos+20, self.pos+20, self.pos-20], [40, 40, 0, 0], facecolor=self.col, edgecolor="white",alpha=self.inten, hatch=self.hatch)
        else:
            print("WARNING: SHAPE: " + self.shape + " IS NOT A SUPPORTED SHAPE SO A SQUARE HAS BEEN ADDED INSTEAD")
            ax.fill([self.pos-20, self.pos+20, self.pos+20, self.pos-20], [40, 40, 0, 0], facecolor=self.col, edgecolor="white",alpha=self.inten, hatch=self.hatch)
                
    def animate(self, direction):
        step = 0
        if self.move == "y":
            if direction == "left":
                step = random.randrange(-100,0)     # Random movement between -100 and 0
            elif direction == "right":
                step = random.randrange(0,100)      # Random movement between 0 and 100
            else:
                step = random.randrange(-100,100)   # Random movement between -100 and 100
        
        left = 40                       # Left Boundary
        right = SIZE - 40               # Right Boundary
        
        if (self.pos + step) > left and (self.pos + step) < right:
            self.pos = self.pos + step
        elif (self.pos - step) > left and (self.pos - step) < right:
            self.pos = self.pos - step
        else:
            self.pos = SIZE/2           # Reset object to middle of stage
    
    def setLighting(self, ranges):
        for range in ranges:
            # iff prop is within the range of the light beams, increase intensity with light's intensity
            if (self.pos-20 > range[0] and self.pos-20 < range[1]) or  (self.pos+20 > range[0] and self.pos+20 < range[1]):
                new_inten = self.inten + range[2]
                if new_inten > 1:
                    new_inten = 1
                self.inten = new_inten
            else:
                self.inten = 0.5
                
    def __str__(self):
        return self.shape + " @ " + str(self.pos)

def setBackdrop(ax, width, height, col):
    ax.set_aspect("equal")
    ax.fill([0,width,width,0],[0,0,height,height], color=col)

def getChoreography(file_name):
    try:
        file = open(file_name, "r")
        return(file.readlines())
    except OSError as err:
        print("ERROR WITH OPENING FILE: ", err)
    except:
        print("UNEXPECTED ERROR: ", err)

def createLightSet(line):
    light_set = []
    no_lights = int(line[5])
    offset = 0
    colours = line[2].split(" ")
    
    if len(colours) != no_lights:
        print("Warning: number of colours is different to the number of lights. Specify colours for all lights, as colours may be added or removed.")
        while len(colours) != no_lights:        # until number of colours match number of lights
            if len(colours) < no_lights:
                colours.append(colours[0])      # adds the first element's colour to the end of the list
            else:
                colours.pop()                   # removes last element of "colours" list
    
    for i in range(no_lights):
        light_set.append(Light(int(line[1])+offset, colours[i], line[3], int(line[4]), line[6], line[7]))
        # Switches from positive offset to negative offset and vice versa, unless light positions are outside of boundaries
        if offset > 0 and int(line[1]) - offset > 0:
            offset = -offset
        elif offset > 0:
            offset += 100
        elif int(line[1]) + -offset + 100 < SIZE:
            offset = -offset + 100
        else:
            offset -= 100
            
    
    return light_set

def getRange(list):
    ranges = []
    for i in list:
        ranges.append(i.range)
    return ranges

def checkPos(pos):
    if pos < 40 or pos > SIZE-40:
        print("WARNING: POSITION: '" + str(pos) + "' MAY APPEAR OUTSIDE OF THE STAGE")
        
def checkInten(inten):
    if inten < 0 or inten > 1:
        print("WARNING: INTENSITY: '" + str(inten) + "' IS NOT BETWEEN 1 and 11, THE DEFAULT INTENSITY VALUE WILL BE USED INSTEAD")
        return 1
    return inten

def checkHatch(hatch):
    hatches = ['', '/', '|', '\\', '-', '+', 'x', 'o', 'O', '.', '*']
    if hatch in hatches:
        return hatch
    print("WARNING: HATCH (PATTERN): '" + str(hatch) + "' IS NOT A RECOGNISIBLE PATTERN, THE DEFAULT HATCH (PATTERN) VALUE WILL BE USED INSTEAD")
    return ''
        

def main():
    FILENAME = ""
    FRAMES = 15
    FILE = False
    SAVE = False
    DIRECTION = None
    Backdrop = []
    Lights = []
    Smokes = []
    Props = []
    
    # CHECKS COMMAND LINE ARGUMENTS
    for i in sys.argv:
        if i == "spinal-tap.py":
            continue
        elif ".csv" in i:
            FILE = True
        elif "." in i:
            print("WARNING, UNKNOWN FILE, '" + i + "' DETECTED IN COMMAND LINE ARGUMENTS. PLEASE USE .csv FILE IF YOU ARE INTENDING TO USE A PRE-SET CHOREOGAPHY")
        elif "-s" in i:
            SAVE = True
        else:
            print("WARNING, UNKNOWN COMMAND LINE ARGUMENT USED: " + i)
    
    if FILE:
        # INITIALISES USING CHOREOGRAPHY FILE
        data = getChoreography(sys.argv[1])
        FILENAME = sys.argv[1] + " " + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " images"
        for line in data:
            splitline = line.strip().replace("\ufeff", "").split(",") # removes "\ufeff" that occurs infront of some strings
            
            if splitline[0].lower() == "frames":
                FRAMES = int(splitline[1])
            
            elif splitline[0].lower() == "direction":
                DIRECTION = splitline[1]
            
            elif splitline[0].lower() == "backdrop":
                Backdrop.append(splitline[1])
                
            elif splitline[0].lower() == "light":
                # One Light
                if int(splitline[5]) < 2 or splitline[5] == "":
                    Lights.append(Light(int(splitline[1]), splitline[2], splitline[3], int(splitline[4]), splitline[6], splitline[7]))
                # Light Set
                else:
                    Lights.extend(createLightSet(splitline))
            
            elif splitline[0].lower() == "smoke":
                Smokes.append(SmokeMachine(int(splitline[1]), splitline[2], int(splitline[3]), splitline[4]))
                
            elif splitline[0].lower() == "prop":
                Props.append(Prop(int(splitline[1]), splitline[2], splitline[3], splitline[4]))
                
    else:
        # INITIALISES (DEFAULT SETTINGS WITHOUT CHOREOGRAPHY FILE)
        FILENAME = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        ## Backdrop
        Backdrop.append("black")
        
        ## Lights array & lights
        Lights.append(Light(250,"red","down",11))
        Lights.append(Light(350,"blue","up",5))
    
        ## Smoke Machine
        smoke1 = SmokeMachine(250, "up", 11, "m")
        Smokes.append(smoke1)
        
        # Props/Band
        prop1 = Prop(50, "square")
        Props.append(prop1)
        
    # PLOTTING
    fig, (ax0, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 10]}, figsize = (10,10))
    
    if SAVE:
        os.mkdir(FILENAME)         # make folder for for saving images
    
    light_ranges = getRange(Lights)
    
    for timestep in range(FRAMES):
        print("\n Timestep: ",timestep)
        
        # Backdrop
        setBackdrop(ax0, SIZE, SMALL_HEIGHT, Backdrop[0])
        setBackdrop(ax1, SIZE, SIZE, Backdrop[0])
        
        ## Lights
        for i in Lights:
            i.plotLight(ax0)
            i.plotLightStage(ax1)
        
        ## Props
        for i in Props:
            i.setLighting(light_ranges)
            i.plotProp(ax1)
            i.animate(DIRECTION)
        
        ## Smoke
        for i in Smokes:
            i.plotSmoke(ax1, DIRECTION, timestep)
            i.stepChange()

        fig.suptitle("Spinal Tap", fontsize="18")
        ax0.set_title("Lights View")
        ax1.set_title("Stage View")
        fig.show()
        
        if SAVE:
            plt.savefig(FILENAME + "/" + str(timestep) + ".png")
            
        if timestep < FRAMES:
            plt.pause(0.5)
            ax0.clear()
            ax1.clear()

if __name__ == "__main__":
    main()