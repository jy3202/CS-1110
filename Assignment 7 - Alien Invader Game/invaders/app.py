"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# Jenny Yu
# December 7, 2021
"""
from consts import *
from game2d import *
from wave import *

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/
# setters
# Invaders is NOT allowed to access anything in models.py


class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game. This code references the start method in
        subcontroller.py.
        """
        # IMPLEMENT ME
        self._state = STATE_INACTIVE
        self._text = GLabel(text='Press "S" to Play',font_size=24,
                            font_name='RetroGame', x=GAME_WIDTH/2,
                            y=GAME_HEIGHT/2)
        self._wave = None

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        assert type(dt) == int or type(dt) == float
        # Determine the current state
        self._determineState()
        # Process the states.  Send to helper methods
        if self._state == STATE_INACTIVE:
            self._STATE_INACTIVE_Helper()
        elif self._state == STATE_NEWWAVE:
            self._STATE_NEWWAVE_Helper()
        elif self._state == STATE_ACTIVE:
            self._STATE_ACTIVE_Helper(dt)
        elif self._state == STATE_PAUSED:
            self._STATE_PAUSED_Helper()
        elif self._state == STATE_CONTINUE:
            self._STATE_CONTINUE_Helper()
        elif self._state == STATE_COMPLETE:
            self._STATE_COMPLETE_Helper()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        # IMPLEMENT ME
        if self._text is not None:
            self._text.draw(self.view)
        if self._wave is not None:
            self._wave.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _determineState(self):
        """
        Helper method that determines current state, assigns it to self._state

        This method checks for a key press, and if there is
        one, changes the state accordingly based on whether the game is
        inactive, paused, or complete (won or lost). A key press is when a key
        is pressed for the first time. The state should not continue to change
        as we hold down the key. The user must release the key and press it
        again to change the state. The code for key press references the
        _determineState method in state.py.
        If there is no key press the function also checks the status of the
        ship, aliens, and whether the alien has crossed the defense line,
        and sets the state accordingly based on whether the game is paused or
        complete (won or lost).
        """
        # Determine the current number of keys pressed
        curr_keys = self.input.key_count
        # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self.lastkeys == 0
        if change: # with key press
            # Previous state is inactive, new wave(game)
            if self.input.is_key_down('s') and self._state == STATE_INACTIVE:
                self._state = STATE_NEWWAVE
            # Previous state is paused, continue
            elif self.input.is_key_down('s') and self._state == STATE_PAUSED:
                self._state = STATE_CONTINUE
            # Previous state is complete, create a new wave, active
            # _STATE_COMPLETE_Helper checks won/lost condition, and the Only
            # scenario the state is STATE_COMPLETE is when all aliens are
            # destroyed and player still has lives left. Therefore, a key
            # press of 'S' will allow a new wave to be created.
            elif self.input.is_key_down('s') and self._state == STATE_COMPLETE:
                self._wave.setAlienWave()
                self._state = STATE_ACTIVE
                pass
        else: # without key press
            # Ship destroyed but still has live(s), pause game
            if (self._wave is not None and self._wave.getShipDestroy() == True
                and self._wave.getLives() > 0):
                self._state = STATE_PAUSED
            # Ship destroyed but has no life left, game complete
            elif (self._wave is not None and self._wave.getShipDestroy()==True
                  and self._wave.getLives()==0):
                self._state = STATE_COMPLETE
            # Alien(s) crossed defense line, game complete
            elif (self._wave is not None and self._wave.getABelowDLine()==True):
                self._state = STATE_COMPLETE
            # Alien(s) all destroyed, game complete
            elif self._wave is not None and self._wave.getAlienLives()==0:
                self._state = STATE_COMPLETE
        # Update last_keys
        self.lastkeys= curr_keys

    def _STATE_INACTIVE_Helper(self):
        """
        Assigns attributes for before game start and alien wave has not started.

        This is the state when the application first opens, as well as the
        state the application returns to when the game is over. It displays a
        simple message on the screen prompting the user to press a key to
        continue. This code references the start method in subcontroller.py.
        """
        self._text = GLabel(text='Press "S" to Play',font_size=24,
                            font_name='RetroGame', x=GAME_WIDTH/2,
                            y=GAME_HEIGHT/2)
        self._wave = None

    def _STATE_NEWWAVE_Helper(self):
        """
        Assigns attributes for when aliens are set up but not yet moving.

        This is the state that creates a new wave and shows it on
        the screen. This state only lasts one animation frame before switching
        to STATE_ACTIVE.
        """
        self._text = None
        self._wave = Wave()
        self._state = STATE_ACTIVE

    def _STATE_ACTIVE_Helper(self,dt):
        """
        Assigns attributes for when aliens are set up and have begun moving.

        This is the state that is a session of normal gameplay.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float
        self._text = None
        self._wave.update(self.input,dt)
        label = 'Player Lives(s): '+str(self._wave.getLives())
        label = label +'    '+'Player Score: '+str(self._wave.getPlayerScore())
        label = label +'    '+'Alien Speed: '+str(self._wave.getAlienSpeed())
        self._text = GLabel(text=label,font_size=18,font_name='RetroGame',
                            x=GAME_WIDTH/2,y=GAME_HEIGHT-(ALIEN_CEILING/2)
                            ,linecolor = 'blue')

    def _STATE_PAUSED_Helper(self):
        """
        Assigns attributes for game pause.

        This is a paused state when the player still has lives left after ship
        has been destroyed. Invaders displays a message that the player
        press ‘S’ to continue.
        """
        self._text = GLabel(text='Game Paused. \nPress "S" to Continue',
                            font_size=24,font_name='RetroGame', x=GAME_WIDTH/2,
                            y=GAME_HEIGHT-(ALIEN_CEILING/2))

    def _STATE_CONTINUE_Helper(self):
        """
        Assigns attributes for when game continues after the paused state.

        This state restores the ship after it was destroyed and the player still
        has lives remaining. The application switches to this state if the
        state was STATE_PAUSED in the previous frame, and the player pressed
        the 's' key.
        """
        self._text = None
        self._wave.setShip()
        self._state = STATE_ACTIVE

    def _STATE_COMPLETE_Helper(self):
        """
        Assigns attributes for when wave is over.

        The state is set as STATE_COMPLETE when 1 of 3 conditions are met:
        1. Player has lost all lives,
        2. aliens have crossed the defense line,
        3. all aliens have been destroyed.
        A message is displayed to inform the player that the game is over in
        cases 1 and 2 when player has lost, and to congratulate the player in
        case 3 when player has won.
        """
        if (self._wave is not None and self._wave.getShipDestroy() == True and
            self._wave.getLives()==0):
            label = 'Game over! You lost all lives.'
            label = label + '\nPress "S" to Start a Brand New Game.'
            self._text = GLabel(text=label,font_size=20,font_name='RetroGame',
                               x=GAME_WIDTH/2,y=GAME_HEIGHT-(ALIEN_CEILING/2),
                               linecolor = 'red')
            self._state = STATE_INACTIVE
        elif (self._wave is not None and self._wave.getABelowDLine()==True):
            label = 'Game over! The Aliens Crossed the Defense Line.'
            label = label + '\nPress "S" to Start a Brand New Game.'
            self._text = GLabel(text=label,font_size=20,font_name='RetroGame',
                               x=GAME_WIDTH/2,y=GAME_HEIGHT-(ALIEN_CEILING/2),
                               linecolor = 'red')
            self._state = STATE_INACTIVE
        elif self._wave is not None and self._wave.getAlienLives()==0:
            label = 'Congratulations! You won the game.'
            label = label + '\nPress "S" to start a NEW WAVE with faster speed.'
            self._text = GLabel(text=label,font_size=20,font_name='RetroGame',
                               x=GAME_WIDTH/2,y=GAME_HEIGHT-(ALIEN_CEILING/2),
                               linecolor = 'green')
