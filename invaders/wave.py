"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Khushi Patel (ksp67)
# December 9, 2021
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class are to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _direction: The current direction of the Alien Wave
    # Invariant: _direction is either +1 or -1.
    #
    # Attribute _lastkeys: The number of keys pressed in the previous frame
    # Invariant: _lastkeys is a int >= 0.
    #
    # Attribute _randStep: The number of steps between Alien shots
    # Invariant: _randStep is an int between 1 and BOLT_RATE
    #
    # Attribute _stepsSince: The number of steps since the last Alien shot
    # Invariant: _stepsSince is a int >= 0.
    #
    # Attribute _shipCol: The state of the ship's collisions
    # Invariant: _shipCol is a boolean.
    #
    # Attribute _contactLine: The state of the wave's collisions with _dline
    # Invariant: _contactLine is a boolean.
    #
    # Attribute _waveEmpty: The state of the wave's emptiness (or lack thereof)
    # Invariant: _waveEmpty is a boolean.

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """Returns the attribute _ship"""
        return self._ship

    def getLives(self):
        """Returns the attribute _lives"""
        return self._lives

    def getShipCol(self):
        """Returns the attribute _shipCol"""
        return self._shipCol

    def getWaveEmpty(self):
        """Returns the attribute _waveEmpty"""
        return self._waveEmpty

    def getContactLine(self):
        """Returns the attribute _contactLine"""
        return self._contactLine

    def setAliens(self):
        """
        Sets the _aliens attribute.

        Creates ALIEN_ROWS * ALIENS_IN_ROW Alien objects and puts them all
        into the attribute _aliens, a rectangular 2D list.
        """
        self._aliens = []

        for alien in range(ALIEN_ROWS):
            tempAlien = []
            for alienrow in range(ALIENS_IN_ROW):
                hpos = ALIEN_H_SEP + (alienrow*ALIEN_H_SEP)
                vpos = GAME_HEIGHT-(ALIEN_CEILING + (alien*ALIEN_V_SEP))
                if alien % 6 == 5 or alien % 6 == 0:
                    tempAlien.append(Alien(source='alien3.png',x=hpos,y=vpos))
                if alien % 6 == 1 or alien % 6 == 2:
                    tempAlien.append(Alien(source='alien2.png',x=hpos,y=vpos))
                if alien % 6 == 3 or alien % 6 == 4:
                    tempAlien.append(Alien(source='alien1.png',x=hpos,y=vpos))
            self._aliens.append(tempAlien)

    def setShip(self):
        """
        Creates the ship for the game.

        Sets the _ship attribute equal to a new Ship object.
        """
        self._ship = Ship()

    def setDline(self):
        """
        Creates the defense line for the game.

        Sets the _dline attribute equal to a new GPath object.
        """
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
        linewidth=2,linecolor='black')

    def setBolts(self):
        """Initializes the _bolts attribute by creating a new empty 1D list."""
        self._bolts = []

    def setLives(self):
        """Sets the attribute _lives equal to the lives left
        for the player, initially at 3"""
        self._lives = 3

    def setTime(self):
        """Sets the amount of time since the last Alien step, initially 0"""
        self._time = 0

    def setInitialDirection(self):
        """Sets the initial direction of the aliens when moving;
        +1 indicates movement to the right, -1 indicates movement to the left"""
        self._direction = 1

    def setLastKeys(self):
        """Sets the number of keys pressed in the previous frame, initially 0"""
        self._lastkeys = 0

    def setrandStep(self):
        """Sets the number of steps between alien shots by randomly choosing a
        number between 1 and BOLT_RATE using the randint method in the random class"""
        self._randStep = random.randint(1,BOLT_RATE)

    def setStepsSince(self):
        """Sets the number of steps since the last alien shot, initally at 0"""
        self._stepsSince = 0

    def setShipCol(self):
        """Sets the state of a ship collision; True if the ship has had a
        collision with a bolt, False if not, initially False"""
        self._shipCol = False

    def setWaveEmpty(self):
        """Sets the state of the wave; True if the wave is empty
        (all elements in the list are None), False if the wave is not empty
        (at least one of the elements in the list is are not None)"""
        self._waveEmpty = False

    def setContactLine(self):
        """Sets the state of the alien's contact with dline;
        True if the aliens have passed the line, False if not"""
        self._contactLine = False

        # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """The initializer for the Wave class."""
        self.setAliens()
        self.setShip()
        self.setDline()
        self.setBolts()
        self.setTime()
        self.setLives()
        self.setLastKeys()
        self.setInitialDirection()
        self.setrandStep()
        self.setStepsSince()
        self.setShipCol()
        self.setWaveEmpty()
        self.setContactLine()

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        The update method for the Wave class.

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._noAliens()
        self._touchLine()
        self._detShipCol()
        if not self._waveEmpty:
            self._detAlCol()
            self._moveWave(dt)
            if self._stepsSince == self._randStep:
                self._alienFire()
        if not self._shipCol:
            self._moveShip(input)
            self._boltKeyPress(input)
        else:
            self._coroutine(dt)
        self._moveBolt()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        The draw method for the Wave class.

        Parameter view: the game view, used in drawing
        Precondition: view is an instance of GView (inherited from GameApp)
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if self._aliens[i][j] is not None:
                    self._aliens[i][j].draw(view)
        if self._ship is not None:
            self._ship.draw(view)
        self._dline.draw(view)
        for x in range(len(self._bolts)):
            self._bolts[x].draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def _noAliens(self):
        """The helper method to detect if the wave is empty,
        if the wave is determined to be empty, the attribute _waveEmpty is
        set to True; if not, the attribute is set to False."""
        var = True
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if self._aliens[i][j] is not None:
                    var = False
        self._waveEmpty = var

    def _touchLine(self):
        """The helper method to detect when an alien touches the defense line,
        if the wave passes the defense line, the attribute _contactLine is set
        to True; if not, the attribute is set to False."""
        var = True
        run = True
        i = 0
        while i < ALIEN_ROWS and run:
            j = 0
            while j < ALIENS_IN_ROW and run:
                if self._aliens[ALIEN_ROWS-1-i][j] is not None:
                    y = self._aliens[ALIEN_ROWS-1-i][j].y - (ALIEN_HEIGHT/2)
                    if y <= DEFENSE_LINE:
                        var = False
                        run = False
                j += 1
            i += 1
        self._contactLine = not var

    def _coroutine(self, dt):
        """The helper method for animating collisions"""
        if self._ship is not None:
            if not self._ship._animator is None:
                if not self._ship._animator is None:
                    try:
                        self._ship._animator.send(dt)
                    except:
                        self._ship._animator = None
                        self._bolts.clear()
                        self._ship = None

            elif self._shipCol:
                self._ship._animator = self._ship._makeAnimator()
                next(self._ship._animator)

    def _detShipCol(self):
        """The helper method to check for collisions with the ship by looping
        through each element of the _bolts list and calling the Ship method collides().

        If a collision is detected, the attribute _shipCol is set to True, the
        number of lives is decremented by 1, and the bolt that is involved in the
        collision is removed from the screen and deleted from the _bolts list;
        if not, the attribute _shipCol stays False
        """
        i = 0
        run = True
        while i < len(self._bolts):
            if self._ship is not None and self._ship.collides(self._bolts[i]):
                self._shipCol = True
                self._lives -= 1
                del self._bolts[i]
                if len(self._bolts) == 0:
                    run = False
            i += 1

    def _detAlCol(self):
        """The helper method to check for collisions with the alien/wave by looping
        through each element of the _bolts list and _aliens list and calling the
        Alien method collides().

        If a collision is detected, the Alien element is set to None and the bolt
        involved in the collision is removed from the screen and deleted from
        the _bolts list.
        """
        i = 0
        run = True
        while i < len(self._bolts) and run:
            j = 0
            while j < ALIEN_ROWS and run:
                k = 0
                while k < ALIENS_IN_ROW and run:
                    try:
                        if self._aliens[ALIEN_ROWS-1-j][k] is not None and \
                        self._aliens[ALIEN_ROWS-1-j][k].collides(self._bolts[i]):
                            self._aliens[ALIEN_ROWS-1-j][k] = None
                            del self._bolts[i]
                            if len(self._bolts) == 0:
                                run = False
                        k += 1
                    except:
                        run = False
                j += 1
            i += 1

    def _moveShip(self,input):
        """The helper method to move the ship horizontally.

        If the 'left' key is pressed and there is still 'room' for the ship to
        move left, it will call the Ship method _shipLeft()
        If the 'right' key is pressed and there is still 'room' for the ship to
        move right, it will call the Ship method _shipRight()

        Parameter input: user input, used to control the ship or resume the game
        Precondtion: input is an instance of GInput (inherited from GameApp)
        """
        if input.is_key_down('left') and self._ship.x > SHIP_WIDTH/2:
            self._ship._shipLeft()
        if input.is_key_down('right') and self._ship.x < GAME_WIDTH-(SHIP_WIDTH/2):
            self._ship._shipRight()

    def _waveHorizontal(self):
        """The helper method to move the wave/aliens horizontally.

        If the element in _aliens is not None, it will call the Alien method
        _alienMove() and send self._direction as an argument, and reset the time
        attribute to 0 to indicate that an alien step has just occurred.
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if self._aliens[i][j] is not None:
                    self._aliens[i][j]._alienMove(self._direction)
                    self._time = 0

    def _waveVertical(self):
        """The helper method to move the wave/aliens vertically.

        If the element in _aliens is not None, it will call the Alien method
        _alienDown(), and reset the time attribute to 0 to indicate
        that an alien step has just occurred.
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if self._aliens[i][j] is not None:
                    self._aliens[i][j]._alienDown()
                    self._time = 0

    def _moveWave(self,dt):
        """The helper method to move the wave of aliens
        horizontally and vertically as needed"""
        if self._time > ALIEN_SPEED:
            self._waveHorizontal()
            self._stepsSince += 1
            for i in range(ALIEN_ROWS):
                for j in range(ALIENS_IN_ROW):
                    rowLeft = i
                    columnLeft = j
                    if self._aliens[rowLeft][columnLeft] is not None:
                        break
                else:
                    continue # Continue if the inner loop wasn't broken.
                break # Inner loop was broken, break the outer.
            for i in range(ALIEN_ROWS):
                for j in range(ALIENS_IN_ROW):
                    rowRight = i
                    columnRight = (ALIENS_IN_ROW-1)-j
                    if self._aliens[rowRight][columnRight] is not None:
                        break
                else:
                    continue
                break
            if self._aliens[rowRight][columnRight]._approachEdge(self._direction) \
            or self._aliens[rowLeft][columnLeft]._approachEdge(self._direction):
                self._waveVertical()
                self._direction *= -1
        self._time += dt

    def _moveBolt(self):
        """
        A helper method for bolt movement.

        This helper method moves all the bolts contained in the _bolts attribute
        across the screen, deleting them from the _bolts list when they have
        reached the top or bottom of the window
        """
        i = 0
        run = True
        while i < len(self._bolts) and run:
            self._bolts[i]._boltUp()
            if self._bolts[i].y > GAME_HEIGHT or self._bolts[i].y < 0:
                del self._bolts[i]
                if len(self._bolts) == 0:
                    run = False
            i += 1

    def _boltKeyPress(self,input):
        """
        Determines if there was a key press

        This method checks for a key press, and if there is one, creates a
        player bolt. A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.
        The user must release the key and press it again to change the state.

        Parameter input: user input, used to control the ship or resume the game
        Precondtion: input is an instance of GInput (inherited from GameApp)
        """
        # Determine the current number of keys pressed
        curr_keys = input.key_count
        # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self._lastkeys == 0 and input.is_key_down('spacebar')
        noPlayerBolts = True
        for x in range(len(self._bolts)):
            if(self._bolts[x]._isPlayerBolt()):
                noPlayerBolts = False
        if change and noPlayerBolts:
            self._bolts.append(Bolt(self._ship.x,self._ship.y+SHIP_HEIGHT/2,BOLT_SPEED))

            # Update last_keys
        self._lastkeys = curr_keys

    def _isEmptyCol(self,i):
        """"
        A helper method for checking columns in the _alien attribute.

        Returns True if the given column i of the list is full of None elements,
        False if any of the elements in the column are none.

        Parameter i: the specified column in _aliens to check
        Precondition: i is an int between 0 and ALIENS_IN_ROW-1
        """
        empty = True
        for x in range(ALIEN_ROWS):
            if self._aliens[x][i] is not None:
                empty = False
        return empty

    def _pickAlien(self):
        """
        A helper method to choose which alien should fire.

        The method chooses a random nonempty column in _aliens, and then finds
        the first element in the column, going from the bottom of the wave up,
        that is not None (and is an Alien object).
        """
        i = random.randint(0,ALIENS_IN_ROW-1)
        while self._isEmptyCol(i):
            i = random.randint(0,ALIENS_IN_ROW-1)
        bottom = True
        x = ALIEN_ROWS - 1
        while bottom:
            if self._aliens[x][i] is not None:
                return self._aliens[x][i]
            x -= 1

    def _alienFire(self):
        """
        A helper method to create an alien bolt.

        The method resets the attribute _stepsSince to 0, to indicate that an
        Alien shot has occurred, then calls the method _pickAlien() to choose an
        alien at random. Once the alien has been chosen, the method adds a new
        Bolt object to _bolts with the same position as the alien, and randomly
        chooses the number of steps until the next Alien shot.
        """
        self._stepsSince = 0
        alien = self._pickAlien()
        self._bolts.append(Bolt(alien.x,alien.y - ALIEN_HEIGHT/2,-BOLT_SPEED))
        self.setrandStep()
