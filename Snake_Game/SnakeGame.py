from tkinter import *
import random


# Snake-Game Code


def SnakeGame(query_func=None, user=None):
    GameWidth = 500
    GameHeight = 500
    GameSpeed = 100
    GameObjectSize = 25
    SnakeBodyParts = 4
    SnakeColour = "#FF0099"
    FoodColour = "#FF0000"
    BackgroundColour = "#000000"

    class Snake:
        def __init__(self):
            self.bodySize = SnakeBodyParts
            self.direction = "right"
            self.coordinates = []
            self.squares = []

            for i in range(self.bodySize):
                self.coordinates.append([0, 0])

            for x, y in self.coordinates:
                square = canvas.create_rectangle(
                    x,
                    y,
                    x + GameObjectSize,
                    y + GameObjectSize,
                    fill=SnakeColour,
                    tag="snake",
                )
                self.squares.append(square)

    class Food:
        def __init__(self):
            x = GameObjectSize * random.randrange(GameWidth // GameObjectSize)
            y = GameObjectSize * random.randrange(GameHeight // GameObjectSize)
            self.coordinates = [x, y]
            canvas.create_oval(
                x,
                y,
                x + GameObjectSize,
                y + GameObjectSize,
                fill=FoodColour,
                tag="food",
            )

    def next_turn(snake, food):
        x, y = snake.coordinates[0]
        direction = snake.direction
        if direction == "left":
            x -= GameObjectSize
        elif direction == "right":
            x += GameObjectSize
        elif direction == "up":
            y -= GameObjectSize
        elif direction == "down":
            y += GameObjectSize
        snake.coordinates.insert(0, [x, y])
        square = canvas.create_rectangle(
            x, y, x + GameObjectSize, y + GameObjectSize, fill=SnakeColour, tag="snake"
        )
        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            nonlocal score
            score += 1
            label.config(text="Score : {}".format(score))
            canvas.delete("food")
            food = Food()
        else:
            snake.coordinates.pop()
            canvas.delete(snake.squares.pop())

        if check_collision(snake):
            game_over()
        else:
            window.after(GameSpeed, next_turn, snake, food)

    def change_direction(snake, new_direction):
        direction = snake.direction
        if new_direction == "right":
            if direction != "left":
                direction = "right"
        elif new_direction == "left":
            if direction != "right":
                direction = "left"
        elif new_direction == "up":
            if direction != "down":
                direction = "up"
        elif new_direction == "down":
            if direction != "up":
                direction = "down"
        snake.direction = direction

    def check_collision(snake):
        x, y = snake.coordinates[0]
        if x < 0 or x >= GameWidth or y < 0 or y >= GameHeight:
            return True
        for xc, yc in snake.coordinates[1:]:
            if x == xc and y == yc:
                print("Collision")
                return True
        return False

    def game_over():
        canvas.delete(ALL)
        canvas.create_text(
            canvas.winfo_width() / 2,
            canvas.winfo_height() / 2,
            font=("aria", GameObjectSize),
            text="GAME OVER",
            fill="red",
            tag="gameover",
        )

    window = Tk()
    window.title("Snake game")
    window.resizable(False, False)

    score = 0

    label = Label(window, text="Score:{}".format(score), font=("aria", GameObjectSize))
    label.pack()

    canvas = Canvas(window, bg=BackgroundColour, height=GameHeight, width=GameWidth)
    canvas.pack()

    window.update()

    WindowWidth = window.winfo_width()
    WindowHeight = window.winfo_height()
    ScreenWidth = window.winfo_screenwidth()
    ScreenHeight = window.winfo_screenheight()

    xOff = int(ScreenWidth / 2 - WindowWidth / 2)
    yOff = int(ScreenHeight / 2 - WindowHeight / 2)
    window.geometry(f"{WindowWidth}x{WindowHeight}+{xOff}+{yOff}")

    window.bind("a", lambda event: change_direction(snake, "left"))
    window.bind("d", lambda event: change_direction(snake, "right"))
    window.bind("w", lambda event: change_direction(snake, "up"))
    window.bind("s", lambda event: change_direction(snake, "down"))

    snake = Snake()
    food = Food()

    next_turn(snake, food)

    window.mainloop()
    
    if query_func:
        query = f"INSERT INTO SNAKE_GAME (USERNAME, SCORE) VALUES ('{user}', {score});"
        query_func(query)
    
    return score


if __name__ == "__main__":
    print(SnakeGame())
