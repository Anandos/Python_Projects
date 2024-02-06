import turtle
import random
import time

# Record score?
# Experiment with shape and colour?

class Snake:
    def __init__(self) -> None:
        self.black = (0, 0, 0)
        self.grey = (128, 128, 128)
        self.light_grey = (192, 192, 192)
        self.white = (255, 255, 255)
        self.screen = turtle.Screen()
        self.screen.title("Snake")
        self.screen.bgcolor("grey")
        self.screen.setup(width= 800, height= 800)
        self.screen.colormode(255)
        self.screen.tracer(0)
        self.screen.listen()

        self.food = turtle.Turtle()
        self.food.color(self.white)
        self.food.shape("circle")
        self.food.shapesize(0.3)
        self.food.up()
        self.food.speed(0)

        self.text = turtle.Turtle()
        self.text.up()
        self.text.hideturtle()
        self.text.color(self.light_grey)
        self.font = ("ArialRoundedMTBold", 40, "bold")
        self.font_big = ("ArialRoundedMTBold", 100, "bold")
        self.font_small = ("ArialRoundedMTBold", 25, "bold")

        self.score = ""
        self.state = "start" #start, game, dead

    
    def start_snake(self):
        self.text.clear()
        self.score = 0
        self.alive = True
        self.head = turtle.Turtle()
        self.head.up()
        self.head.shape("square")
        self.head.color(self.light_grey)
        self.head.speed(0)

        self.snake_body = [self.head]
        self.snake_body[0].goto(0, 0)

        for _ in range(4):
            self.add_snake()
        self.scoreboard()
        self.refresh_food()
    
    def move_snake(self):
        # Shift length of snake body
        for i in range((len(self.snake_body) - 1), 0, -1):
            x, y = self.snake_body[i - 1].pos()
            self.snake_body[i].goto(x, y)

        # Move snake head forwards
        self.snake_body[0].forward(20)

        # Round snake head poistion to stop collision bugs
        x, y = self.snake_body[0].pos()
        self.snake_body[0].goto(round(x), round(y))

        time.sleep(0.1)
        self.screen.update()
    
    def turn_snake(self):
        def up():
            if self.snake_body[0].heading() != 270:
                self.snake_body[0].setheading(90)
        
        def left():
            if self.snake_body[0].heading() != 0:
                self.snake_body[0].setheading(180)
        
        def down():
            if self.snake_body[0].heading() != 90:
                self.snake_body[0].setheading(270)
        
        def right():
            if self.snake_body[0].heading() != 180:
                self.snake_body[0].setheading(0)
        
        def quit():
            print(self.score)
            self.screen.bye()

        self.screen.onkey(key= "w", fun= up)
        self.screen.onkey(key= "a", fun= left)
        self.screen.onkey(key= "s", fun= down)
        self.screen.onkey(key= "d", fun= right)
        self.screen.onkey(key= "q", fun= quit)
    
    def refresh_food(self):
        x = random.randint(-360, 360)
        x = round( x / 20 ) * 20
        y = random.randint(-360, 360)
        y = round( y / 20 ) * 20
        self.food.goto(x, y)
        print(f"food respawn at {x}, {y}")

    def check_food_collision(self):
        # Check if snake head collides with food
        if self.snake_body[0].xcor() == self.food.xcor():
            if self.snake_body[0].ycor() == self.food.ycor():
                self.score += 1
                self.refresh_food()
                self.add_snake()
                self.scoreboard()
                print(f"Score: {self.score}")

    def check_self_collision(self):
        # Check if snake head collides with body list        
        for i in range(len(self.snake_body) - 2):
            x, y = self.snake_body[0].pos()
            i = i + 1
            if self.snake_body[0].xcor() == self.snake_body[i].xcor():
                if self.snake_body[0].ycor() == self.snake_body[i].ycor():
                    print("Snake self collision")
                    self.state = 'dead'
                    self.game_over()
                    self.text.clear()
        
    
    def check_offscreen(self):
        x, y = self.snake_body[0].pos()
        if x > 380 or x < -380:
            print("Snake out of bounds")
            self.state = "dead"
            self.game_over()
            self.text.clear()
        elif y > 380 or y < -380:
            print("Snake out of bounds")
            self.state = "dead"
            self.game_over()
            self.text.clear()
            
    
    def scoreboard(self):
        self.text.clear()
        self.text.color(self.light_grey)
        self.text.write(arg= f"{self.score}", 
                        align= "center", 
                        font= self.font_big)
    
    def add_snake(self):
            body = turtle.Turtle()
            body.shape("square")
            body.up()
            body.goto(0, 0)
            body.speed(0)
            body.color(self.random_colour())
            self.snake_body.append(body)
        
    
    def text_reset(self):
        print("resetting")
        self.text.clear()
        self.text.goto(0, 0)
        self.text.color(self.light_grey)
    
    def random_colour(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)
    
    def game_over(self):
        # Game Over Screen w restart option
        self.text.clear()
        self.text.goto(0, 0)
        self.text.write(arg= f"Game Over", 
                        align= "center", 
                        font= self.font
                        )
        self.text.goto(0, -45)
        self.text.write(arg= f"Score: {self.score}", 
                        align= "center", 
                        font= self.font_small
                        )
        self.text.goto(0, -90)
        self.text.write(arg= f"Press 'q' to quit, 'r' to replay", 
                        align= "center", 
                        font= self.font_small
                        )
        self.text.goto(0,0)
        
        print(f"Game Over, Score: {self.score}")
        
        def quit():
            self.screen.bye()
        
        def restart():
            self.state = "game"
            for body in self.snake_body:
                body.hideturtle()
            
            self.start_snake()
            print("restarting")

        self.screen.onkey(key= "q", fun= quit)
        self.screen.onkey(key= "r", fun= restart)
        
        self.screen.update()
        time.sleep(1)
        self.text.clear()

    def start_screen(self):
        # Start Screen with start and options
        self.text.write(arg= f"SNAKE", 
                        align= "center", 
                        font= self.font
                        )
        self.text.goto(0, -300)
        self.text.write(arg= "press r to start",
                        align= "center",
                        font= self.font_small)
        
        def quit():
            self.screen.bye()

        def start_switch():
            self.state = "game"
            print("starting game")
            self.start_snake()
        
        self.screen.onkey(key= "q", fun= quit)
        self.screen.onkey(key="r", fun= start_switch)
        
        self.screen.update()
        time.sleep(1)
        self.text.clear()
        self.text.goto(0,0)


        
snake = Snake()
while True:
    if snake.state == "start":
        snake.start_screen()

    elif snake.state == "game":
        snake.move_snake()
        snake.turn_snake()
        snake.check_offscreen()
        snake.check_self_collision()
        snake.check_food_collision()

    elif snake.state == "dead":
        snake.game_over()
    
    else:
        print("game state error *o*")
    
    snake.screen.update()

