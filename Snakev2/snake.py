import turtle


class Snake(turtle.Turtle):
    def __init__(self):  # modify turtle class to suit snake
        super().__init__()
        self.snake_segments = []
        self.penup()
        self.color("white")
        self.shape("square")
        self.hideturtle()

    def snake_setup(self, input_number):  # call snake class into list of snake objects
        i = 0
        for position in range(input_number):
            new_segment = Snake()
            new_segment.showturtle()
            new_segment.goto(i, 0)
            self.snake_segments.append(new_segment)
            i -= 20

    def move(self):
        for segment in range(len(self.snake_segments) - 1, 0, -1):
            new_x = self.snake_segments[segment - 1].xcor()
            new_y = self.snake_segments[segment - 1].ycor()
            self.snake_segments[segment].goto(new_x, new_y)

        self.snake_segments[0].forward(20)

        print(f"segments number {len(self.snake_segments)}, head position {self.snake_segments[0].xcor()}, "
              f"heading is {self.snake_segments[0].heading()}")

    def grow_snake(self):
        new_segment = Snake()
        new_segment.goto(self.snake_segments[-1].xcor(), self.snake_segments[-1].ycor())
        new_segment.showturtle()
        self.snake_segments.append(new_segment)
        print("snake grown")

    def check_boundary(self):
        if self.snake_segments[0].xcor() > 200 or self.snake_segments[0].xcor() < -200:
            return False
        elif self.snake_segments[0].ycor() > 200 or self.snake_segments[0].ycor() < -200:
            return False
        else:
            return True

    def check_ouroboros(self):
        collision_safe = True
        for i in self.snake_segments[1:]:
            if self.snake_segments[0].distance(i) < 5:
                print("\nOuroboros")
                collision_safe = False
        return collision_safe

    def head_position(self):
        head_x = self.snake_segments[0].xcor()
        head_y = self.snake_segments[0].ycor()
        return head_x, head_y

    def reset(self):
        for seg in self.snake_segments:
            seg.goto(800, 800)
        self.snake_segments = []
        self.snake_setup(3)

    def up(self):
        if self.snake_segments[0].heading() != 270:
            self.snake_segments[0].setheading(90)
            print(f"heading now {self.snake_segments[0].heading()}")

    def down(self):
        if self.snake_segments[0].heading() != 90:
            self.snake_segments[0].setheading(270)
            print(f"heading now {self.snake_segments[0].heading()}")

    def lft(self):
        if self.snake_segments[0].heading() != 0:
            self.snake_segments[0].setheading(180)
            print(f"heading now {self.snake_segments[0].heading()}")

    def rght(self):
        if self.snake_segments[0].heading() != 180:
            self.snake_segments[0].setheading(0)
            print(f"heading now {self.snake_segments[0].heading()}")
