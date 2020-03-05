import turtle
import math
import os
import random
from playsound import playsound

# screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("back.gif")
# playsound('background.wav')

turtle.register_shape("bullet.gif")
turtle.register_shape("ene.gif")
turtle.register_shape("player.gif")

# border
border = turtle.Turtle()  # object
border.speed(0)
border.color("blue")
border.penup()
border.setposition(-300, -300)
border.pendown()
border.pensize(4)
for side in range(4):
    border.fd(600)
    border.lt(90)
border.hideturtle()

# set the score to 0
score = 0
# draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 270)
scorestring = "Score:%s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()


# player turtle
player = turtle.Turtle()  # object
player.color("green")
player.shape("player.gif")
player.penup()
player.speed(0)  # fastest
player.setposition(0, -250)
player.setheading(90)  # to make triangle straight

# moving the player
playerspeed = 15


enemyspeed = 2

# choose no. of enemies
number_of_enemies = 5
# create empty list of enemies
enemies = []
# Add enemies to list
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())
for enemy in enemies:
    enemy.color("red")
    enemy.shape("ene.gif")
    enemy.penup()  # restrict from drawing
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)


# player weapon

bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("bullet.gif")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 20

# bullet states
# ready
# fire
bulletstate = "ready"


# to left


def move_left():
    x = player.xcor()  # default x coordinate value=0
    x -= playerspeed  # takes value of x subtracts speed from it and assign it to x value=-15
    if x < -280:  # limit to move
        x = -280
    player.setx(x)  # changing location to new x coordinate(-15)


def move_right():
    x = player.xcor()
    x += playerspeed  # + to move right
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    # bullet state as global if needs to be changed
    global bulletstate
    if bulletstate == "ready":  # if bullet is ready
        bulletstate = "fire"  # fire if ready
        x = player.xcor()
        y = player.ycor()+10
        bullet.setposition(x, y)
        bullet.showturtle()


def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(), 2) +
                         math.pow(t1.ycor()-t2.ycor(), 2))  # standard formula
    if distance < 15:
        return True
    else:
        return False
    # move bullet above the player


# keys
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

#  main game loop

while True:

    for enemy in enemies:
        # move enemy same code as for player
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # reversing enemy
        if enemy.xcor() > 280:
            # move all down
            for e in enemies:
                y = e.ycor()
                y -= 40  # when enemy reaches border it moves down by 40px each time
                e.sety(y)
            enemyspeed *= -1

        if enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

            # check for collision between bullet and enemy
        if isCollision(bullet, enemy):
            playsound('explosion.wav')
            # reset bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            # reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            # update score
            score += 10
            scorestring = "Score:%s" % score
            score_pen.clear()  # to prevent overwriting
            score_pen.write(scorestring, False, align="left",
                            font=("Arial", 14, "normal"))

        if isCollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            print("GAME OVER")
            break

    # move bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # check to see if bullet has gone to top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"  # brings back the state to ready to fire it again


delay = input("Press enter to finish")
