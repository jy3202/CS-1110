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

# Jenny Yu
# December 7, 2021
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

    The constructor for the ship references the online documentation for
    GSprite.
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    #Attribute _shipAnimatorTime: time passed so far in the coroutine
    #Invariant: _shipAnimatorTime is a float >= 0

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,imagex,imagey,imagesource,stripformat):
        """
        Initializes ship dimensions.

        Ship width and height are referenced in consts.py

        Parameter imagex: the x position of the image
        Precondition: imagex is an float

        Parameter imagey: the y position of the image
        Precondition: imagey is an float

        Parameter imagesource: the file name of the image
        Precondition: imagesource is a string
        """
        assert type(imagex) == float
        assert type(imagey) == float
        assert type(imagesource) == str
        super().__init__(x=imagex,y=imagey,width=SHIP_WIDTH,height=SHIP_HEIGHT,
                         source=imagesource,format=stripformat,frame=0)
        self._shipAnimatorTime = 0

    # METHODS TO MOVE THE SHIP
    def moveShip(self,direction):
        """
        Moves the ship left or right SHIP_MOVEMENT based on direction.

        The ship stays completely on the game board.

        Parameter direction: direction to move left or right
        Precnodition: direction is a string of values "left" or "right
        """
        assert type(direction) == str
        assert direction == 'left' or direction == 'right'
        if direction == 'left':
            self.x = max(self.x-SHIP_MOVEMENT,0+(SHIP_WIDTH/2))
        elif direction == 'right':
            self.x = min(self.x+SHIP_MOVEMENT,GAME_WIDTH-(SHIP_WIDTH/2))

    # METHOD TO cHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns True if ship collides with bolt

        This method returns False if bolt was fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt, Bolt)
        #if bolt was fired by the player, return False
        if bolt.isPlayerBolt():
            return False
        #upper left corner
        ulx = bolt.x-(BOLT_WIDTH/2)
        uly = bolt.y+(BOLT_HEIGHT/2)
        #upper right corner
        urx = bolt.x+(BOLT_WIDTH/2)
        ury = bolt.y+(BOLT_HEIGHT/2)
        #bottom left corner
        blx = bolt.x-(BOLT_WIDTH/2)
        bly = bolt.y-(BOLT_HEIGHT/2)
        #bottom right corner
        brx = bolt.x+(BOLT_WIDTH/2)
        bry = bolt.y-(BOLT_HEIGHT/2)
        #if one of the 4 bolt corners is contained in the ship, return True
        if (self.contains((ulx,uly)) or self.contains((urx,ury)) or
            self.contains((blx,bly)) or self.contains((brx,bry))):
            return True
        else:
            return False

    # COROUTINE METHOD TO ANIMATE THE SHIP
    def animator(self):
        """
        Animates frames of image over DEATH_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it.

        The code references the _animate_slide method in the file coroutine.py
        provided in the sample code.
        """
        animating = True
        while animating:
            # Get the current time
            dt = (yield)
            self._shipAnimatorTime += dt
            currentFrame = round((self._shipAnimatorTime/DEATH_SPEED)*7)
            # If we go beyond 7 frames, stop animating
            if currentFrame <= 7:
                self.frame = currentFrame
            else:
                animating = False
                self._shipAnimator = 0

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

    The constructor for the bolt references the online documentation for
    GImage.
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,imagex,imagey,imagesource):
        """
        Initializes alien dimensions.

        These dimensions are all specified in consts.py. The format of the
        constructor references the online documentation for GImage.

        Parameter imagex: the x position of the image
        Precondition: imagex is an float

        Parameter imagey: the y position of the image
        Precondition: imagey is an float

        Parameter imagesource: the source of the image
        Precondition: imagesource is a string
        """
        assert type(imagex) == float
        assert type(imagey) == float
        assert type(imagesource) == str
        super().__init__(x=imagex,y=imagey,width=ALIEN_WIDTH,
                         height=ALIEN_HEIGHT,source=imagesource)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if alien collides with bolt

        This method returns False if bolt was not fired by the player.

        The contains function references gobj.contains((x,y)) method in GObject
        object.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt, Bolt)
        #if bolt was NOT fired by the player, return False
        if bolt.isPlayerBolt()==False:
            return False
        #upper left corner
        ulx = bolt.x-(BOLT_WIDTH/2)
        uly = bolt.y+(BOLT_HEIGHT/2)
        #upper right corner
        urx = bolt.x+(BOLT_WIDTH/2)
        ury = bolt.y+(BOLT_HEIGHT/2)
        #bottom left corner
        blx = bolt.x-(BOLT_WIDTH/2)
        bly = bolt.y-(BOLT_HEIGHT/2)
        #bottom right corner
        brx = bolt.x+(BOLT_WIDTH/2)
        bry = bolt.y-(BOLT_HEIGHT/2)
        #if one of the 4 bolt corners is contained in the alien, return True
        if (self.contains((ulx,uly)) or self.contains((urx,ury)) or
            self.contains((blx,bly)) or self.contains((brx,bry))):
            return True
        else:
            return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


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
    from GRectangle as a helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.

    The constructor for the bolt references the online documentation for
    GRectangle.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Returns velocity of bolt.
        """
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,boltx,bolty,vdirect,bfillcolor,blinecolor):
        """
        Initializes bolt dimensions.

        These dimensions are all specified in consts.py

        Parameter boltx: the x position of the bolt
        Precondition: boltx is an float

        Parameter bolty: the y position of the bolt
        Precondition: bolty is an float

        Parameter vdirect: the direction of the bolt
        Precondition: vdirect is an int of -1 or 1

        Parameter bfillcolor: the fill color of the bolt
        Precondition: bfillcolor is a string

        Parameter blinecolor: the line color of the bolt
        Precondition: blinecolor is a string
        """
        assert type(boltx) == float
        assert type(bolty) == float
        assert type(vdirect) == int and (vdirect == 1 or vdirect == -1)
        assert type(bfillcolor) == str
        assert type(blinecolor) == str
        #set the starting velocity
        self._velocity = BOLT_SPEED*vdirect
        super().__init__(x=boltx,y=bolty,width=BOLT_WIDTH,height=BOLT_HEIGHT,
                         fillcolor=bfillcolor,linecolor=blinecolor)

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Returns True if player is firing bolt, False otherwise.
        """
        if self._velocity>0:
            return True
        else:
            return False


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
