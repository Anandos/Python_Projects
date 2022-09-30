import turtle

class Paddle(turtle.Turtle):
    def __init__(self, x_position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(0.5, 2.5)
        self.penup()
        self.goto(x_position, 0)
        self.speed(0)
    
    def up(self):
        """Move paddle upwards"""
        self.forward(20)
    
    def down(self):
        """Move paddle downwards"""
        self.backward(20)
    
    def reset(self):
        """Reset paddle position"""
        self.sety(0)

        