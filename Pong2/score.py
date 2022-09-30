import turtle
FONT = ("Courier", 22, "normal")

class Scoreboard(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.penup()
        self.color("white")
        self.hideturtle()
        self.goto(0, 200)
        self.score1 = 0
        self.score2 = 0
        self.write(arg=f"{self.score1} : {self.score2}", align="center", font=FONT)

    def update(self, wall):
        """Update score depending on which wall the ball hit"""
        if wall == 1:
            self.score2 += 1
        elif wall == 2:
            self.score1 += 1

        self.clear()
        self.write(arg=f"{self.score1} : {self.score2}", align="center", font=FONT)
    
    def check_winner(self):
        """Check if either player has scored 10 yet"""
        if self.score1 > 9:
            self.goto(0, 0)
            self.write(arg=f"Player 1 Wins!", align="center", font=FONT)
            return False
        elif self.score2 > 9:
            self.goto(0, 0)
            self.write(arg=f"Player 2 Wins!", align="center", font=FONT)
            return False
        else:
            return True
    
