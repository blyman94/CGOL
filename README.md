# Conway's Game of Life (CGOL)

A simple implementation of the famous Conway's Game of Life. In this           
application, a NumPy array is used to track the status (living or dead) of the 
cells on the gameboard, which is drawn using PyQt5's painter object. The user 
can interact with CGOL in the following ways:

	1. Start the game.
	2. Pause the game.
	3. Adjust the speed of the game.
	4. Change the colors of the alive and dead cells.
	5. Experiment with famous starting conditions (Pulsar,
	   Penta-Decathalon, and Gosper Glider Gun)

The rules and starting conditions for Conway's Game of Life were researched on
Wikipedia. For more information on rules and starting conditions, please visit
the following page:

	https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

The main script in the package is "cgol_main.py". The script's main function
creates a Conway object which contains all elements of CGOL and its user
interface.

# Installation

"cgol_main.py" is dependent on the following Python packages:

	Package   | Function
	------------------------------------------------------------------
	sys       | Interact with operating system to create applications.
	PyQt5     | Create windows, buttons, paint, and other UI elements.
	numpy     | Matrix calculations.
	os        | Directory management for file retrieval.
	------------------------------------------------------------------

Lines 8-19 of "ols_main.py" import these packages. If there is an issue with
importing these libraries, simply use the "pip" or "conda" command from the
Python or Anaconda shell, respectively, to properly install them.

# Usage

With the proper Python environment installed, "cgol_main.py" can be run 
simply by double clicking the file in Windows File Explorer.

Each of the UI elements can be used to manipulate the game board in the ways 
described above. Tooltips are provided to ensure controls are used correctly
and the user is aware of each UI element's function.

# Changelog

	Version | Date       | Notes
	------------------------------------------------------------
	1.0.0   | 06-19-2020 | First end-to-end implementation of 
			       Conway's Game of Life for this 
			       project.
	-------------------------------------------------------------

# Known Issues

	1. If the game board is running (not paused) when the "Reset" button
	   or any starting condition button is pressed, the game board may 
	   reflect the second generation of the starting condition instead of
	   the actual starting condition. This is not a critical bug.
	
	   The speed of the game is determined by a while loop, wherein the 
	   command
	
	   QtTest.QTest.qWait(self.speed)

	   Is called. If the user makes a change to the application during this
	   waiting period

	   self.goToNextGen()

	   Will be called at the conclusion of the waiting period.

# Authors

Brandon C Lyman
