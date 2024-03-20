import turtle
import random
import sys

curr_path = r"C:\Users\Thej Venkat\Desktop\Projects\Minigames\Space_Invaders"

def initialize_variables():
    global game_speed_factor, game_over_message, score, SCREEN_WIDTH, SCREEN_HEIGHT, WN, line, Hero_im, bulletim, list_of_enemies, hero, bullet
    # Global Variables
    DIRECTORY_PATH = sys.path[0]
    game_over_message = False
    game_speed_factor = 1
    score = 0
    turtle.title("Space Invaders")
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    turtle.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    WN = turtle.Screen()
    WN.bgcolor("black")
    WN.tracer(0)

    # Drawing the boundary line
    line = turtle.Turtle()
    line.penup()
    line.setx(-(SCREEN_WIDTH / 2))
    line.sety(-(SCREEN_HEIGHT / 2) + 100)
    line.pendown()
    line.pencolor("white")
    line.setx(SCREEN_WIDTH / 2 + 1)
    line.hideturtle()

    # Registering the images
    Hero_im = curr_path + "\\rocket.gif"
    bulletim = curr_path + "\\bullet.gif"
    WN.register_shape(Hero_im)
    WN.register_shape(bulletim)


# Hero Class
class Hero:
    def __init__(self):
        self.hero = turtle.Turtle()
        self.hero.ht()
        self.hero.pu()
        self.hero.sety(-(SCREEN_HEIGHT / 2) + 50)
        self.hero.st()
        self.hero.shape(Hero_im)
        self.hero.left(90)
        self.hero.x = 0
        self.hero.y = -(SCREEN_HEIGHT / 2) + 50

    def move_left(self):
        if self.hero.xcor() >= -(SCREEN_WIDTH / 2) + 20:
            self.hero.x -= 10
            self.hero.setx(self.hero.x)

    def move_right(self):
        if self.hero.xcor() <= (SCREEN_WIDTH / 2) - 20:
            self.hero.x += 10
            self.hero.setx(self.hero.x)

    def shoot(self, bullet: turtle.Turtle):
        if not bullet.running:
            bullet.running = True
            bullet.x = self.hero.xcor()
            bullet.y = self.hero.ycor()
            bullet.bullet.goto(self.hero.pos())
            bullet.bullet.st()


# Bullet Class
class Bullet:
    def __init__(self):
        self.bullet = turtle.Turtle()
        self.bullet.ht()
        self.bullet.shape(bulletim)
        self.bullet.setheading(90)
        self.bullet.pu()
        self.bullet.goto(0, SCREEN_HEIGHT / 2)
        self.x = 0
        self.y = SCREEN_HEIGHT / 2
        self.running = False

    def move(self):
        if self.running is False:
            return False
        if self.y > SCREEN_HEIGHT / 2:
            self.bullet.ht()
            self.running = False
            return False
        else:
            self.bullet.st()
            self.bullet.fd(0.5 * game_speed_factor)
            self.y += 0.5 * game_speed_factor
            return True


# Enemy Class
class Enemy:
    def __init__(self):
        self.enemy = turtle.Turtle()
        self.x = 0
        self.y = 0
        self.enemy.ht()
        self.enemy.penup()
        self.enemy.pu()
        self.enemy.color("red")
        self.enemy.setheading(270)
        self.set_position()
        self.enemy.st()

    def set_position(self):
        self.enemy.ht()
        self.x = random.randint(-(SCREEN_WIDTH / 2) + 20, (SCREEN_WIDTH / 2) - 20)
        self.enemy.setx(self.x)
        self.y = SCREEN_HEIGHT / 2
        self.enemy.sety(self.y)
        self.enemy.st()

    def hit_reg(self, bullet: Bullet):
        if (bullet.y - 10 <= self.y < bullet.y + 11) and (
            bullet.x - 10 <= self.x < bullet.x + 11
        ):
            global score, list_of_enemies, WN, game_speed_factor
            score += 1
            game_speed_factor += 0.05
            if str(score)[-1] in ("0", "5"):
                list_of_enemies.append(Enemy())
                game_speed_factor -= 0.15
            self.enemy.ht()
            self.set_position()
            WN.update()
            return True
        else:
            return False

    def move(self, bullet: Bullet):
        if self.enemy.ycor() < -(SCREEN_HEIGHT / 2) + 100:
            print("Lost")
            game_over()
        else:
            self.enemy.fd(0.1 * game_speed_factor)
            self.y -= 0.1 * game_speed_factor
            self.hit_reg(bullet)
            return True


# Game Over Function
def game_over():
    global score, game_over_message, WN
    try:
        turtle.clearscreen()
    except Exception:
        turtle.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        WN = turtle.Screen()
        turtle.clearscreen()
    turtle.goto(0, 0)
    turtle.write(
        f"Game Over\n  Score: {score}", align="center", font=("Arial", 20, "bold")
    )
    turtle.ht()
    print("Score: ", score)
    turtle.exitonclick()
    game_over_message = True


def spawning():
    global list_of_enemies, hero, bullet
    # Spawning the Game Objects
    hero = Hero()
    bullet = Bullet()
    list_of_enemies = [Enemy()]


def set_keybindings():
    global hero, bullet
    # Setting the Key Bindings
    WN.listen()
    WN.onkeypress(hero.move_right, "d")
    WN.onkeypress(hero.move_left, "a")
    WN.onkeypress(lambda: hero.shoot(bullet), "space")


def game_loop():
    global list_of_enemies, hero, bullet, game_over_message
    # Main Game Loop
    while 1:
        try:
            bullet.move()
            for enemy in list_of_enemies:
                enemy.move(bullet)
            WN.update()

        except Exception as e:
            if not game_over_message:
                game_over()
            break


# Main Game Function
def space_invaders_game(query_func=None, user=None):
    initialize_variables()
    spawning()
    set_keybindings()
    game_loop()
    
    if query_func:
        query = f"INSERT INTO SPACE_INVADERS_GAME (USERNAME, SCORE) VALUES ('{user}', {score});"
        query_func(query)
    
    return score


if __name__ == "__main__":
    space_invaders_game()
