import turtle, ball, score, paddle, time

# Create ball and move it
# Detect ball and wall collision, and make it bounce
# Detect collision with ball and paddle
# Detect when ball goes out
# Keep score

screen = turtle.Screen()
screen.setup(800, 500)
screen.bgcolor("black")
screen.mode("logo")
screen.tracer(0)

ball = ball.Ball()
scoreboard = score.Scoreboard()
p1_paddle = paddle.Paddle(x_position = -360)
p2_paddle = paddle.Paddle(x_position = 360)

screen.listen()
screen.onkey(p1_paddle.up, "Up")
screen.onkey(p1_paddle.down, "Down")
screen.onkey(p2_paddle.up, "w")
screen.onkey(p2_paddle.down, "s")

bounces = 0
game_on = True
while game_on:
    screen.update()
    ball.move()

    # Ball Hits Paddle?
    if ball.xcor() >= 350 or ball.xcor() <= -350:
        bounces = 0
        if ball.distance(p1_paddle) < 40: # <---
            distance = ball.distance(p1_paddle)
            paddle_y = p1_paddle.ycor()
            ball.left_paddle_bounce(distance, paddle_y)
            
        elif ball.distance(p2_paddle) < 40: # --->
            distance = ball.distance(p2_paddle)
            paddle_y = p2_paddle.ycor()
            ball.right_paddle_bounce(distance, paddle_y)

    # Check if ball htis top or bottom walls, count bounces
    if ball.wall_bounce():
        bounces += 1
    
    if bounces > 5:
        ball.reset()
        time.sleep(1)

    # Ball hits wall and update score
    if ball.xcor() > 400:
        scoreboard.update(wall = 2)
        ball.reset()
        screen.update()
        time.sleep(1)
        
    elif ball.xcor() < -400:
        scoreboard.update(wall = 1)
        ball.reset()
        screen.update()
        time.sleep(1)        

    # Check if someone has won the game
    game_on = scoreboard.check_winner()

screen.exitonclick()


# get distance of centre of paddle to ball
# is ball above or below paddle center
# adjust heading according to distance to centre of paddle and above ot below paddle center
# If ball crosses horizontal walls, inverse the heading
