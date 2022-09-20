import turtle, snake, food, score, time

screen = turtle.Screen()  # initialise screen
snake = snake.Snake()  # initialise snake
food = food.Food()  # initialise food
scoreboard = score.Score()  # initialise score
screen_size = 400
screen.tracer(0)
screen.setup(width=screen_size, height=screen_size)
screen.bgcolor("grey")
screen.title("Snake Game")

snake_segments = []
snake.snake_setup(3)

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.lft, "Left")
screen.onkey(snake.rght, "Right")
screen.onkey(quit, "q")

scoreboard.get_high_score()
snake.move()
i = 0
game_on = True
while game_on:
    screen.update()
    time.sleep(0.4)
    snake.move()

    if not snake.check_boundary() or not snake.check_ouroboros():  # check if defeat
        snake.reset()
        scoreboard.reset()

    i += 1
    if i >= 20:  # food expired?
        food.reposition_food()
        i = 0
        print("food repositioned")
        snake.head_position()

    if food.distance(snake.head_position()) < 5:  # eat food?
        scoreboard.iterate_score()
        food.reposition_food()
        snake.grow_snake()
        i = 0
        print(f"om nom nom, score is now {score}")

print(f"\nScore was {scoreboard.score}\nGame Over")
scoreboard.game_over()

screen.exitonclick()
