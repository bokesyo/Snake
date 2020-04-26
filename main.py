#


# Author: Bokai XU
# Email: bokaixu@link.cuhk.edu.cn
# CSC 1002 Assignment 2


#

# Import lib

from turtle import *
import time
import random
import sys
import datetime


# End of omport


# Snake Module
#
#
#


# Create a snake (only head) in the center of screen at the beginning
def snakeCreate():
    global snake_list
    # snake_list is a list contains coordinates of all the parts of snake, in a ordered way
    global stamp_list
    # stamp_list is a list contains ids of all the parts of snake
    stamp_list = []
    snake_list = [(0, 0)]


# Draw a snake head at the welcome screen
def snakeDrawInit():
    cod_init_snake = snake_list[0]
    ini_x = (cod_init_snake[0]) * 20
    ini_y = (cod_init_snake[1]) * 20
    cod_init_snake_post = [(ini_x, ini_y)]
    snakeDrawGeneral(cod_init_snake_post)
    return


# Input a snake list, it will convert it into a list of coordinate
def snakeConvertCod(snake_list):
    cod_list = []
    for cod in snake_list:
        x = cod[0]
        y = cod[1]
        x_cod = x * 20
        y_cod = y * 20
        new_cod = (x_cod, y_cod)
        cod_list.append(new_cod)
    return cod_list


# Draw the snake head and get the stamp and store it
def snakeDrawRedSqu():
    global stamp_list
    # stamp_list is a list contains ids of all the parts of snake
    screen.tracer(False)
    snake.pencolor("red")
    snake.fillcolor("red")
    snake.shape("square")
    snake.shapesize(1, 1, 0)
    back_stamp = snake.stamp()
    stamp_list.append(back_stamp)
    return


# Draw the snake tail and get stamps and store them
def snakeDrawSqu():
    global stamp_list
    # stamp_list is a list contains ids of all the parts of snake
    tracer(False)
    snake.pencolor("red")
    snake.fillcolor("black")
    snake.shape("square")
    snake.shapesize(1, 1, 0)
    back_stamp = snake.stamp()
    stamp_list.append(back_stamp)
    return


# This is a function used to draw snake
def snakeDrawGeneral(cod_list):
    # Draw head first
    cod_h = cod_list[0]
    x = cod_h[0]
    y = cod_h[1]
    snake.penup()
    snake.goto(x, y)
    snake.pendown()
    snakeDrawRedSqu()
    # End of draw head

    # Draw tail
    idcard = 2
    length = len(cod_list)
    while idcard <= length:
        idi = idcard - 1
        cod_xy = cod_list[idi]
        x = cod_xy[0]
        y = cod_xy[1]
        snake.penup()
        snake.goto(x, y)
        snake.pendown()
        snakeDrawSqu()
        idcard = idcard + 1
    # End of tail
    return


# Input a old list to get a new list. It can make snake walk
def snakeNewList(snake_list, mode='Default'):
    # User control

    # Any unexpected event
    if snake_dir == 'p':
        return snake_list
    # End

    # Normal event
    if True:
        length = len(snake_list)
        new_snake_list = []
        # Add a new box at the head, according to the direction
        if snake_dir == 'l':
            cod = snake_list[0]
            x = cod[0]
            y = cod[1]
            x = x - 1
            new_cod = (x, y)
            new_snake_list.append(new_cod)
        elif snake_dir == 'r':
            # print(snake_dir)
            cod = snake_list[0]
            x = cod[0]
            y = cod[1]
            x = x + 1
            new_cod = (x, y)
            new_snake_list.append(new_cod)
        elif snake_dir == 'u':
            cod = snake_list[0]
            x = cod[0]
            y = cod[1]
            y = y + 1
            new_cod = (x, y)
            new_snake_list.append(new_cod)
        elif snake_dir == 'd':
            cod = snake_list[0]
            x = cod[0]
            y = cod[1]
            y = y - 1
            new_cod = (x, y)
            new_snake_list.append(new_cod)
        for remainder in snake_list:
            new_snake_list.append(remainder)

        # Remove the last box
        if mode == 'average':
            del new_snake_list[length]
        elif mode == 'consume':
            pass
        return new_snake_list


# When the sanke is consuming food, it will slow down the snake timer.
def snakeNewFreq(status='n'):
    # 'n' = normal movement
    # 'e' = the snake is consuming food items
    global snake_freq
    # snake_freq is a variable which determine the refresh rate of snake
    if status == 'e':
        # snake will move slower
        snake_freq = int(2.5 * time_unit)
    else:
        snake_freq = 1 * time_unit
    return snake_freq


# This is the hub of snake
def snakeMoveHub():
    # Every time it runs, it means a movement of snake, it refreshes the title
    # This function always repeat itself
    global n
    global food_list
    global snake_list
    global mons_pos
    # the position of monster
    global over_control
    # a variable determine the status of game, not used

    # controlling variables
    global snake_ctr
    global mons_ctr
    global count_ctr

    # Stamp List
    global stamp_list
    global pause_reason

    # How long should the snake extend? This variable will tell us
    # About food consuming
    global food_payable

    # Renew the title bar every time the snake moves
    statusCountHub()

    # Judge if snake is eaten
    judge_1 = statusIfEatByMons()

    if judge_1:
        # Draw Game over
        statusDrawOver()
        return

    # If the game is over or paused
    if snake_ctr == 'p':
        return
    # Kill this thread

    # Predict if the snake is going out
    # If so, the snake will be paused
    if (20 * abs(snakeNewList(snake_list)[0][1]) > 240) or (20 * abs(snakeNewList(snake_list)[0][0]) > 240):
        pause_reason = 'system'
        snake_ctr = 'p'
        return

    # Judge if user wins
    if (food_list == {}) and (food_payable == 0):
        snake.penup()
        snake.goto(-100, 0)
        snake.write("Winner", font=["Arial Bold", 70])
        snake.pendown()

        # Stop all the threads
        snake_ctr = 'p'
        mons_ctr = 'p'
        # End the hub program, so snake stops moving
        return

    # Judge if snake becomes a loop
    if len(snake_list) >= 2:
        judge_2 = statusIfLoop()
        if judge_2:
            statusDrawOver()
            # If the snake becomes a loop or eaten by monster, End the Hub Program
            return

    # Search food items
    if statusIfFoodInRange():
        food_payable = food_payable + post_food
        cod_food = food_list[post_food]
        x_food = cod_food[0]
        y_food = cod_food[1]
        del food_list[post_food]
        food.penup()
        food.goto(x_food, y_food)
        food.pendown()
        foodCoverSqu()

    # Draw renewed snake
    tracer(False)
    # if the snake is going to extend its tail
    if food_payable > 0:
        snakeNewFreq('e')
        snake_list = snakeNewList(snake_list, 'consume')
        food_payable = food_payable - 1
    # If the snake is not eating any food items
    else:
        snakeNewFreq('n')
        snake_list = snakeNewList(snake_list, 'average')

    # Convert into absolute coordinates
    cod_list = snakeConvertCod(snake_list)

    # Erase the old snake
    snake.clearstamps()
    stamp_list = []
    snake.hideturtle()

    # Draw new snake
    snakeDrawGeneral(cod_list)
    update()
    n = n + 1
    # Renew the keyboard control
    controlKeyUser()
    # New recursion
    ontimer(snakeMoveHub, snake_freq)
    return


#
#
#
# End of Snake Module


# Food Module
#
#
#


# Create random food coordinate and store food data
def foodCreate():
    global food_list
    # food_list is a dictionary which contains all the foods value and corresponding coordinates
    food_list = {}
    for i in range(1, 10):
        while True:
            # The scope of snake head is from -240<=x<=240 and -240<=y<=240, so we pick from -12 to 12.
            generated_data = (20 * random.randint(-12, 11), 20 * random.randint(-12, 11))
            # Avoid repetition
            if not (generated_data in food_list.values()):
                # Cannot place on origin because snake is there
                if not (generated_data == (0, 0)):
                    food_list[i] = generated_data
                    break
    return


# Draw all the food at the beginning of the game
def foodDraw():
    global food_list
    # food_list is a dictionary which contains all the foods value and corresponding coordinates
    food_l = list(food_list.keys())
    # tracer(False)
    for j in food_l:
        cod = food_list[j]
        x_fd = cod[0]
        y_fd = cod[1]
        food.penup()
        food.goto(x_fd, y_fd)
        food.pendown()
        opt = str(j)
        food.write(opt, font=["Arial Bold", 10])
    # update()
    return


# When food is consumed by snake, we cover the corresponding food item by drawing a white square
def foodCoverSqu():
    global food
    # food is a turtle instance which we use to draw food items and eliminate food items
    hideturtle()
    tracer(False)
    food.pencolor("white")
    food.fillcolor("white")
    food.shape("square")
    food.shapesize(1, 1, 0)
    food.stamp()
    return


#
#
#
# End Food Module


# Monster Module
#
#
#


# Create a monster item at the beginning
def monsCreate():
    global mons_pos
    while True:
        mons_cod_list_x = list(range(-10, 11))
        mons_cod_list_y = list(range(-10, 0))
        x_mons = random.choice(mons_cod_list_x)
        y_mons = random.choice(mons_cod_list_y)
        snake_head_cod = snake_list[0]
        snake_head_x = snake_head_cod[0]
        snake_head_y = snake_head_cod[1]
        delta_x = abs(x_mons - snake_head_x)
        delta_y = abs(y_mons - snake_head_y)
        cod_mons = (x_mons, y_mons)
        if (delta_x <= 7) and (delta_y <= 7):
            continue
        else:
            if cod_mons in food_list.values():
                continue
            else:
                break
    mons_pos = (x_mons, y_mons)
    return


# Draw a monster at the welcome screen
def monsDrawInit():
    # mons_pos is the postion of monster
    x_mons = mons_pos[0]
    y_mons = mons_pos[1]
    mons.penup()
    mons.goto(x_mons * 20, y_mons * 20)
    mons.pendown()
    monsDrawGeneral()
    update()
    return


# Generally draw a monster
def monsDrawGeneral():
    global mons_stamp
    # a integer which contains the stamp id of monster
    mons.hideturtle()
    tracer(False)

    # erase old monster
    mons.clearstamp(mons_stamp)
    # end

    # draw a new one
    mons.pencolor("purple")
    mons.fillcolor("purple")
    mons.shape("square")
    mons.shapesize(1, 1, 0)
    mons_stamp = mons.stamp()
    # print('Get stamp id of monster')
    update()

    return


# The algorithm of monster
def monsDirection():
    global snake_list
    global dir_mons
    # dir_mons is the direction where the monster is heading
    # the head of the snake

    # Avoid any unexpected events
    if dir_mons == 'p':
        return dir_mons
    # End

    # Get the snake head
    head_pos = snake_list[0]
    x_head = head_pos[0]
    y_head = head_pos[1]

    # the monster
    x_mons = mons_pos[0]
    y_mons = mons_pos[1]

    # Calculating the distance on x axis and y axis
    adelta_x = x_head - x_mons
    adelta_y = y_head - y_mons

    # Judge module
    if adelta_x == 0:
        # Consider that gradient is infinity
        if adelta_y > 0:
            dir_mons = 'u'
        elif adelta_y < 0:
            dir_mons = 'd'
    else:
        gradient = adelta_y / adelta_x
        if gradient >= 1:
            if adelta_x > 0:
                dir_mons = 'u'
            elif adelta_x < 0:
                dir_mons = 'd'
        elif (gradient < 1) and (gradient > 0):
            if adelta_x < 0:
                dir_mons = 'l'
            elif adelta_x > 0:
                dir_mons = 'r'
        elif gradient == 0:
            if adelta_x > 0:
                dir_mons = 'r'
            elif adelta_x < 0:
                dir_mons = 'l'
        elif (gradient > -1) and (gradient < 0):
            if adelta_x < 0:
                dir_mons = 'l'
            elif adelta_x > 0:
                dir_mons = 'r'
        elif gradient <= -1:
            if adelta_x > 0:
                dir_mons = 'd'
            elif adelta_x < 0:
                dir_mons = 'u'

    return dir_mons


# Randomly pick a time interval for monster
def monsNewFreq():
    global mons_freq
    # mons_freq idetermines the refresh rate of monster

    # it should be slightly higher or smaller than the time unit
    lower_bound = 0.95 * time_unit * 2
    upper_bound = 1.05 * time_unit * 2
    # Randomly choose one
    mons_freq = int(random.uniform(lower_bound, upper_bound))

    return mons_freq


# The hub of monster
def monsMoveHub():
    global over_control

    mons_freq_1 = monsNewFreq()

    # refresh the title bar
    statusCountHub()

    # Judge if snake is eaten
    judge_1 = statusIfEatByMons()

    if judge_1:
        # Draw Game over
        statusDrawOver()
        return

    if mons_ctr == 'p':
        # Avoid bugs
        return
    if not over_control:
        # It will repeat itself
        operation = monsDirection()

        global mons_pos

        if operation == 'u':
            tracer(False)
            x_mons = mons_pos[0]
            y_mons = mons_pos[1]
            mons_step = 1
            y_mons = y_mons + mons_step
            mons_pos = (x_mons, y_mons)
            # print('Monster renewed')
            # print('Monster coordinate is ' + str(mons_pos))
            mons.penup()
            mons.goto(x_mons * 20, y_mons * 20)
            mons.pendown()
            monsDrawGeneral()
            # print('Exec is OK')
            update()
            tracer(False)
        elif operation == 'd':
            tracer(False)
            x_mons = mons_pos[0]
            y_mons = mons_pos[1]
            mons_step = 1
            y_mons = y_mons - mons_step
            mons_pos = (x_mons, y_mons)
            # print('Monster renewed')
            # print('Monster coordinate is ' + str(mons_pos))
            mons.penup()
            mons.goto(x_mons * 20, y_mons * 20)
            mons.pendown()
            monsDrawGeneral()
            # print('Exec is OK')
            update()
            tracer(False)
        elif operation == 'l':
            tracer(False)
            x_mons = mons_pos[0]
            y_mons = mons_pos[1]
            mons_step = 1
            x_mons = x_mons - mons_step
            mons_pos = (x_mons, y_mons)
            # print('Monster renewed')
            # print('Monster coordinate is ' + str(mons_pos))

            # draw a new monster
            mons.penup()
            mons.goto(x_mons * 20, y_mons * 20)
            mons.pendown()
            monsDrawGeneral()
            # print('Exec is OK')
            update()
            tracer(False)
        elif operation == 'r':
            tracer(False)
            x_mons = mons_pos[0]
            y_mons = mons_pos[1]
            mons_step = 1
            x_mons = x_mons + mons_step
            mons_pos = (x_mons, y_mons)
            mons.penup()
            mons.goto(x_mons * 20, y_mons * 20)
            mons.pendown()
            monsDrawGeneral()
            # print('Exec is OK')
            update()
            tracer(False)

        mons_freq_2 = monsNewFreq()
        ontimer(monsMoveHub, mons_freq_2)
        return


#
#
#
# End of Monster Module


# Game Status Module
#
#
#


# Judge if the snake is eaten by monster
def statusIfEatByMons():
    global n
    global food_list
    global over_control
    global snake_list
    global mons_pos

    x_mons_j = mons_pos[0]
    y_mons_j = mons_pos[1]
    snake_head = snake_list[0]
    x_snake_j = snake_head[0]
    y_snake_j = snake_head[1]
    delta_x = x_mons_j - x_snake_j
    delta_y = y_mons_j - y_snake_j

    if (abs(delta_x) < 1) and (abs(delta_y) < 1):
        return True
    else:
        return False


# Just if the snake becomes a loop
def statusIfLoop():
    global n
    global food_list
    global over_control
    global snake_list
    global mons_pos

    length_j = len(snake_list)
    end_index = length_j - 1
    snake_end = snake_list[end_index]
    snake_head = snake_list[0]
    x_snake_je = snake_end[0]
    y_snake_je = snake_end[1]
    x_snake_j = snake_head[0]
    y_snake_j = snake_head[1]
    delta_xe = x_snake_je - x_snake_j
    delta_ye = y_snake_je - y_snake_j

    if (abs(delta_xe) < 1) and (abs(delta_ye) < 1):
        return True
    else:
        return False


# Judge if there is food nearby
def statusIfFoodInRange():
    global post_food

    # global snake_list
    # global food_list
    head_cod = snake_list[0]
    # print('Food item '+str(list(food_list.keys())))

    for food_index in list(food_list.keys()):
        food_cod = food_list[food_index]
        # print('Food coordinate '+str(food_cod))
        x_cod_food = food_cod[0]
        y_cod_food = food_cod[1]
        x_cod_head = head_cod[0] * 20
        y_cod_head = head_cod[1] * 20
        delta_x = x_cod_food - int(x_cod_head)
        delta_y = y_cod_food - int(y_cod_head)
        abs_x = abs(delta_x)
        abs_y = abs(delta_y)

        if (abs_x <= 10) and (abs_y <= 10):
            post_food = food_index
            return True

    return False


# Draw Game Over
def statusDrawOver():
    global snake_ctr
    global mons_ctr
    global count_ctr

    snake_ctr = 'p'
    mons_ctr = 'p'
    count_ctr = 'p'

    snake.penup()
    snake.goto(-170, 0)
    snake.pendown()
    snake.write("Game Over", font=["Arial Bold", 70])


# Judge if there is contact between monster and snake
def statusIfCont():
    global contact_list
    # This is to restore the parts which have intersection with snake
    contact_list_backup = contact_list
    contact_list = []
    x_m = mons_pos[0]
    y_m = mons_pos[1]
    card = 1
    length = len(snake_list)

    while card <= length:
        index_card = card - 1
        cod_xy = snake_list[index_card]
        x_s = cod_xy[0]
        y_s = cod_xy[1]
        delta_x = abs(x_s - x_m)
        # print(delta_x)
        delta_y = abs(y_s - y_m)
        # print(delta_y)
        card = card + 1
        if (delta_x <= 1) and (delta_y <= 1):
            contact_list.append(card)

    if contact_list_backup == []:

        if contact_list != []:
            return 1
        else:
            return 0
    else:
        return 0


# Time counting and contacts counting and display
def statusCountHub():
    global endTime
    global total_numbers
    total_numbers = total_numbers + statusIfCont()
    endTime = time.perf_counter()
    string = "DoodleSnake Time: " + str(int(endTime - start_time)) + ", Contacted: " + str(total_numbers)
    screen.title(string)
    if count_ctr == 'p':
        return
    else:
        # The minimum refresh frequency is 1000 milliseconds
        return


#
#
#
# End of Game Status Module


# Control Module
#
#
#


# Null function
def controlNull():
    # print('Please follow your heart')
    return


# Pause function, pause all the threads
def controlPause():
    global snake_ctr
    global mons_ctr
    global count_ctr
    global pauseTime
    global pause_reason

    # Record pause time
    pauseTime = time.perf_counter()

    # Controlling variables
    snake_ctr = 'p'
    pause_reason = 'system'

    # Waiting the user
    screen.onkey(controlResume, "space")
    screen.listen()
    done()
    # screen.mainloop()


# Bring the game back to life
def controlResume():
    global count_ctr
    global mons_ctr
    global snake_ctr
    global start_time

    # Process time deviation
    resume_time = time.perf_counter()
    time_diff = resume_time - pauseTime
    start_time = start_time + time_diff

    # Controlling Variables
    snake_ctr = 'o'
    ontimer(snakeMoveHub, 0)
    return


# Snake turn right
def controlRight():
    global snake_dir
    global snake_ctr
    global pause_reason
    a = snake_list[0]

    # This is a prediction, if the result is not permitted, the operation will be invalid.
    # Here the snake is at the right border

    # The reason of pause is because of user operation
    if a[0] * 20 + 20 > 240:
        if snake_dir in ['u', 'd']:
            # This is on purpose, we won't give any response
            return
        return
    # The reason of pause is because of system
    elif (pause_reason == 'system') and (snake_dir != 'l'):
        # Here the snake crashed into the border. This is OK, and the system has stopped the snake
        # User can give any valid instructions so the snake will move again.
        snake_dir = 'r'
        snake_ctr = 'o'
        pause_reason = 'Default'
        ontimer(snakeMoveHub, 0)
        return
    else:
        # This is the regular controller!
        if snake_dir == 'u':
            snake_dir = 'r'
        elif snake_dir == 'd':
            snake_dir = 'r'
        return


# Snake turn left
def controlLeft():
    global snake_dir
    global snake_ctr
    global pause_reason
    a = snake_list[0]
    # print(a)
    if a[0] * 20 - 20 < -240:
        if snake_dir in ['u', 'd']:
            return
        return
    else:
        if (pause_reason == 'system') and (snake_dir != 'r'):
            snake_dir = 'l'
            snake_ctr = 'o'
            # print('????')
            pause_reason = 'Default'
            ontimer(snakeMoveHub, 0)
            return
        if snake_dir == 'u':
            snake_dir = 'l'
        elif snake_dir == 'd':
            snake_dir = 'l'
        return


# Snake go up
def controlUp():
    global snake_dir
    global snake_ctr
    global pause_reason
    a = snake_list[0]
    if a[1] * 20 + 20 > 240:
        if snake_dir in ['l', 'r']:
            return
        return
    else:
        if (pause_reason == 'system') and (snake_dir != 'd'):
            snake_dir = 'u'
            snake_ctr = 'o'
            # print('????')
            pause_reason = 'Default'
            ontimer(snakeMoveHub, 0)
            return
        if snake_dir == 'l':
            snake_dir = 'u'
        elif snake_dir == 'r':
            snake_dir = 'u'
        return


# Snake go down
def controlDown():
    global snake_dir
    global snake_ctr
    global pause_reason
    a = snake_list[0]
    if a[1] * 20 - 20 < -240:
        if not (snake_dir in ['l', 'r']):
            snake_ctr = 'p'
            pause_reason = 'system'
            return
        return
    else:
        if (pause_reason == 'system') and (snake_dir != 'u'):
            snake_dir = 'd'
            snake_ctr = 'o'
            pause_reason = 'Default'
            # print('????')
            ontimer(snakeMoveHub, 0)
            return
        if snake_dir == 'l':
            snake_dir = 'd'
        elif snake_dir == 'r':
            snake_dir = 'd'
        return


# Listen function
def controlKeyUser():
    screen.onkey(controlRight, "Right")
    screen.onkey(controlLeft, "Left")
    screen.onkey(controlUp, "Up")
    screen.onkey(controlDown, "Down")
    screen.onkey(controlPause, "space")
    screen.listen()


# Welcome screen
def controlDisplayUI():
    global n
    hideturtle()
    penup()
    goto(-200, 100)
    write("Welcome to Boke's version of Snake\n\n"
          "You are going to use the 4 arrow keys to move the snake\n"
          "around the screen, trying to consume all the food items\n"
          "before the monster catches you...\n\n"
          "click anywhere to start the game, have fun!!", font=["Arial Bold", 15])
    return


# Activate the game at the beginning, after the welcome screen
def controlDynam(x, y):
    global food_payable
    food_payable = 5
    # Make the snake and monster move
    clearscreen()
    controlKeyUser()
    snakeDrawInit()
    monsDrawInit()
    foodDraw()
    ontimer(monsMoveHub, 0)
    ontimer(snakeMoveHub, 0)
    return


#
#
#
# End of User Control Module


# Initializer Module
#
#
#


# Do all the jobs in advance
def initializer():
    # tell us why the snake is stopped
    global pause_reason
    # Declare global variable
    global start_time
    # The time when game starts
    global stamp_list
    # A list contains all stamp ids of snake
    global n
    # The number of operatinons
    global count_ctr
    # Time counting module switch
    global snake_ctr
    # Snake movement module switch
    global mons_ctr
    # Monster movement module switch
    global snake_dir
    # Direction of snake
    global dir_mons
    # Direction of monster
    global total_numbers
    # Total times of contacts
    global mons_stamp
    # The stamp id of monster
    global over_control
    # Game over switch
    global time_unit
    # The unit refresh time interval
    global snake
    # Turtle object snake
    global mons
    # Turtle object monster
    global food
    # Turtle object food
    global screen
    # Turtle onject screen
    global contact_list
    # Id of parts of snake with intersection with snake
    global food_payable
    # How many food should be consumed

    # Set the maximum recursion depth
    sys.setrecursionlimit(999999)

    # Monster
    mons = Turtle()
    # Monster End

    # Food item
    food = Turtle()
    # Food item

    # Snake
    snake = Turtle()
    # Snake End

    pause_reason = 'Default'

    # Game Area
    screen = Screen()
    screen.setup(width=500, height=500)
    # Game Area End

    # Define a minimum refresh frequency
    time_unit = 250

    # Define total contact numbers, initially 0
    total_numbers = 0

    # How many food is to be consumed
    food_payable = 0

    # Define the stamp of monster
    mons_stamp = 0

    # If the game is ended
    over_control = False

    # Define the direction of monster
    dir_mons = 'u'

    # Define the direction of snake
    snake_dir = 'u'

    # How many operations
    n = 0

    # Contacted items of snake
    contact_list = []

    # Designed for user control: pause and resume
    count_ctr = 'o'
    snake_ctr = 'o'
    mons_ctr = 'o'

    # Timer module initialize
    start_time = time.perf_counter()

    # Hide the cursor
    snake.hideturtle()
    food.hideturtle()
    mons.hideturtle()

    # Initialize food items
    foodCreate()

    # Initialize snake item
    snakeCreate()

    # Draw initial image
    snakeDrawInit()

    # Initialize monster item
    monsCreate()

    # Draw initial image
    monsDrawInit()

    # Welcome Screen
    controlDisplayUI()
    screen.onclick(controlDynam)
    done()


#
#
#
# End of Initializer Module


# Start the game
initializer()
# End of the game

