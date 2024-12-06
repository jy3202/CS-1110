"""
A module to draw cool shapes with the introcs Turtle.

You call all of these functions in the interactive shell, but you will have
to create a Window first.  Alternatively, you can use the a4test.py test script
to try out the functions.
"""
from introcs.turtle import Window, Turtle, Pen
import introcs  # For the RGB and HSV objects
import math     # For the math computations


################# Helpers for Precondition Verification #################

def is_number(x):
    """
    Returns: True if value x is a number; False otherwise.

    Parameter x: the value to check
    Precondition: NONE (x can be any value)
    """
    return type(x) in [float, int]


def is_window(w):
    """
    Returns: True if w is a introcs Window; False otherwise.

    Parameter w: the value to check
    Precondition: NONE (w can be any value)
    """
    return type(w) == Window


def is_valid_color(c):
    """
    Returns: True c is a valid turtle color; False otherwise

    Parameter c: the value to check
    Precondition: NONE (c can be any value)
    """
    return (type(c) == introcs.RGB or type(c) == introcs.HSV or
            (type(c) == str and (introcs.is_tkcolor(c) or introcs.is_webcolor(c))))


def is_valid_speed(sp):
    """
    Returns: True if sp is an int in range 0..10; False otherwise.

    Parameter sp: the value to check
    Precondition: NONE (sp can be any value)
    """
    return (type(sp) == int and 0 <= sp and sp <= 10)


def is_valid_length(side):
    """
    Returns: True if side is a number >= 0; False otherwise.

    Parameter side: the value to check
    Precondition: NONE (side can be any value)
    """
    return (is_number(side) and 0 <= side)


def is_valid_iteration(n):
    """
    Returns: True if n is an int >= 1; False otherwise.

    Parameter n: the value to check
    Precondition: NONE (n can be any value)
    """
    return (type(n) == int and 1 <= n)


def is_valid_depth(d):
    """
    Returns: True if d is an int >= 0; False otherwise.

    Parameter d: the value to check
    Precondition: NONE (d can be any value)
    """
    return (type(d) == int and d >= 0)


def is_valid_turtlemode(t):
    """
    Returns: True t is a Turtle with drawmode True; False otherwise.

    Parameter t: the value to check
    Precondition: NONE (t can be any value)
    """
    return (type(t) == Turtle and t.drawmode)


def is_valid_penmode(p):
    """
    Returns: True t is a Pen with solid False; False otherwise.

    Parameter p: the value to check
    Precondition: NONE (p can be any value)
    """
    return (type(p) == Pen and not p.solid)


def report_error(message, value):
    """
    Returns: An error message about the given value.

    This is a function for constructing error messages to be used in assert
    statements. We find that students often introduce bugs into their assert
    statement messages, and do not find them because they are in the habit of
    not writing tests that violate preconditions.

    The purpose of this function is to give you an easy way of making error
    messages without having to worry about introducing such bugs. Look at
    the function draw_two_lines for the proper way to use it.

    Parameter message: The error message to display
    Precondition: message is a string

    Parameter value: The value that caused the error
    Precondition: NONE (value can be anything)
    """
    return message+': '+repr(value)

def complement_rgb(rgb):
    """
    Returns the complement of color rgb.

    Parameter rgb: the color to complement
    Precondition: rgb is an RGB object
    """
    return introcs.RGB(255-rgb.red, 255-rgb.green, 255-rgb.blue)


#################### DEMO: Two lines ####################

def draw_two_lines(w,sp):
    """
    Draws two lines on to window w.

    This function clears w of any previous drawings. Then, in the middle of
    the window w, this function draws a green line 100 pixels to the east,
    and then a blue line 200 pixels to the north. It uses a new turtle that
    moves at speed sp, 0 <= sp <= 10, with 1 being slowest and 10 fastest
    (and 0 being "instant").

    REMEMBER: You need to flush the turtle if the speed is 0.

    This procedure asserts all preconditions.

    Parameter w: The window to draw upon.
    Precondition: w is a introcs Window object.

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # Clear the window first!
    w.clear()

    # Create a turtle and draw
    t = Turtle(w)
    t.speed = sp
    t.color = 'green'
    t.forward(100) # draw a line 100 pixels in the current direction
    t.left(90)     # add 90 degrees to the angle
    t.color = 'blue'
    t.forward(200)

    # This is necessary if speed is 0!
    t.flush()


#################### TASK 1: Triangle ####################

def draw_triangle(t, s, c):
    """
    Draws an equilateral triangle of side s and color c at current position.

    The direction of the triangle depends on the current facing of the turtle.
    If the turtle is facing west, the triangle points up and the turtle starts
    and ends at the east end of the base line.

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (x and y, within round-off errors), heading, color, and drawmode.
    If you changed any of these in the function, you must change them back.

    REMEMBER: You need to flush the turtle if the speed is 0.

    This procedure asserts all preconditions.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter s: The length of each triangle side
    Precondition: s is a valid side length (number >= 0)

    Parameter c: The triangle color
    Precondition: c is a valid turtle color (see the helper function above)
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(s), report_error('Invalid side length', s)
    assert is_valid_color(c), report_error('Invalid color', c)

    # Save the original attributes
    orgcolor = t.color
    orgdrawmode = t.drawmode

    # Set color
    t.color = c

    # For loop range 0..3
    for x in range(0,3):
        # Go s length from current position
        t.forward(s)
        # Turn 120 degrees counterclockwise
        t.left(120)

    # Restore attributes to original values
    t.color = orgcolor
    t.drawmode = orgdrawmode

    # This is necessary if speed is 0!
    t.flush()

    # Hint: each angle in an equilateral triangle is 60 degrees.
    # Note: In this function, DO NOT save the turtle position and heading
    # in the beginning and then restore them at the end. The turtle moves
    # should be such that the turtle ends up where it started and facing
    # in the same direction, automatically.

    # Also, 3 lines have to be drawn. Does this suggest a for loop that
    # processes the range 0..2?
    pass


#################### TASK 2: Hexagon ####################

def draw_hex(t, s):
    """
    Draws six triangles using the color 'cyan' to make a hexagon.

    The triangles are equilateral triangles, using draw_triangle as a helper.
    The drawing starts at the turtle's current position and heading. The
    middle of the hexagon is the turtle's starting position.

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (x and y, within round-off errors), heading, color, and drawmode.
    If you changed any of these in the function, you must change them back.

    REMEMBER: You need to flush the turtle if the speed is 0.

    This procedure asserts all preconditions.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter s: The length of each triangle side
    Precondition: s is a valid side length (number >= 0)
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(s), report_error('Invalid side length', s)

    # For loop range 0..6
    for x in range(0,6):
        # Draw triangle
        draw_triangle(t, s, 'cyan')
        # Turn 60 degrees counterclockwise
        t.left(60)

    #flush
    t.flush()


    # Note: Do not save any of the turtle's properties and then restore them
    # at the end. Just use 6 calls on procedures drawTriangle and t.left. Test
    # the procedure to make sure that t's final location and heading are the
    # same as t's initial location and heading (except for roundoff error).
    pass


#################### Task 3A: Spirals ####################

def draw_spiral(w, side, ang, n, sp):
    """
    Draws a spiral using draw_spiral_helper(t, side, ang, n, sp)

    This function clears the window and makes a new turtle t.  This turtle
    starts in the middle of the canvas facing south (NOT the default east).
    It then calls draw_spiral_helper(t, side, ang, n, sp). When it is done,
    the turtle is left hidden (visible is False).

    REMEMBER: You need to flush the turtle if the speed is 0.

    This procedure asserts all preconditions.

    Parameter w: The window to draw upon.
    Precondition: w is a introcs Window object.

    Parameter side: The length of each spiral side
    Precondition: side is a valid side length (number >= 0)

    Parameter ang: The angle of each corner of the spiral
    Precondition: ang is a number

    Parameter n: The number of edges of the spiral
    Precondition: n is a valid number of iterations (int >= 1)

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert is_number(ang), report_error('ang is not a valid number',ang)
    assert is_valid_iteration(n), report_error('n is an invalid number',n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # Clear Window
    w.clear()

    # Create TURTLE
    t = Turtle(w)

    # Set Turtle drawmode to True
    t.drawmode == True

    # Turtle starts facing north
    t.left(-90)

    # Call multi_polygons_helper
    draw_spiral_helper(t, side, ang, n, sp)

    # Set Turtle visible to False
    t.visible = False

    # Flush
    t.flush()

    # HINT: w.clear() clears window.
    # HINT: Set the visible attribute to False at the end, and remember
    # to flush
    pass


def draw_spiral_helper(t, side, ang, n, sp):
    """
    Draws a spiral of n lines at the current position and heading.

    The spiral begins at the current turtle position and heading, turning ang
    degrees to the left after each line. Line 0 is side pixels long. Line 1
    is 2*side pixels long, and so on.  Hence each Line i is (i+1)*side pixels
    long. The lines alternate between blue, magenta, and red, in that order,
    with the first one blue.

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    color, speed, visible, and drawmode. However, the final position and
    heading may be different. If you changed any of these four in the
    function, you must change them back.

    This procedure asserts all preconditions.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter side: The length of each spiral side
    Precondition: side is a valid side length (number >= 0)

    Parameter ang: The angle of each corner of the spiral
    Precondition: ang is a number

    Parameter n: The number of edges of the spiral
    Precondition: n is a valid number of iterations (int >= 1)

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert is_number(ang), report_error('ang is not a valid number',ang)
    assert is_valid_iteration(n), report_error('n is an invalid number', n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # Save the original attributes based on specifications
    orgcolor = t.color
    orgspeed = t.speed
    orgvisible = t.visible
    orgdrawmode = t.drawmode

    # Set the Turtle speed to be the given sp
    t.speed = sp

    # Set color list
    colors = ['blue','magenta','red']
    c = colors[0]

    # For loop range 0..n
    for x in range(0,n):
        t.color = c
        # Go (x+1)*side length from current position
        t.forward((x+1)*side)
        # Turn ang degrees counterclockwise
        t.left(ang)
        # Change color through the list
        if c == colors[0]:
            c = colors[1]
        elif c == colors[1]:
            c = colors[2]
        elif c == colors[2]:
            c = colors[0]

    # Restore the original attributes based on specifications
    t.color = orgcolor
    t.speed = orgspeed
    t.visible = orgvisible
    t.drawmode = orgdrawmode

    # NOTE: Since n lines must be drawn, use a for loop on a range of integers.
    pass


#################### TASK 3B: Polygons ####################

def multi_polygons(w, side, k, n, sp):
    """
    Draws polygons using multi_polygons_helper(t, side, k, n, sp)

    This function clears the window and makes a new turtle t. This turtle
    starts in the middle of the canvas facing north (NOT the default east).
    It then calls multi_polygons_helper(t, side, k, n, sp). When it is done,
    the turtle is left hidden (visible is False).

    REMEMBER: You need to flush the turtle if the speed is 0.

    This procedure asserts all preconditions.

    Parameter w: The window to draw upon.
    Precondition: w is a introcs Window object.

    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)

    Parameter k: The number of polygons to draw
    Precondition: k is an int >= 1

    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 3

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert type(k)==int and k>=1, report_error('k is not a valid # polygons',k)
    assert type(n)==int and n>=3, report_error('n is not a # poly sides',n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # Clear Window
    w.clear()

    # Create TURTLE
    t = Turtle(w)

    # Set Turtle drawmode to true
    t.drawmode == True

    # Turtle starts facing north
    t.left(90)

    # Call multi_polygons_helper
    multi_polygons_helper(t, side, k, n, sp)

    # Set Turtle visible to False
    t.visible = False

    # Flush
    t.flush()

    # HINT: w.clear() clears window.
    # HINT: Set the visible attribute to False at the end, and remember to flush
    pass


def multi_polygons_helper(t, side, k, n, sp):
    """
    Draws k n-sided polygons of side length s.

    The polygons are drawn by turtle t, starting at the current position. The
    turtles alternate colors between blue and orange (starting with blue).
    Each polygon is drawn starting at the same place (within roundoff errors),
    but t turns left 360.0/k degrees after each polygon.

    At the end, ALL ATTRIBUTES of the turtle are the same as they were in the
    beginning (within roundoff errors). If you change any attributes of the
    turtle. then you must restore them. Look at the helper draw_polygon for
    more information.

    This procedure asserts all preconditions.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)

    Parameter k: The number of polygons to draw
    Precondition: k is an int >= 1

    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 3

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert type(k) == int and k >= 1, report_error('k is an invalid number',k)
    assert type(n) == int and n >= 3, report_error('n is an invalid number',n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # Save the ALL original attributes based on the specifications
    orgx = t.x
    orgy = t.y
    orgheading = t.heading
    orgcolor = t.color
    orgspeed = t.speed
    orgvisible = t.visible
    orgdrawmode = t.drawmode

    # Set color list
    colors = ['blue','orange']
    c = colors[0]

    # Set speed according to given sp
    t.speed = sp

    # For loop range 0..k
    for y in range(0,k):
        t.color = c
        # For loop range 0..n
        for x in range(0,n):
            # Turn 360/n degrees counterclockwise
            t.left(360/n)
            # Go s length from current position
            t.forward(side)
        t.left(360/k)
        # Alternate color in the list
        if c == colors[0]:
            c = colors[1]
        elif c == colors[1]:
            c = colors[0]

    # Restore ALL attributes to original values based on the specifications
    t.move(orgx,orgy)
    t.heading = orgheading
    t.color = orgcolor
    t.speed = orgspeed
    t.visible = orgvisible
    t.drawmode = orgdrawmode

    # HINT: Make sure you restore t's color and speed when done
    # HINT: Since k polygons should be drawn, use a for-loop on a range of numbers.
    pass


# DO NOT MODIFY
def draw_polygon(t, side, n):
    """
    Draws an n-sided polygon using of side length side.

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    position (x and y, within round-off errors), heading, color, speed,
    visible, and drawmode. There is no need to restore these.

    This procedure asserts all preconditions.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter side: The length of each polygon side
    Precondition: side is a valid side length (number >= 0)

    Parameter n: The number of sides of each polygon
    Precondition: n is an int >= 1
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert type(n) == int and n >= 1, report_error('n is an invalid # sides',n)

    # Remember old speed
    ang = 360.0/n # exterior angle between adjacent sides

    # t is in position and facing the direction to draw the next line.
    for _ in range(n):
        t.forward(side)
        t.left(ang)


#################### TASK 3C: Radiating Petals ####################

def radiate(w, side, n, sp):
    """
    Drawd n straight radiating lines using radiate_helper(t, side, n, sp)

    This function clears the window and makes a new turtle t.  This turtle
    starts in the middle of the canvas facing west (NOT the default east).
    It then calls radiate_helper(t, side, n, sp). When it is done, the turtle
    is left hidden (visible is False).

    REMEMBER: You need to flush the turtle if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a tkturtle Window object.

    Parameter side: The length of each radial line
    Precondition: side is a valid side length (number >= 0)

    Parameter n: The number of lines to draw
    Precondition: n is an int >= 2

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # HINT: w.clear() clears window.
    # HINT: Set the visible attribute to False at the end, and remember to flush
    pass


def radiate_helper(t, side, n, sp):
    """
    Draws n straight radiating lines of length s at equal angles.

    This lines are drawn using turtle t with the turtle moving at speed sp.
    A line drawn at angle ang, 0 <= ang < 360 has HSL color (ang % 360.0, 1, 0.4).

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    color, speed, visible, and drawmode. However, the final position and
    heading may be different. If you changed any of these four in the
    function, you must change them back.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter side: The length of each radial line
    Precondition: side is a valid side length (number >= 0)

    Parameter n: The number of lines to draw
    Precondition: n is an int >= 2

    Parameter sp: The turtle speed.
    Precondition: sp is a valid turtle speed.
    """
    # Assert the preconditions
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert (type(n) == int and n >= 2), report_error('n is an invalid #',n)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # Hints:
    # 1. Drawing n lines should be draw with a  range loop.
    # 2. The heading of the turtle should stay in the range 0 <= heading < 360.
    # 3. (t.heading % 360.0, 1, 1) is the HSL color of the turtle for each line
    # 4. Use the method webcolor to convert an HSL object to a turtle color
    pass


#################### TASK 4A: Sierpinski Triangle ####################

def triangle(w, side, d, sp):
    """
    Draws a Sierpinski triangle with the given side length and depth d.

    This function clears the window and makes a new pen p.  This pen starts at the
    triangle center (0,0). This method draws the triangle by calling the helper
    function triangle_helper with color blue: RGB(0,0,255). The pen is hidden during
    drawing and left hidden at the end.

    REMEMBER: You need to flush the pen if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a cornell Window object.

    Parameter side: The side length of the triangle
    Precondition: side is a valid side length (number >= 0)

    Parameter d: The recursive depth of the triangle
    Precondition: n is a valid depth (int >= 0)

    Parameter sp: The pen speed.
    Precondition: sp is a valid pen speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert is_valid_depth(d), report_error('d is an invalid depth',d)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # Clear Window
    w.clear()

    # Create Pen
    p = Pen(w)

    # Set pen speed to given sp
    p.speed = sp

    # Define color (blue)
    color = introcs.RGB(0,0,255)
    p.edgecolor = color
    p.fillcolor = color

    # Set pen visible attribute to False
    p.visible = False

    # Call Helpers to draw
    triangle_helper(p, 0, 0, color, side, d)
    p.visible = False

    # Flush
    p.flush()

    # HINT: w.clear() clears window.
    # HINT: Set the visible attribute to False at the end, and remember to flush
    pass


def triangle_helper(p, x, y, color, side, d):
    """
    Draws a Sierpinski triangle with side length s and depth d, anchored at (x, y).

    The triangle is draw with current pen visibility attribute, but it uses the provided
    color. Follow the instructions on the course website to recursively draw the
    Sierpinski triangle. Remember to draw an upside down triangle in the center with the
    complement of color.

    Parameter p: The graphics pen
    Precondition: p is a Pen with fill attribute False.

    Parameter x: The x-coordinate of the triangle center
    Precondition: x is a number

    Parameter y: The y-coordinate of the triangle center
    Precondition: y is a number

    Parameter color: The triangle color
    Precondition: color is an RGB object (NOT a string)

    Parameter side: The side-length of the triangle
    Precondition: side is a valid side length (number >= 0)

    Parameter d: The recursive depth of the triangle
    Precondition: n is a valid depth (int >= 0)
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    assert is_number(x), report_error('x is not a valid number',x)
    assert is_number(y), report_error('y is not a valid number',y)
    assert is_valid_color(color), report_error('Invalid color', color)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert is_valid_depth(d), report_error('d is an invalid depth',d)

    # Base case
    if d == 0:
        fill_triangle(p, x, y, side, True)
    elif d > 0:
        # Set color
        color = introcs.RGB(0,0,255)
        p.edgecolor = color
        p.fillcolor = color
        h = (side*math.sqrt(.75))/4

        # Draw bottom left triangle with side/2 and d-1 depth
        triangle_helper(p, x-side/4, y-h, color, side/2, d-1)
        # Draw top triangle with side/2 and d-1 depth
        triangle_helper(p, x, y+h, color, side/2, d-1)
        # Draw bottom right triangle with side/2 and d-1 depth
        triangle_helper(p, x+side/4, y-h, color, side/2, d-1)

        # Complement color
        color = complement_rgb(color)
        p.edgecolor = color
        p.fillcolor = color

        # Draw upsidedown triangle in the middle with side/2
        fill_triangle(p, x, y-(side*math.sqrt(.75))/4, side/2, False)

        # Complement color back
        color = complement_rgb(color)


    #call fill_triangle
    # Hint: Use fill_triangle to draw an individual triangle
    pass


# DO NOT MODIFY
def fill_triangle(p, x, y, side, up):
    """
    Fills an equilateral triangle of side length centered at (0,0)

    The triangle may either be pointing up or down, depending upon the value
    of parameter up.

    Parameter p: The graphics pen
    Precondition: p is a Pen with fill attribute False.

    Parameter x: The x-coordinate of the triangle center
    Precondition: x is a number

    Parameter y: The y-coordinate of the triangle center
    Precondition: y is a number

    Parameter side: The side length of the triangle
    Precondition: side is a valid side length (number >= 0)
    """
    # Precondition Assertions
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    assert is_number(x), report_error('x is not a valid position',x)
    assert is_number(y), report_error('x is not a valid position',y)
    assert is_valid_length(side), report_error('side is an invalid length',side)

    h = side * math.sqrt(.75)
    if not up:
        h = -h

    p.move(x-side/2, y-h/2)
    p.solid = True
    p.drawLine(side, 0)
    p.drawLine(-side/2.0, h)
    p.drawLine(-side/2.0, -h)
    p.solid = False


#################### TASK 4B: Sierpinski Snowflake ####################

def snowflake(w, side, d, sp):
    """
    Draws a Sierpinski snowflake with the given side length and depth d.

    This function clears the window and makes a new graphics pen p.  This pen starts
    in the middle of the canvas at (0,0). It draws by calling the function
    sierpinski_helper(p, 0, 0, side, d). The pen is hidden during drawing and left
    hidden at the end.

    The pen should have fill color 'deep sky blue' and a 'black' line color.

    REMEMBER: You need to flush the pen if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a cornell Window object.

    Parameter side: The side-length of the snowflake
    Precondition: side is a valid side length (number >= 0)

    Parameter d: The recursive depth of the snowflake
    Precondition: n is a valid depth (int >= 0)
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert is_valid_depth(d), report_error('d is an invalid depth',d)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # Clear the window first!
    w.clear()

    # Create pen
    p = Pen(w)

    # Set pen speed to given sp
    p.speed = sp

    # Set pen color
    color = introcs.RGB(0, 0, 255)
    p.edgecolor = "black"
    p.fillcolor = "deep sky blue"

    # Set pen visible to False
    p.visible = False

    # Call snowflake_helper
    snowflake_helper(p, 0, 0, side, d)
    p.visible = False

    # Flush
    p.flush()

    # HINT: w.clear() clears window.
    # HINT: Set the visible attribute to False at the end, and remember to flush
    pass


def snowflake_helper(p, x, y, side, d):
    """
    Draws a snowflake with the given side length and depth d centered at (x, y).

    The snowflake is draw with the current pen color and visibility attribute. Follow the
    instructions on the course website to recursively draw the Sierpinski snowflake.

    Parameter p: The graphics pen
    Precondition: p is a Pen with fill attribute False.

    Parameter x: The x-coordinate of the snowflake center
    Precondition: x is a number

    Parameter y: The y-coordinate of the snowflake center
    Precondition: y is a number

    Parameter side: The side-length of the snowflake
    Precondition: side is a valid side length (number >= 0)

    Parameter d: The recursive depth of the snowflake
    Precondition: n is a valid depth (int >= 0)
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    assert is_number(x), report_error('x is not a valid position',x)
    assert is_number(y), report_error('x is not a valid position',y)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert is_valid_depth(d), report_error('d is an invalid depth',d)

    # Base case
    if d == 0:
        fill_hex(p, x, y, side)
    else:
        h = side*math.sin(math.radians(60))
        snowflake_helper(p, x-side/3, y- (2/3)*h, side/3, d-1)
        snowflake_helper(p, x-2*side/3, y, side/3, d-1)
        snowflake_helper(p, x-side/3, y+ (2/3)*h, side/3, d-1)
        snowflake_helper(p, x+side/3, y+ (2/3)*h, side/3, d-1)
        snowflake_helper(p, x+2*side/3, y, side/3, d-1)
        snowflake_helper(p, x+side/3, y- (2/3)*h, side/3, d-1)
    # HINT: Use fill_hex instead of setting p's position directly
    pass


# DO NOT MODIFY
def fill_hex(p, x, y, side):
    """
    Fills a hexagon of side length s with center at (x, y) using pen p.

    Parameter p: The graphics pen
    Precondition: p is a Pen with fill attribute False.

    Parameter x: The x-coordinate of the hexagon center
    Precondition: x is a number

    Parameter y: The y-coordinate of the hexagon center
    Precondition: y is a number

    Parameter side: The side length of the hexagon
    Precondition: side is a valid side length (number >= 0)
    """
    # Precondition assertions omitted
    assert is_valid_penmode(p), report_error('Invalid pen mode', p)
    assert is_number(x), report_error('x is not a valid position',x)
    assert is_number(y), report_error('y is not a valid position',y)
    assert is_valid_length(side), report_error('side is an invalid length',side)

    # Move to the center and draw
    p.move(x + side, y)
    dx = side*math.cos(math.pi/3.0)
    dy = side*math.sin(math.pi/3.0)
    p.solid = True
    p.drawLine(  -dx,  dy)
    p.drawLine(-side,   0)
    p.drawLine(  -dx, -dy)
    p.drawLine(   dx, -dy)
    p.drawLine( side,   0)
    p.drawLine(   dx,  dy)
    p.solid = False


#################### TASK 5: Sierpinski Arrowhead ####################

def arrowhead(w, side, d, sp):
    """
    Draws a Sierpinski arrowhead with the given side length and depth d.

    This function clears the window and makes a new turtle T. While the arrowhead
    triangle is centered at (0,0), the turtle will need to move to the bottom left
    corner of the triangle (see the instructions for how to compute the position).
    The turtle should start facing east and draw a left-turning arrowhead by calling
    arrowhead_helper.

    The turtle should be visible while drawing, but hidden at the end. The turtle
    color is 'sea green'.

    REMEMBER: You need to flush the turtle if the speed is 0.

    Parameter w: The window to draw upon.
    Precondition: w is a Window object.

    Parameter side: The side-length of the arrowhead triangle
    Precondition: side is a valid side length (number >= 0)

    Parameter d: The recursive depth of the arrowhead triangle
    Precondition: n is a valid depth (int >= 0)

    Parameter sp: The drawing speed.
    Precondition: sp is a valid turtle/pen speed.
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_window(w), report_error('w is not a valid window',w)
    assert is_valid_length(side), report_error('side is an invalid length',side)
    assert is_valid_depth(d), report_error('d is an invalid depth',d)
    assert is_valid_speed(sp), report_error('sp is not a valid speed',sp)

    # Clear Window
    w.clear()

    # Create TURTLE
    t = Turtle(w)

    # Set Turtle drawmode to True
    t.drawmode = True

    # Set Turtle visible to True
    t.visible = True

    # Set Turtle speedn to given sp
    t.speed = sp

    # Set Turtle color to "sea green"
    t.color = 'sea green'

    # Move Turtle to bottom left corner of the triangle
    t.move(0-side/2,0-(side*math.sqrt(.75))/2)

    # Call arrowhead_helper to draw a left-turning arrowhead (left = True)
    arrowhead_helper(t, side, True, d)

    # Set Turtle visible False
    t.visible = False

    # Flush
    t.flush()

    # HINT: w.clear() clears window.
    # HINT: Set the visible attribute to False at the end, and remember to flush
    pass


def arrowhead_helper(t, length, left, d):
    """
    Draws an arrowhead with the given length and depth d at the current position.

    The edge is draw with the current turtle color. You should make no assumptions of
    the current angle of the turtle (e.g. use left and right to turn; do not set the
    heading). See the instructions for the difference between a left-turning edge
    and a right-turning edge.

    WHEN DONE, THE FOLLOWING TURTLE ATTRIBUTES ARE THE SAME AS IT STARTED:
    color, speed, visible, and drawmode. However, the final position and
    heading may be different. If you changed any of these four in the function,
    you must change them back.

    Parameter t: The drawing Turtle
    Precondition: t is a Turtle with drawmode True.

    Parameter length: The length of each side in the arrowhead triangle
    Precondition: length is a valid side length (number >= 0)

    Parameter left: The arrowhead orientation (true if left-turning edge)
    Precondition: left is a boolean

    Parameter d: The recursive depth of the edge
    Precondition: n is a valid depth (int >= 0)
    """
    # ARE THESE ALL OF THE PRECONDITIONS?
    assert is_valid_turtlemode(t), report_error('Invalid turtle mode', t)
    assert is_valid_length(length), report_error('length is invalid',length)
    assert type(left) == bool, report_error('left is an invalid boolean',left)
    assert is_valid_depth(d), report_error('d is an invalid depth',d)

    # Save the original attributes based on the specification
    orgcolor = t.color
    orgspeed = t.speed
    orgvisible = t.visible
    orgdrawmode = t.drawmode

    # Base case
    if d==0:
        t.forward(length)

    else:
        if left == True:
            angle = 60
            opp = False
        else:
            angle = -60
            opp = True

        # Turtle turns 60 degrees in its direction of orientation
        t.left(angle)
        # Turtle draws 1/2 length in the opposite orientation at d-1 depth
        arrowhead_helper(t, length/2, opp, d-1)
        # Turtle turns 60 degrees in the opposite direction of its orientation
        t.left(-angle)
        # Turtle draws 1/2 length in the same orientation at d-1 depth
        arrowhead_helper(t, length/2, left, d-1)
        # Turtle turnes 60 degrees in the opposite direction of its orientation
        t.left(-angle)
        # Turtle draws 1/2 length in the opposite orientation at d-1 depth
        arrowhead_helper(t, length/2, opp, d-1)
        # Turtle turns back 60 degrees in the orientation direction
        t.left(angle)

    # Restore the original attributes based on the specification
    t.color = orgcolor
    t.speed = orgspeed
    t.visible = orgvisible
    t.drawmode = orgdrawmode

    # HINT: Look at the picture from the instructions.
    # Note how the turning angle changes as it draws
    pass
