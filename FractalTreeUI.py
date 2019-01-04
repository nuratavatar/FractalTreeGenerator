# Tarun Mandalapu 2017

# import statements for all of the graphics libraries
# there is a distinction between python 2 and python 3
# in terms of what they call the Tkinter library
try:
    import Tkinter as tk
    import ttk
except ImportError: #for python 3.3
    import tkinter as tk
    from tkinter import ttk

# (R)ushy (P)anchal modified Zelle's graphics library
# to support GraphWins within frames
import RP_graphics as graphics

# utilities as needed
import math
from random import randint

#Simple drawline function
#Draws a line in window 'w', starting at point p0, at an angle of 'theta' from the horizontal, with length 'L', width 'width', and colors it 'color'
def drawLine(w, p0, theta, L, width, color):
    #Get the ending x and y values by adding the x component of the L vector to the p0's x value and the y component of the L vector to p0's y value 
    x1 = p0.getX() + L * math.cos(math.pi/180 * theta)
    y1 = p0.getY() + L * math.sin(math.pi/180 * theta)
    p1 = graphics.Point(x1, y1)
    line = graphics.Line(p0, p1); line.setOutline(color); line.setWidth(width); line.draw(w)
    return p1

def getEndpoint(w, p0, theta, L, color):
    x1 = p0.getX() + L * math.cos(math.pi/180 * theta)
    y1 = p0.getY() + L * math.sin(math.pi/180 * theta)
    p1 = graphics.Point(x1, y1)
    return p1

def fracTrees(win, lvl, clvl, p0, angle, theta, sf, L, width, season):
    if(season == 'fall'):
        colors = ['green4', 'DarkOrange1', 'yellow', 'orange red']
        win.setBackground('turquoise1')
    elif(season == 'summer'):
        colors = ['green4', 'dark green', 'forest green']
        win.setBackground('turquoise1')
    elif(season == 'winter'):
        colors = ['snow']
        win.setBackground('snow')
    elif(season == 'spring'):
        colors = ['green2', 'green3']
        win.setBackground('deep sky blue')
    else:
        colors = ['black']

    if(clvl == 0):
        p1 = drawLine(win, p0, angle, L, width, 'saddle brown') #draw trunk and set current point to endpoint
        L *= sf #length is changed by scale factor
        clvl += 1 #current level increases by one
        fracTrees(win, lvl, clvl, p1, angle, theta, sf, L, width, season) #Left branch


    elif(lvl > clvl):
        #leaves
        if(clvl/lvl > 1/2):
            width = 4
            rand = randint(0, len(colors)-1)
            color = colors[rand]
        #trunk + branches
        else:
            color = 'saddle brown'
            width *= sf

        #Preparing values for next iteration
        clvl += 1
        sfv = randint(0, 50)/100
        randangle = randint(0, 25)
        randangle2 = randint(0, 25)
        angleR = angle - (theta + randangle)
        angleL = angle + (theta + randangle2)
        #Drawing branches
        pR = drawLine(win, p0, angleR, L* (sf+sfv), width, color) #Right branch
        fracTrees(win, lvl, clvl, pR, angleR, theta, sf, L*sf, width, season) #Continuing from right branch
        pL = drawLine(win, p0, angleL, L* (sf+sfv), width, color) #Left branch
        fracTrees(win, lvl, clvl, pL, angleL, theta, sf, L*sf, width, season) #Continuing from left branch


# change the name of 'LinearEquationExplorerApp' as necessary
class LinearEquationExplorerApp:

   
    # constructor for App class, which implements an App to
    # explore equations of the form Y = MX + B
    def __init__(self, master):
        self.master = master

        #*************************************************************
        #Fractal Tree Explorer Instance Fields

        #Tree Season
        self.season = "None"
        self.seasonVar = tk.StringVar()

        #Starting length
        self.L = 3.0
        self.lScaleVar = tk.DoubleVar()

        #Level of fractal tree to be drawn
        self.lvl = 15
        self.lvlScaleVar = tk.IntVar()
        
        #Branch angle of fractal tree
        self.angle = 45
        self.angleScaleVar = tk.IntVar()

        #Scale factor at which the length and width change per level
        self.sf = 0.67
        self.sfScaleVar = tk.DoubleVar()

        #Starting width
        self.width = 15.0
        self.widthScaleVar = tk.DoubleVar()

        #3. default window settings for graph window &
        #   storage of current window settings
        self.defaultCoords = (-10, -10, 10, 10)
        self.minx = self.defaultCoords[0]
        self.miny = self.defaultCoords[1]
        self.maxx = self.defaultCoords[2]
        self.maxy = self.defaultCoords[3]

        #*************************************************************
        # the main frames for this program

        # 1. the outer, container frame of the entire thing
        self.frame = tk.Frame(self.master, background = 'gray11')

        # 2. the plot window will go inside of drawFrame
        self.drawFrame = tk.Frame(self.frame, bg = "gray15")
        self.drawFrame.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = tk.N)

        # 3. the frame to hold the controls (buttons, sliders, etc.)
        self.controlFrame = tk.Frame(self.frame, bg = 'gray15')
        self.controlFrame.grid(row = 1, column = 2, padx = 10, pady = [10,100], sticky = tk.N + tk.S)

        #*************************************************************
        # setting up graph window
        self.graph = graphics.GraphWin(self.drawFrame, 600, 450, autoflush = False)
        self.graph.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.graph.setCoords(self.defaultCoords[0], self.defaultCoords[1], self.defaultCoords[2], self.defaultCoords[3])
        self.graph.setBackground('turquoise1')
        #Control Frame Title
        self.instructions = "INSTRUCTIONS:\n1. Use sliders to customize your tree \n2. Select a season\n3. Click the DRAW button\n 4. Click anywhere to grow tree\n 5. You can do this multiple times!\n 6. Click the CLEAR button to clear"
        self.instructionsLabel = tk.Label(self.drawFrame, text = self.instructions, justify = "left", fg = 'white', bg = 'gray15')
        self.instructionsLabel.grid(row = 0, column = 1, padx = 5, pady = 0, sticky = tk.W)

        #*************************************************************
        # setting up controls in control frame

        #Control Frame Title
        self.controlLabel = tk.Label(self.controlFrame, text = "Inputs for Fractal Tree Explorer", fg = 'white', bg = 'gray15')
        self.controlLabel.grid(row = 10, column = 1, columnspan = 1, padx = 5, pady = 15)

        #Length Scroll
        self.lScroll = tk.Scale(self.controlFrame, from_ = 0, to = 10, tickinterval = 1, resolution = 1)
        self.lScroll.configure(label = "Trunk Length", orient = tk.HORIZONTAL)
        self.lScroll.configure(bg = 'gray15', fg = 'white', troughcolor = 'white', activebackground = 'gray15')
        self.lScroll.configure(variable = self.lScaleVar)
        self.lScroll.grid(row = 20, column = 1, columnspan = 1, padx = 10, pady = 2, sticky = tk.W + tk. E)

        #Level Scroll
        self.lvlScroll = tk.Scale(self.controlFrame, from_ = 0, to = 20, tickinterval = 5, resolution = 1)
        self.lvlScroll.configure(label = "Level of Fractal Tree", orient = tk.HORIZONTAL)
        self.lvlScroll.configure(bg = 'gray15', fg = 'white', troughcolor = 'white', activebackground = 'gray15')
        self.lvlScroll.configure(variable = self.lvlScaleVar)
        self.lvlScroll.grid(row = 30, column = 1, columnspan = 1, padx = 10, pady = 2, sticky = tk.W + tk.E)

        #Angle Scroll
        self.angleScroll = tk.Scale(self.controlFrame, from_ = 0, to = 90, tickinterval = 15, resolution = 1)
        self.angleScroll.configure(label = "Branch Angles", orient = tk.HORIZONTAL)
        self.angleScroll.configure(bg = 'gray15', fg = 'white', troughcolor = 'white', activebackground = 'gray15')
        self.angleScroll.configure(variable = self.angleScaleVar)
        self.angleScroll.grid(row = 40, column = 1, columnspan = 1, padx = 10, pady = 2, sticky = tk.W + tk.E)

        #Scale Factor Scroll
        self.sfScroll = tk.Scale(self.controlFrame, from_ = 0, to = 1, tickinterval = .2, resolution = 0.01)
        self.sfScroll.configure(label = "Scale Factor", orient = tk.HORIZONTAL)
        self.sfScroll.configure(bg = 'gray15', fg = 'white', troughcolor = 'white', activebackground = 'gray15')
        self.sfScroll.configure(variable = self.sfScaleVar)
        self.sfScroll.grid(row = 50, column = 1, columnspan = 1, padx = 10, pady = 2, sticky = tk.W + tk.E)

        #Width Scroll
        self.widthScroll = tk.Scale(self.controlFrame, from_ = 0, to = 20, tickinterval = 4, resolution = 1)
        self.widthScroll.configure(label = "Width", orient = tk.HORIZONTAL)
        self.widthScroll.configure(bg = 'gray15', fg = 'white', troughcolor = 'white', activebackground = 'gray15')
        self.widthScroll.configure(variable = self.widthScaleVar)
        self.widthScroll.grid(row = 55, column = 1, columnspan = 1, padx = 10, pady = 2, sticky = tk.W + tk.E)

        #Frame for seasons radio buttons
        self.seasonsFrame = tk.LabelFrame(self.controlFrame, bg = 'gray15', fg= 'white')
        self.seasonsFrame.configure(text = "Choose a season")
        self.seasonsFrame.grid(row = 60, column = 1, columnspan = 2, padx = 2, pady = 5, sticky = tk.N + tk.S)

        #Spring R-Button
        self.SpringButton = tk.Radiobutton(self.seasonsFrame, text = "Spring", indicatoron = 0, variable = self.seasonVar, value = 'spring')
        self.SpringButton.configure(width = 8)
        self.SpringButton.grid(row = 1, column =1, padx = (3,1), pady = 2)

        #Summer R-Button
        self.SummerButton = tk.Radiobutton(self.seasonsFrame, text = "Summer", indicatoron = 0, variable = self.seasonVar, value = 'summer')
        self.SummerButton.configure(width = 8)
        self.SummerButton.grid(row = 1, column = 2, padx = (1,3), pady = 2)

        #Fall R-Button
        self.FallButton = tk.Radiobutton(self.seasonsFrame, text = "Fall", indicatoron = 0, variable = self.seasonVar, value = 'fall')
        self.FallButton.configure(width = 8)
        self.FallButton.grid(row = 2, column = 1, padx = (3,1), pady = 2)

        #Winter R-Button
        self.WinterButton = tk.Radiobutton(self.seasonsFrame, text = "Winter", indicatoron = 0, variable = self.seasonVar, value = 'winter')
        self.WinterButton.configure(width = 8)
        self.WinterButton.grid(row = 2, column = 2, padx = (1,3), pady = 2)

        #Frame for DRAW & CLEAR buttons
        self.drawclearFrame = tk.LabelFrame(self.controlFrame, bg = 'gray15', fg = 'white')
        self.drawclearFrame.configure(text = "control buttons")
        self.drawclearFrame.grid(row = 70, column = 1, padx = 0, pady = 5, sticky = tk.N + tk.S)

        #DRAW button
        self.drawTreeButton = ttk.Button(self.drawclearFrame, text = "DRAW", command = lambda: self.acceptInputs())
        self.drawTreeButton.grid(row = 1, column = 1, padx = (3,1), pady = 2, sticky = tk.W + tk.E)

        #CLEAR button
        self.clearButton = ttk.Button(self.drawclearFrame, text = "CLEAR", command = lambda: self.erase())
        self.clearButton.grid(row = 1, column = 2, padx = (1,3), pady = 2, sticky = tk.W + tk.E)

        # initialize scale widgets to corresponding initial parameter values
        self.lScaleVar.set(self.L)
        self.lvlScaleVar.set(self.lvl)
        self.angleScaleVar.set(self.angle)
        self.sfScaleVar.set(self.sf)
        self.widthScaleVar.set(self.width)
        self.frame.pack()

    def acceptInputs(self):
        #Getting values all scrollbars
        self.L = self.lScaleVar.get()
        self.lvl = self.lvlScaleVar.get()
        self.angle = self.angleScaleVar.get()
        self.sf = self.sfScaleVar.get()
        self.width = self.widthScaleVar.get()
        self.season = self.seasonVar.get()
        #Clear Graph
        self.erase()

        #Whenever the user clicks, draw a tree with their settings at that point
        while(1):
            p0 = self.graph.getMouse()
            self.drawTree(p0)

    def drawTree(self, p0):
        fracTrees(self.graph, self.lvl, 0, p0, 90, self.angle, self.sf, self.L, self.width, self.season)
        

    def erase(self):
        self.graph.clear()

    def shutDown(self):
        self.root.quit()
