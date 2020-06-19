# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:55:07 2020

@author: Brandon Lyman
"""

# PyQt Packages
import sys
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QWidget, 
                             QPushButton, QStyle, QSlider, QLabel, 
                             QColorDialog, QGroupBox, QGridLayout)
from PyQt5.QtGui import QPainter, QBrush, QPen
import PyQt5.QtCore as QtCore
from PyQt5 import QtTest

# Other Packages
import numpy as np
import os

ROOT =  os.path.dirname(os.path.realpath(__file__)) + '/'

class Conway(QWidget):
    """A PyQtWidget with all elements necessary to implement the famous
    Conway's game of life application."""
    def __init__(self):

        super().__init__()

        self.title = "Conway's Game of Life"
        self.width = 400
        self.height = 600
        self.baseSpeed = 101
        self.aliveColor = QtCore.Qt.blue
        self.deadColor = QtCore.Qt.white
        self.speed = self.baseSpeed
        self.initUI()
        self.center()
        
        self.gosper = False
        self.gridSize = 20
        self.squareSize = 50
        self.grid = np.random.randint(2,size = (self.gridSize,self.gridSize))
     
    def center(self):
        "Centers the Conway object window on the desktop."
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def getNeighbors(self,pos):
        """Retrieve a list of neighbors in a given cell.
        
        Conway's game of life is governed by rules involving the neighboring
        cells of each cell on the game board. This function identifies the 
        neighbor cells of a given position on the grid, so that the rules may
        be applied to the subject cell. 
        
        For the Gosper Glider Gun, the sides of the game board are unstitched, 
        as the gliders are intended to go on forever without interfering with
        their source.
        
        """
        up_row = pos[0] - 1
        down_row = pos[0] + 1
        left_col = pos[1] - 1
        right_col = pos[1] + 1
        
        if self.gosper:
            neighbor_list = [(up_row,left_col),(up_row,pos[1]),(up_row,right_col),
               (pos[0],left_col),(pos[0],right_col),
               (down_row,left_col),(down_row,pos[1]),(down_row,right_col)]
            
            if up_row < 0:
                try:
                    neighbor_list.remove((up_row,left_col))
                    neighbor_list.remove((up_row,pos[1]))
                    neighbor_list.remove((up_row,right_col))
                except ValueError:
                    pass
            if left_col < 0:
                try:
                    neighbor_list.remove((up_row,left_col))
                except ValueError:
                    pass
                neighbor_list.remove((pos[0],left_col))
                neighbor_list.remove((down_row,left_col))
            if down_row > self.gridSize - 1:
                try:
                    neighbor_list.remove((down_row,left_col))
                except ValueError:
                    pass
                neighbor_list.remove((down_row,pos[1]))
                neighbor_list.remove((down_row,right_col))
                
            if right_col > self.gridSize - 1:
                try:
                    neighbor_list.remove((up_row,right_col))
                except ValueError:
                    pass
                try:
                    neighbor_list.remove((down_row,right_col))
                except ValueError:
                    pass
                
                neighbor_list.remove((pos[0],right_col))
            
        else:
            
            if up_row < 0:
                up_row = self.gridSize - 1
            if left_col < 0:
                left_col = self.gridSize - 1
            if down_row > self.gridSize - 1:
                down_row = 0
            if right_col > self.gridSize - 1:
                right_col = 0
                
            neighbor_list = [(up_row,left_col),(up_row,pos[1]),(up_row,right_col),
               (pos[0],left_col),(pos[0],right_col),
               (down_row,left_col),(down_row,pos[1]),(down_row,right_col)]
        
        return neighbor_list
    
    def goToNextGen(self):
        """Calculate the next generation of cells.
        
        Uses the rules of Conway's Game of Life to create a new generation of
        cells based on the current generation of cells, then updates the window
        so the Painter object re-draws the grid.
        
        Conway's Game of Life Rules (per Wikipedia):
            
            1. Any live cell with two or three live neighbours survives.
            2. Any dead cell with three live neighbours becomes a live cell.
            3. All other live cells die in the next generation. Similarly, 
            all other dead cells stay dead.
            
        """
        nextgen = np.array([[0]*self.gridSize]*self.gridSize)
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                neighbors = self.getNeighbors((i,j))
                testsum = self.grid[i,j]
                for n in neighbors:
                    testsum += self.grid[n[0],n[1]] 
                if testsum == 3:
                    nextgen[i,j] = 1
                elif testsum == 4:
                    nextgen[i,j] = self.grid[i,j]
                else:
                    nextgen[i,j] = 0
        
        self.grid = nextgen
        self.update()

    def initUI(self):
        """Initialize User Interface
        
        Populates the window with userful UI elements, including:
            
            1. Start, Pause, and Reset buttons.
            2. A speed slider.
            3. Color selection buttons and associated dialogs
            4. Pulsar, Penta-Decathalon, and Gosper Glider Gun buttons, which
            change the initial state of the application for predictable 
            results. The initial states are read in from provided CSV files.
            
        Each of these elements are connected to functions that materialize
        their effects in the game board.
            
        """
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        
        # Media Buttons
        self.btnStart = QPushButton(self) 
        self.btnStart.setGeometry(QtCore.QRect(155, 365, 45, 25)) 
        self.btnStart.setIcon(self.style()
                              .standardIcon(getattr(QStyle, 'SP_MediaPlay')))
        self.btnStart.setToolTip('Start')
        self.btnPause = QPushButton(self) 
        self.btnPause.setGeometry(QtCore.QRect(195, 365, 45, 25)) 
        self.btnPause.setIcon(self.style()
                              .standardIcon(getattr(QStyle, 'SP_MediaPause')))
        self.btnPause.setToolTip('Pause')
        
        # Speed Slider
        lblSlow = QLabel("Slow", self)
        lblSlow.setGeometry(QtCore.QRect(65, 400, 25, 25)) 
        self.slSpeed = QSlider(QtCore.Qt.Horizontal, parent = self)
        self.slSpeed.setGeometry(QtCore.QRect(96, 400, 200, 25)) 
        self.slSpeed.setMinimum(-10)
        self.slSpeed.setMaximum(10)
        self.slSpeed.setValue(0)
        self.slSpeed.setTickPosition(QSlider.TicksBelow)
        self.slSpeed.setTickInterval(1)
        self.slSpeed.setToolTip('Change tick speed.')
        lblFast = QLabel("Fast", self)
        lblFast.setGeometry(QtCore.QRect(305, 400, 25, 25)) 
        
        # Color Selection
        group = QGroupBox("Change Colors",self)
        grid = QGridLayout()
        self.btnAliveColor = QPushButton("Alive...",self)
        self.btnAliveColor.setToolTip('Change color of alive cells.')
        self.btnDeadColor = QPushButton("Dead...",self)
        self.btnDeadColor.setToolTip('Change color of dead cells.')
        grid.addWidget(self.btnAliveColor,0,0)
        grid.addWidget(self.btnDeadColor,0,1)
        group.setLayout(grid)
        group.setGeometry(QtCore.QRect(35,435,325,60))

        # Starting Conditions
        group = QGroupBox("Starting Conditions",self)
        
        grid = QGridLayout()
        
        self.btnPulsar = QPushButton("Pulsar",self)
        self.btnPulsar.setToolTip("Change to 'Pulsar' initial state.")
        self.btnPenta = QPushButton("Penta-Decathalon",self)
        self.btnPenta.setToolTip("Change to 'Penta-Decathalon' initial state.")
        self.btnGosper = QPushButton("Gosper Glider Gun",self)
        self.btnGosper.setToolTip("Change to 'Gosper Glider Gun' " +
                                  "initial state.")
        
        grid.addWidget(self.btnPulsar,0,0)
        grid.addWidget(self.btnPenta,0,1)
        grid.addWidget(self.btnGosper,0,2)
        
        group.setLayout(grid)
        group.setGeometry(QtCore.QRect(35, 500, 325, 60))

        # Reset Button
        self.btnReset = QPushButton('Reset',self) 
        self.btnReset.setGeometry(QtCore.QRect(155, 565, 90, 25)) 
        self.btnReset.setToolTip("Reset program to a random initial state.")

        self.show()
        
        self.btnStart.clicked.connect(self.onClickStart)
        self.btnPause.clicked.connect(self.onClickPause)
        self.slSpeed.valueChanged.connect(self.onSpeedChange)
        self.btnReset.clicked.connect(self.onClickReset)
        self.btnAliveColor.clicked.connect(self.onClickAliveColor)
        self.btnDeadColor.clicked.connect(self.onClickDeadColor)
        self.btnPulsar.clicked.connect(self.onClickPulsar)
        self.btnPenta.clicked.connect(self.onClickPenta)
        self.btnGosper.clicked.connect(self.onClickGosper)
    
    def onClickAliveColor(self):
        "Changes the color of living cells to the user's choice."
        self.running = False
        self.aliveColor = QColorDialog.getColor()
        
    def onClickDeadColor(self):
        "Changes the color of dead cells to the user's choice."
        self.running = False
        self.deadColor = QColorDialog.getColor()
    
    def onClickGosper(self):
        "Changes the initial state of the game to the Gosper Glider Gun."
        self.running = False
        self.gosper = True
        self.baseSpeed = 101
        self.slSpeed.setValue(0)
        self.gridSize = 50
        self.squareSize = 20
        self.grid = np.loadtxt(open(ROOT + "inputs/gosper.txt", "rb"),
                               delimiter=",").T
        self.update()
        
    def onClickPause(self):
        "Pauses Conway's game of life on the game board."
        self.running = False
    
    def onClickPenta(self):
        "Changes the initial state of the game to the Penta-Decathalon."
        self.running = False
        self.baseSpeed = 801
        self.speed = self.baseSpeed
        self.slSpeed.setValue(0)
        self.gridSize = 20
        self.squareSize = 50
        self.grid = np.loadtxt(open(ROOT + "inputs/penta.txt", "rb"),
                               delimiter=",").T
        self.update()
    
    
    def onClickPulsar(self):
        "Changes the initial state of the game to the Pulsar."
        self.running = False
        self.baseSpeed = 801
        self.speed = self.baseSpeed
        self.slSpeed.setValue(0)
        self.gridSize = 20
        self.squareSize = 50
        self.grid = np.loadtxt(open(ROOT + "inputs/pulsar.txt", "rb"),
                               delimiter=",").T
        self.update()
        
    def onClickReset(self):
        """Resets the game to its initial state. This means a random intial 
        state for the game board, blue and white for alive and dead colors
        respectively, and changing the base speed back to 101."""
        self.running = False
        self.aliveColor = QtCore.Qt.blue
        self.deadColor = QtCore.Qt.white
        self.gridSize = 20
        self.squareSize = 50
        self.base_speed = 101
        self.speed = self.baseSpeed
        self.slSpeed.setValue(0)
        self.grid = np.random.randint(2,size = (self.gridSize,self.gridSize))
        self.update()
    
    def onClickStart(self):
        "Runs Conway's game of life on the game board."
        self.running = True
        while self.running:
            QtTest.QTest.qWait(self.speed)
            self.goToNextGen()
        
    def onSpeedChange(self):
        """Changes the speed of Conway's game of life by increasing or 
        decreasing the time in between updates."""
        self.speed = self.baseSpeed + (self.slSpeed.value()*
                                       -(self.baseSpeed*0.1))
        
    def paintEvent(self, event):
        """Creates a painter object to construct a visual representation of 
        Conway's Game of Life."""
        painter = QPainter(self)
        painter.setPen(QPen(QtCore.Qt.black,1,QtCore.Qt.SolidLine))
        painter.setWindow(-100,-50,1200,1800)
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if self.grid[row,col] == 0:
                    painter.setBrush(QBrush(self.deadColor,
                                            QtCore.Qt.SolidPattern))
                    painter.drawRect(row*self.squareSize,col*self.squareSize,
                                     self.squareSize,self.squareSize)
                else:
                    painter.setBrush(QBrush(self.aliveColor,
                                            QtCore.Qt.SolidPattern))
                    painter.drawRect(row*self.squareSize,col*self.squareSize,
                                     self.squareSize,self.squareSize)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Conway()
    sys.exit(app.exec())