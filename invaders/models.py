"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Khushi Patel (ksp67)
# December 9, 2021
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine (or None)
    #
    # Attribute frame: Tracks which frame in the sprite sheet is displayed
    # Invariant: frame is an int >= 0
    #
    # Attribute time: Tracks the total time passed
    # Invariant: time is a number >= 0

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setFrame(self):
        """The setter for the frame for the Ship"""
        self.frame = 0

    def setAnimator(self):
        """The setter for the animator for the Ship"""
        self._animator = None

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        The initializer for the Ship class
        """
        super().__init__(source='ship-strip.png',format=(2,4),
        width=SHIP_WIDTH,height=SHIP_HEIGHT,x=GAME_WIDTH/2,y=SHIP_BOTTOM)
        self.setFrame()
        self.setAnimator()

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        The method to check for a collision between an Alien bolt and the Ship.

        The metho checks all four corners of the bolt.
        Returns True if the alien bolt collides with the ship. Returns False if the
        bolt was not fired by an alien or there is no collision.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        i = [[-1,-1],[-1,1],[1,-1],[1,1]]
        collide = False
        k = 0
        while k < 4 and not collide:
            x = bolt.x + (i[k][0] * (BOLT_WIDTH/2))
            y = bolt.y + (i[k][1] * (BOLT_WIDTH/2))
            if self.contains((x,y)) and not bolt._isPlayerBolt():
                collide = True
            k += 1
        return collide

    def _shipLeft(self):
        """
        The helper method to move the ship to the left.
        """
        self.x -= SHIP_MOVEMENT

    def _shipRight(self):
        """
        The helper method to move the ship to the right.
        """
        self.x += SHIP_MOVEMENT

    # COROUTINE METHOD TO ANIMATE THE SHIP
    def _makeAnimator(self):
        """
        Animates the ship over DEATH_SPEED seconds.

        This method is a coroutine that takes the dt as periodic input so
        it knows how many (parts of) seconds to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        time = 0
        while time < DEATH_SPEED:
            dt = (yield)
            percentDone = time / DEATH_SPEED
            floatFrame = percentDone * 7
            self.frame = int(floatFrame)
            time += dt

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, source):
        """
        The initializer for the Alien class
        """
        super().__init__(x=x,y=y,source=source,height=ALIEN_HEIGHT,width=ALIEN_WIDTH)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        The method to check for a collision between an Player bolt and the Alien.

        The metho checks all four corners of the bolt.
        Returns True if the player bolt collides with the alien. Returns False if the
        bolt was not fired by an player or there is no collision.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        i = [[-1,-1],[-1,1],[1,-1],[1,1]]
        collide = False
        k = 0
        while k < 4 and not collide:
            x = bolt.x + (i[k][0] * (BOLT_WIDTH/2))
            y = bolt.y + (i[k][1] * (BOLT_WIDTH/2))
            if self.contains((x,y)) and bolt._isPlayerBolt():
                collide = True
            k += 1
        return collide

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def _alienMove(self,direction):
        """
        The helper method to move the aliens horizontally.

        Parameter direction: The direction to move the aliens
        Precondition: direction is either -1 or 1.
        """
        self.x += (ALIEN_H_WALK * direction)

    def _alienDown(self):
        """
        The helper method to move aliens down.
        """
        self.y -= ALIEN_V_WALK

    def _approachEdge(self, direction):
        """
        The helper method to check if the wave is close to the edge of the window.

        Returns True if the wave is close to the leftmost or rightmost edge,
        False if not.

        Parameter direction: The direction to move the aliens
        Precondition: direction is either -1 or 1.
        """
        if ((GAME_WIDTH - ALIEN_H_SEP) <= self.x) and direction == 1:
            return True
        if (ALIEN_H_SEP >= self.x) and direction == -1:
            return True
        return False


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """Returns the velocity attribute"""
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,X,Y,speed):
        """The initalizer for the Bolt Class"""
        self._velocity = speed
        super().__init__(x=X,y=Y,width=BOLT_WIDTH,height=BOLT_HEIGHT,
        fillcolor="black",linecolor="black")

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def _boltUp(self):
        """
        The helper method to move the y position of the bolts up.
        """
        self.y += self._velocity

    def _isPlayerBolt(self):
        """
        Checks the type of the Bolt object

        Returns True if the Bolt object given is a player Bolt,
        False if the Bolt object is an Alien Bolt
        """
        if(self.getVelocity() > 0):
            return True
        else:
            return False

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
