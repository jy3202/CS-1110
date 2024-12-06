OVERVIEW:
This is the final project of Cornell University's CS1110 Fall 2021 course. It involves developing an Alien Invaders game in Python. This project integrates concepts taught throughout the semester, such as basic object-oriented programming and graphics. The game includes core features like player movement, shooting, and alien behavior. Additionally, students are encouraged to extend the functionality with extra features such as sound, animations, and additional levels. By incrementally programming and testing, students can successfully complete the project while preparing for more complex coding challenges.

ASSIGNMENT URL: 
https://www.cs.cornell.edu/courses/cs1110/2021fa/assignments/a7/

BASIC FEATURES:
app.py: 
This module contains the main controller class for the Alien Invaders app.

const.py:
This module contains global constants for the game Alien Invaders. These constants are
used in the model, the view, and the controller. 

models.py
This module contains the model classes for the Alien Invaders game. 

wave.py
This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game. 

ADDITIONAL FEATURES:
Feature 1: Multiple Waves
If the player destroyed all aliens without losing all the lives, the screen
displays a message saying "Congratulations! You have won the game. Press 's'
to Start a New Wave of Aliens." When the player presses 's', a new wave of
aliens begins, and the alien speed is increased by 0.1 second for each new wave
(speed value is reduced by 0.1). This does not start a new game, therefore
player lives and player score will carry over from the previous wave.

Implementation details:
In Wave.py, I created a new attribute _alienspeed to hold alien speed. It is
initialized to ALIEN_SPEED in the __init__ method. I then created a setter
setAlienWave(self). In the setter, I called the private _alienWave() method I
created previously for creating the alien wave, and I added one line of code
self._alienspeed = self._alienspeed-0.1 to increase the alien speed for the
new wave.

In app.py, in the _STATE_COMPLETE_Helper method, I checked if all aliens have been
destroyed and player still has live(s) left. If yes, I created a GLabel to
display the message "Congratulations! You have won the game. Press 's' to Start
a New Wave of Aliens." Then I kept the _state as STATE_COMPLETE.

In app.py, in the _determineState method, I checked if the user key press is 's'
when the _state is STATE_COMPLETE, I called the self._wave.setAlienWave() method to
create the new wave, and then set the _state to STATE_ACTIVE to play the game
again.


Feature 2: Sound Effects
When the alien is destroyed, it plays the 'pew1.wav' audio file.
When the ship is destroyed, it plays the 'blast2.wav' audio file.
When the ship fires a bolt, it plays the 'pop1.wav' audio file.
When the alien fires a bolt, it plays the 'pop2.wav' audio file.

Implementation details:
In Wave.py, I created 4 hidden attributes to store the audio files:
_aliendestroyfx: Sound object stores audio file when alien is destroyed
_shipdestroyfx: Sound object stores audio file when ship is destroyed
_shipfirefx: Sound object stores audio file when ship fires
_alienfirefx: Sound object stores audio file when alien fires

In Wave.py, in the __init__ method, I imported the 4 audio files:
self._aliendestroyfx = Sound('pew1.wav')
self._shipdestroyfx = Sound ('blast2.wav')
self._shipfirefx = Sound ('pop1.wav')
self._alienfirefx = Sound('pop2.wav')

In Wave.py, within the _checkAlienCollision method when the alien collides
with the player bolt the sound is played: self._aliendestroyfx.play()
In Wave.py, within the _checkShipCollision method when the ship collides with
the alien bolt the sound is played: self._shipdestroyfx.play()
In Wave.py, within the _shipBolt method when the ship fires the bolt the
sound is played: self._shipfirefx.play()
In Wave.py, within the _alienBolt method when the alien fires the bolt the
sound is played: self._alienfirefx.play()


Feature 3: Player Score
During the game play, a GLabel is being displayed above the aliens to show:
Player Lives(s):     Player Score:    Alien Speed:
When an alien is destroyed, the player score will be increased by adding the
destroyed alien's score. And the GLabel will reflect the new score.

Implementation details:
In Wave.py, I created a new hidden attribute _alienscore. It is a dictionary
that stores the ID of each alien and its corresponding score. The aliens in
the bottom row are worth higher points, whereas the aliens in the top row are
worth lower points. For example, for a 3x3 alien wave, each alien in the bottom
row is worth 3 points, the middle row of aliens are each worth 2 points,
and the top row of aliens are each worth 1 point. Therefore each alien's score
is ALIEN_ROWS - [row index]._alienscore is initialized in the _alienWave method
when the new wave of aliens is created.

In Wave.py, I created a new hidden attribute _playerscore. It is to store the
player's score. The player score is initiated to 0 in the __init__ method.

In Wave.py, with the _checkAlienCollision method where it detects if an alien
collides with a player bolt, the player score will be increased by adding the
destroyed alien's score: self._playerscore += self._alienscore.get(alienid)

In Wave.py, I created a getter getPlayerScore(self) to return the _playscore.

In app.py, with the _STATE_ACTIVE_Helper method, I call the getter in
_STATE_ACTIVE_Helper to display the player score in the GLabel.
