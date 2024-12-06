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

# Jenny Yu
# December 7, 2021
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
    class will be similar to that one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
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
    # Invariant: _aliens is a rectangular 2d list contains Alien objects or None
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
    # Attribute _direction: the aliens' direction of movement
    # Invariant: _direction is a string with values in 'left', 'right' or 'down'
    #
    # Attribute _step: number of steps the aliens take since last bolt fired
    # Invariant: _step is an int between 0..BOLT_RATE
    #
    # Attribute _between: the number of steps aliens take between bolts fired
    # Invariant: _between is an int between 1..BOLT_RATE
    #
    # Attribute _shipfirefx: audio file played when ship fires bolt
    # Invariant: _shipfirefx is a Sound object
    #
    # Attribute _shipdestroyfx: audio file played when ship is destroyed
    # Invariant: _shipdestroyfx is a Sound object
    #
    # Attribute _alienfirefx: audio file played when alien fires bolt
    # Invariant: _alienfirefx is a Sound object
    #
    # Attribute _aliendestroyfx: audio file played when alien is destroyed
    # Invariant: _aliendestroyfx is a Sound object
    #
    # Attribute _shipanimator: coroutine for performing an animation
    # Invariant: _shipanimator is a generator-based coroutine or None
    #
    # Attribute _shipdestroy: whether ship is destroyed or not
    # Invariant: _shipdestroy is a Boolean
    #
    # Attribute _abelowdline: whether alien is below defense line or not
    # Invariant: _abelowdline is a Boolean
    #
    # Attribute _alienlives: number of aliens remaining
    # Invariant: _alienlives is an int >=0 and <= ALIEN_ROWS*ALIENS_IN_ROW
    #
    # Attribute _alienspeed: the alien speed
    # Invariant: _alienspeed is a float >0 and <= ALIEN_SPEED
    #
    # Attribute _alienscore: aliens' IDs and scores (ID is key, score is value)
    # Invariant: _alienscore is a dictionary w ALIEN_ROWS*ALIENS_IN_ROW elements
    #
    # Attribute _playerscore: player scores received based on aliens destroyed
    # Invariant: _playerscore is an int >=0

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setAlienWave(self):
        """
        Creates a new wave of Aliens only

        For every new wave created, increase alien speed by 0.1 second.
        """
        self._alienWave()
        self._alienspeed = max(0, round(self._alienspeed-0.1,1))

    def setShip(self):
        """
        Creates a new ship.
        """
        self._createShip()

    def getShipDestroy(self):
        """
        Returns whether ship is destroyed or not
        """
        return self._shipdestroy

    def getLives(self):
        """
        Returns player lives left
        """
        return self._lives

    def getABelowDLine(self):
        """
        Returns whether aliens crossed defense line or not
        """
        return self._abelowdline

    def getAlienLives(self):
        """
        Returns number of aliens remaining
        """
        return self._alienlives

    def getAlienSpeed(self):
        """
        Returns alien speed
        """
        return self._alienspeed

    def getPlayerScore(self):
        """
        Returns player score
        """
        return self._playerscore

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes a Wave object
        """
        self._alienWave()
        self._alienspeed = ALIEN_SPEED
        self._createShip()
        self._playerscore = 0
        self._createDLine()
        self._lives = SHIP_LIVES
        self._aliendestroyfx = Sound('pew1.wav')
        self._shipdestroyfx = Sound ('blast2.wav')
        self._shipfirefx = Sound ('pop1.wav')
        self._alienfirefx = Sound('pop2.wav')
        self._shipanimator = None
        self._shipdestroy = False
        self._abelowdline = False

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Moves the ship, aliens, and laser bolts.

        The organization of this method references the update method in
        state.py. The coroutine-related code (try...except) references the
        update method in the file coroutine.py provided in the sample code.

        Parameter input: the input
        Precnodition: input is an instance of GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(input,GInput)
        assert type(dt) == int or type(dt) == float
        if not self._shipanimator is None:       # We have something to animate
            try:
                self._shipanimator.send(dt)      # Tell it how far to animate
            except StopIteration:
                self._shipanimator = None
                self._ship = None
                self._shipdestroy = True
                self._lives -= 1
        else:
            self._moveShip(input)
            self._shipBolt(input)
        self._moveAliens(dt)
        self._alienBolt()
        self._checkShipCollision()
        self._checkAlienCollision()
        self._checkAlienBelowDLine()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the ship, aliens, defensive line and bolts to the view

        Parameter view: a reference to the game window
        Precondition: view is an instance of GView
        """
        assert isinstance(view,GView)
        self._drawAlien(view)
        self._drawShip(view)
        self._drawDLine(view)
        self._drawBolt(view)

    def _alienWave(self):
        """
        Creates a wave of aliens and assigns to _aliens attribute.

        This helper method fills a 2D list of Alien objects with ALIENS_ROWS
        rows of aliens and ALIENS_IN_ROW aliens in each row, spaced and sized
        based on the module's constants. In rows from bottom to top, images of
        aliens alternate in order after every two rows. After each image within
        the given selection (ALIEN_IMAGES) has been run through successively
        once, start over with using the first given image in the selection
        again.

        This method contains 27 lines of code.
        """
        self._aliens = []
        self._alienscore = {}
        # Set the starting x and y of the bottom row
        imagex=ALIEN_H_SEP + (ALIEN_WIDTH/2)
        imagey=(GAME_HEIGHT - (ALIEN_CEILING + (ALIEN_ROWS-1)*ALIEN_HEIGHT
                + (ALIEN_ROWS-1)*ALIEN_V_SEP + (ALIEN_HEIGHT/2)))
        rowAccumulator = 0
        imageIndex = 0
        for x in range(ALIEN_ROWS):
            current = []
            for y in range(ALIENS_IN_ROW):
                current.append(Alien(imagex, imagey, ALIEN_IMAGES[imageIndex]))
                # This step adds alien ID and score pair to the dictionary
                self._alienscore[id(current[-1])] = ALIEN_ROWS-x
                imagex = imagex + ALIEN_H_SEP + ALIEN_WIDTH
            self._aliens.append(current)
            #set new x and y for the next row
            imagex = ALIEN_H_SEP + (ALIEN_WIDTH/2)
            imagey = imagey + ALIEN_V_SEP + ALIEN_HEIGHT
            #reset rowAccumulator
            rowAccumulator = rowAccumulator+1
            if rowAccumulator == 2:
                rowAccumulator = 0
                imageIndex = imageIndex + 1
            #reset imgIndex to 0 if it is 3
            if imageIndex == 3: imageIndex = 0
        self._time = 0
        self._direction = 'right'
        self._bolts = []
        self._step = 0
        self._between = random.randint(1,BOLT_RATE)
        self._alienlives = ALIEN_ROWS*ALIENS_IN_ROW

    def _drawAlien(self,view):
        """
        Draws the aliens to the view.

        Parameter view: a reference to the game window
        Precondition: view is an instance of GView
        """
        assert isinstance(view,GView)
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.draw(view)

    def _createShip(self):
        """
        Creates ship and assigns to _ship attribute.
        """
        imagex = (GAME_WIDTH/2)
        imagey = (SHIP_HEIGHT/2)+SHIP_BOTTOM
        self._ship = Ship(imagex,imagey,'ship-strip.png',(2,4))
        self._shipdestroy = False

    def _drawShip(self,view):
        """
        Draws the ship to the view.

        Parameter view: a reference to the game window
        Precondition: view is an instance of GView
        """
        assert isinstance(view,GView)
        if self._ship is not None:
            self._ship.draw(view)

    def _createDLine(self):
        """
        Creates defense line and assigns to _dline attribute.

        The defense line is an instance of the GPath object.
        """
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                      linewidth=2,linecolor = 'blue')

    def _drawDLine(self,view):
        """
        Draws the defense line to the view.

        Parameter view: a reference to the game window
        Precondition: view is an instance of GView
        """
        assert isinstance(view,GView)
        if self._dline is not None:
            self._dline.draw(view)

    def _moveShip(self,input):
        """
        Moves the ship left or right based on user key press.

        The ship stays completely on the board even if the player continues
        to hold down a key. The code for checking left or right key press and
        moving ship accordingly references the update method in arrows.py file
        provided in the sample code.

        Parameter input: the input
        Precnodition: input is an instance of GInput
        """
        assert isinstance(input,GInput)
        if self._ship is not None:
            if input.is_key_down('left'):
                self._ship.moveShip('left')
            if input.is_key_down('right'):
                self._ship.moveShip('right')

    def _moveAliens(self,dt):
        """
        Moves aliens back and forth on the game board

        When aliens move horizontally, they move the same amount: ALIEN_H_WALK.
        When aliens move vertically, they move the same amount: ALIEN_V_WALK.

        If the current direction is "right", aliens move towards the right edge
        of the game board. If the next step will cause the rightmost alien(s) to
        go off board, then aliens will walk down ALIEN_V_WALK. Then the
        direction will be set to "left".

        If the current direction is "right", aliens move towards the left edge
        of the game screen. If the next step will cause the leftmost alien(s) to
        go off-screen, then aliens will walk down ALIEN_V_WALK. Then the
        direction will be set to "right".

        Aliens do not move every animation frame. The method keeps track of the
        number of seconds passed, and only moves the aliens when the accumulated
        time is greater than ALIEN_SPEED.

        This method contains 25 lines of code.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float
        if self._time < self._alienspeed:
            self._time = self._time + dt
        else:
            self._time = 0
            self._step = self._step+1
            # If current direction is "right",
            # check the position of the rightmost alien,
            # If next step is off right edge, set direction to "down-left"
            # else, keep moving right
            if self._direction == 'right':
                rightmostX = self._rightmostAlien()
                if rightmostX + ALIEN_H_SEP > (GAME_WIDTH - ALIEN_H_SEP -
                                               (ALIEN_WIDTH/2)):
                    self._direction = 'down-left'
                else:
                    self._alienWalk('right')
            # If current direction is "left"
            # check the position of the leftmost alien
            # If next step is off left edge, set direction to "down-right"
            # else, keep moving left
            if self._direction == 'left':
                leftmostX = self._leftmostAlien()
                if leftmostX - ALIEN_H_SEP < ALIEN_H_SEP + (ALIEN_WIDTH/2):
                    self._direction = 'down-right'
                else:
                    self._alienWalk('left')
            if self._direction == 'down-left':
                self._alienWalk('down')
                self._direction = 'left'
            if self._direction == 'down-right':
                self._alienWalk('down')
                self._direction = 'right'

    def _alienWalk(self, direction):
        """
        Move aliens ONE STEP to "left", "right" or "down" based on direction

        Parameter direction: the aliens' direction of movement
        Precondition: direction is string w values in 'left','right' or 'down'
        """
        assert type(direction) == str
        assert direction in ['left','right','down']
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] is not None:
                    if direction == 'left':
                        self._aliens[row][col].x = (self._aliens[row][col].x -
                                                    ALIEN_H_WALK)
                    elif direction == 'right':
                        self._aliens[row][col].x = (self._aliens[row][col].x +
                                                    ALIEN_H_WALK)
                    elif direction == 'down':
                        self._aliens[row][col].y = (self._aliens[row][col].y -
                                                    ALIEN_V_WALK)

    def _shipBolt(self,input):
        """
        Creates bolt and appends to _bolts attribute; fires bolt.

        Bolt is created with BOLT_SPEED velocity and appended to the _bolt list
        if ship is not None and user key input is 'up'. The bolt is only
        created and fired when there is no player bolt on the screen. That way,
        the player may only have one laser bolt on the screen at a time. The
        bolt is deleted from the _bolt list when it goes off screen. This
        method plays the audio when the bolt is fired.

        Parameter input: the input
        Precnodition: input is an instance of GInput
        """
        assert isinstance(input,GInput)
        if self._ship is not None:
            if input.is_key_down('up'):
                numSBolt = 0
                #Check if there is a bolt on the screen
                for x in self._bolts:
                    if x.isPlayerBolt() == True:
                        numSBolt += 1
                #Only create a new bolt when there is no bolt on screen
                if numSBolt == 0:
                    boltx = self._ship.x
                    bolty = self._ship.y+(SHIP_HEIGHT/2)+(BOLT_HEIGHT/2)
                    self._bolts.append(Bolt(boltx,bolty,1,'red','gray'))
                    self._shipfirefx.play()    # Plays audio
            self._fireBolt(True)

    def _drawBolt(self,view):
        """
        Draws bolt to the view.

        Parameter view: a reference to the game window
        Precondition: view is an instance of GView
        """
        assert isinstance(view,GView)
        for x in self._bolts:
            if x is not None:
                x.draw(view)

    def _alienBolt(self):
        """
        Creates alien bolt and appends to _bolts attribute; fires bolt.

        Aliens do not fire every step. It takes aliens up to BOLT_RATE steps
        to fire a bolt. The number of steps between bolts is a random number
        between 1 and BOLT_RATE. The alien that fires a bolt is a randomly
        selected bottom-most alien from a non-empty column. Once the timing and
        the alien is picked, a bolt is created with -BOLT_SPEED velocity and
        appended to the _bolt list. This method plays audio when the bolt is
        fired. This method contains 20 lines of code.
        """
        #only fire bolt when aliens make self._between steps
        if self._step == self._between:
            #find random alien column
            aliencols = self._alienNonEmptyCols()
            randcol = random.choice(aliencols)
            #find alien on bottom of random column
            bottomAlien = 0
            for x in range(ALIEN_ROWS):
                if self._aliens[x][randcol] is not None:
                    bottomAlien = x
                    break
            #calculate bolt x and y for bottom-most alien
            bx = self._aliens[bottomAlien][randcol].x
            by = (self._aliens[bottomAlien][randcol].y-(ALIEN_HEIGHT/2)-
                  (BOLT_HEIGHT/2))
            #create alien bolt
            numABolt = 0
            self._bolts.append(Bolt(bx,by,-1,'blue','gray'))
            self._alienfirefx.play() # Plays audio
            self._between = random.randint(1,BOLT_RATE)
            self._step = 0
        elif self._step>self._between:
            self._between = random.randint(1,BOLT_RATE)
            self._step = 0
        self._fireBolt(False)

    def _fireBolt(self,isPlayerBolt):
        """
        Helper method fires the player bolt or alien bolt

        Parameter isPlayerBolt: whether bolt is fired by player or alien
        Precondition: isPlayerBolt is a boolean
        """
        assert type(isPlayerBolt) == bool
        if isPlayerBolt == True:
            for x in self._bolts:
                if x.isPlayerBolt():
                    x.y = x.y+x.getVelocity()
                    if (x.y-(BOLT_HEIGHT/2))>GAME_HEIGHT:
                        self._bolts.remove(x)
        else:
            for x in self._bolts:
                if x.isPlayerBolt()==False:
                    x.y = x.y+x.getVelocity()
                    if (x.y-(BOLT_HEIGHT/2))<0:
                        self._bolts.remove(x)

    # HELPER METHOD TO FIND NON-EMPTY ALEN COLUMN
    def _alienNonEmptyCols(self):
        """
        Helper method returns a list of non-empty alien column indices
        """
        list = []
        for y in range(ALIENS_IN_ROW):
            sum = 0
            for x in range(ALIEN_ROWS):
                if self._aliens[x][y] is None:
                    sum += 1
            if sum < ALIEN_ROWS:
                list.append(y)
        return list

    # HELPER METHOD TO FIND LEFT-MOST ALIEN X COORDINATE
    def _leftmostAlien(self):
        """
        Helper method returns the x coordinate of the leftmost alien.
        """
        aliencol = self._alienNonEmptyCols()
        for x in range(ALIEN_ROWS):
            if self._aliens[x][aliencol[0]] is not None:
                return self._aliens[x][aliencol[0]].x

    # HELPER METHOD TO FIND RIGHT-MOST ALIEN X COORDINATE
    def _rightmostAlien(self):
        """
        Helper method returns the x coordinate of the rightmost alien.
        """
        aliencol = self._alienNonEmptyCols()
        for x in range(ALIEN_ROWS):
            if self._aliens[x][aliencol[-1]] is not None:
                return self._aliens[x][aliencol[-1]].x

    # HELPER METHODS FOR COLLISION DETECTION
    def _checkShipCollision(self):
        """
        A procedure that checks if ship has collided with alien bolt.

        If the ship has collided with the alien bolt, the audio sound plays,
        and the alien bolt is removed. The ship explodes through animation
        (coroutine).
        """
        if self._ship is not None:
            for x in self._bolts:
                if x.isPlayerBolt()==False:
                    if self._ship.collides(x) == True:
                        self._shipdestroyfx.play()
                        self._bolts.remove(x)
                        self._shipanimator = self._ship.animator()
                        next(self._shipanimator)

    def _checkAlienCollision(self):
        """
        A procedure that checks if alien has collided with player bolt.

        If the alien has collided with the player bolt, the audio sound plays,
        and the player bolt is removed. That alien instance is set to None.
        """
        for x in range(ALIEN_ROWS):
            for y in range(ALIENS_IN_ROW):
                if self._aliens[x][y] is not None:
                    for z in self._bolts:
                        if self._aliens[x][y].collides(z) == True:
                            self._aliendestroyfx.play()
                            alienid = id(self._aliens[x][y])
                            self._playerscore += self._alienscore.get(alienid)
                            self._alienlives = self._alienlives-1
                            self._aliens[x][y] = None
                            self._bolts.remove(z)

    # HELPER METHOD TO DETECT ALIENS CROSSED DEFENSE LINE
    def _checkAlienBelowDLine(self):
        """
        A procedure that checks whether aliens have crossed the defense line.

        When the bottom-most alien(s) goes below the dline, this procedure sets
        _abelowdline to True; otherwise it sets _abelowdline to False.
        """
        alienlowest = GAME_HEIGHT
        for x in range(ALIEN_ROWS):
            for y in range(ALIENS_IN_ROW):
                if self._aliens[x][y] is not None:
                    if self._aliens[x][y].y<alienlowest:
                        alienlowest = self._aliens[x][y].y
        if (alienlowest-(ALIEN_HEIGHT/2))<DEFENSE_LINE:
            self._abelowdline = True
        else:
            self._abelowdline = False
