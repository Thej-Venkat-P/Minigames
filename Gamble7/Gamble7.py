# Basic Idea:
"""
Two players play a game of Chance.
Each player has their own points, and they can bet a certain amount of points.
The probability of winning the game depends on the amount of points bet.
"""

import random
import tkinter as tk


class Gamble7:
    def __init__(
        self,
        window: tk.Tk,
        player1_name: str,
        player2_name: str,
        player1_points: int,
        player2_points: int,
        query_func=None
    ):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = player1_points
        self.player2_points = player2_points
        self.player1_bet_amount = 0
        self.player2_bet_amount = 0

        self.window = window
        self.window.title("Gamble7")
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        # Displaying the players' names and points
        self.player1_name_label = tk.Label(
            self.window, text=self.player1_name, font=("Arial", 20)
        )
        self.player1_name_label.place(x=50, y=50)
        self.player1_points_label = tk.Label(
            self.window, text=self.player1_points, font=("Arial", 20)
        )
        self.player1_points_label.place(x=50, y=100)
        self.player2_name_label = tk.Label(
            self.window, text=self.player2_name, font=("Arial", 20)
        )
        self.player2_name_label.place(x=50, y=450)
        self.player2_points_label = tk.Label(
            self.window, text=self.player2_points, font=("Arial", 20)
        )
        self.player2_points_label.place(x=50, y=500)

        # Displaying the bet entry
        self.bet_entry1 = tk.Entry(self.window, font=("Arial", 20))
        self.bet_entry1.place(x=50, y=250)
        self.bet_entry2 = tk.Entry(self.window, font=("Arial", 20))
        self.bet_entry2.place(x=50, y=350)

        # Displaying the bet button
        self.bet_button1 = tk.Button(
            self.window, text="Bet", font=("Arial", 20), command=self.bet1
        )
        self.bet_button1.place(x=300, y=250)
        self.bet_button2 = tk.Button(
            self.window, text="Bet", font=("Arial", 20), command=self.bet2
        )
        self.bet_button2.place(x=300, y=350)

        # Displaying the bet amount
        self.bet_amount_display1 = tk.Label(
            self.window, text=self.player1_bet_amount, font=("Arial", 20)
        )
        self.bet_amount_display1.place(x=450, y=250)
        self.bet_amount_display2 = tk.Label(
            self.window, text=self.player2_bet_amount, font=("Arial", 20)
        )
        self.bet_amount_display2.place(x=450, y=350)

        # Displaying the play button
        self.play_button = tk.Button(
            self.window, text="Play", font=("Arial", 20), command=self.play
        )
        self.play_button.place(x=600, y=250)
        self.query_func = query_func
        self.window.mainloop()

    def bet1(self):
        bet = int(self.bet_entry1.get())
        if bet > self.player1_points or bet < 0:
            return "Invalid bet"
        self.player1_bet_amount = bet
        self.bet_amount_display1.config(text=self.player1_bet_amount)

    def bet2(self):
        bet = int(self.bet_entry2.get())
        if bet > self.player2_points or bet < 0:
            return "Invalid bet"
        self.player2_bet_amount = bet
        self.bet_amount_display2.config(text=self.player2_bet_amount)

    def play(self):
        if self.player1_bet_amount == 0 or self.player2_bet_amount == 0:
            return "Invalid play"
        self.player1_points -= self.player1_bet_amount
        self.player2_points -= self.player2_bet_amount
        total = self.player1_bet_amount + self.player2_bet_amount
        result = random.randrange(0, total)
        if result < self.player1_bet_amount:
            if self.query_func:
                query = f"INSERT INTO GAMBLE_GAME_GAMBLES (USER1, USER2, SCORE1, SCORE2, GAMBLE) VALUES ('{self.player1_name}', '{self.player2_name}', {self.player1_points}, {self.player2_points}, {total})"
                self.query_func(query)
            self.player1_points += total
            self.update_values()
            return self.player1_name + " wins " + str(total)
        else:
            if self.query_func:
                query = f"INSERT INTO GAMBLE_GAME_GAMBLES (USER1, USER2, SCORE1, SCORE2, GAMBLE) VALUES ('{self.player2_name}', '{self.player1_name}', {self.player2_points}, {self.player1_points}, {total})"
                self.query_func(query)
            self.player2_points += total
            self.update_values()
            return self.player2_name + " wins " + str(total)

    def update_values(self):
        # Updating the label values
        self.player1_points_label.config(text=self.player1_points)
        self.player2_points_label.config(text=self.player2_points)
        self.player1_bet_amount = 0
        self.player2_bet_amount = 0
        self.bet_amount_display1.config(text=self.player1_bet_amount)
        self.bet_amount_display2.config(text=self.player2_bet_amount)


def gamble(query_func=None, user1=None, user2=None):
    if (user1 or user2) and user1 == user2:
        return None
    if query_func:
        root = tk.Tk()
        query = f"SELECT SCORE FROM GAMBLE_GAME_POINTS WHERE USERNAME = '{user1}';"
        user1_points = query_func(query)
        if not user1_points:
            query = (
                f"INSERT INTO GAMBLE_GAME_POINTS (USERNAME, SCORE) VALUES ('{user1}', 100);"
            )
            query_func(query)
            user1_points = [[100]]
        user1_points = user1_points[0][0]
        if user1_points == 0:
            query = f"UPDATE GAMBLE_GAME_POINTS SET SCORE = 50 WHERE USERNAME = '{user1}' ;"
            query_func(query)
            user1_points = 50
            
        query = f"SELECT SCORE FROM GAMBLE_GAME_POINTS WHERE USERNAME = '{user2}';"
        user2_points = query_func(query)
        if not user2_points:
            query = (
                f"INSERT INTO GAMBLE_GAME_POINTS (USERNAME, SCORE) VALUES ('{user2}', 100);"
            )
            query_func(query)
            user2_points = [[100]]
        user2_points = user2_points[0][0]
        if user2_points == 0:
            query = f"UPDATE GAMBLE_GAME_POINTS SET SCORE = 50 WHERE USERNAME = '{user2}' ;"
            query_func(query)
            user2_points = 50

        game = Gamble7(root, user1, user2, user1_points, user2_points, query_func)
        return game.player1_points, game.player2_points
    else:
        root = tk.Tk()
        game = Gamble7(root, "Player1", "Player2", 100, 100)
        return game.player1_points, game.player2_points

if __name__ == "__main__":
    gamble()
