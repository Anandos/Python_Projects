import turtle


class Score(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("white")
        self.setposition(0, 160)
        self.score = 0
        self.high_score = 0
        self.write_score()

    def write_score(self):
        self.clear()
        self.write(arg=f"Score: {self.score}, High Score: {self.high_score}", align="center", font=("Courier", 14, "normal"))

    def iterate_score(self):
        self.score += 1
        self.write_score()

    def game_over(self):
        self.setposition(0,0)
        self.write(arg="Game Over", align="center", font=("Courier", 20, "normal"))

    def get_high_score(self):
        with open("../Snakev2/highscore.txt", mode="r") as file:
            contents = file.read()
            contents = int(contents)
            self.high_score = contents
        self.write_score()

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("./highscore.txt", mode="w") as file:
                file.write(str(self.high_score))

        self.score = 0
        self.write_score()

