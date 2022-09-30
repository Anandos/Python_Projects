import turtle, random
SPEED = 5

class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.setheading(random.choice([90, 270]))
        self.speed(0)
    
    def move(self):
        """Ball's speed"""
        self.forward(SPEED)
    
    # Left and right paddle's need own functions as calculations are different
    def left_paddle_bounce(self, distance, paddle_y):
        """Calculate ball heading after hitting left paddle"""
        new_heading = (180 - self.heading() + 180)
        self.setheading(new_heading)
        self.setx(-330)
        if self.ycor() > paddle_y:
            self.setheading(self.heading() - (distance * 2))
        elif self.ycor() < paddle_y:
            self.setheading(self.heading() + (distance * 2))

    def right_paddle_bounce(self, distance, paddle_y):
        """Calculate ball heading after hitting right paddle"""
        new_heading = 180 - (self.heading() - 180)
        self.setheading(new_heading)
        self.setx(330)
        if self.ycor() > paddle_y:
            self.setheading(self.heading() + distance)
        elif self.ycor() < paddle_y:
            self.setheading(self.heading() - distance)

    def wall_bounce(self):
        """Check if bal hits top or bottom walls, return True to count bounces"""
        if self.ycor() <= -250: # self hits bottom
            self.setheading(360 - (self.heading() - 180))
            return True
        elif self.ycor() >= 250: # self hits top
            self.setheading(180 - self.heading())
            return True
        else:
            return False
    
    def reset(self):
        """Reset Ball position, and set a horizontal heading"""
        self.goto(0, 0)
        if self.heading() <= 180:
            self.setheading(90)
        else:
            self.setheading(270)
        
        

