import turtle
import random


class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("light grey")
        self.shape("circle")
        self.shapesize(0.5)
        self.speed("fastest")
        self.reposition_food()

    def reposition_food(self):
        self.hideturtle()
        random_x = random.randrange(-180, 180, 20)
        random_y = random.randrange(-180, 180, 20)
        self.setposition(random_x, random_y)
        self.showturtle()

    def detect_collision_snake(self):
        pass

