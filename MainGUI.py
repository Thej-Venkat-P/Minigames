import sys
import os
from Gamble7.Gamble7 import gamble as gamble_game
from Space_Invaders.SpaceInvader import space_invaders_game
from Snake_Game.SnakeGame import SnakeGame as snake_game

import tkinter as tk
from tkinter import ttk

import mysql.connector

connection = mysql.connector.connect(
    host="localhost", user="root", password="password", database="game_db"
)
cursor = connection.cursor()

BACKGROUND_COLOR = "#cccccc"
LABEL_BACKGROUND_COLOR = "#cccccc"
LABEL_TEXT_COLOR = "#000000"


# Function to execute a query
def execute_query(query):
    print(query)
    cursor.execute(query)
    results = cursor.fetchall()
    # commit the changes
    connection.commit()
    return results


# Gamble_game
def play_gamble_game():
    login_window(main_window, secondary=True)


# Clear the window
def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()
    return window


# Snake_game
def play_snake_game():
    player_score = snake_game(execute_query, current_user)
    return player_score


# Space_invaders
def play_space_invaders_game():
    player_score = space_invaders_game(execute_query, current_user)
    return player_score


# Select Game
def game_selected(game):
    if game == "Gamble":
        play_gamble_game()
    elif game == "Snake Game":
        play_snake_game()
    elif game == "Space Invaders":
        play_space_invaders_game()


# Window to Choose Game
def play_window(window):
    # Create the main window
    root = window
    # Clear the window
    clear_window(root)
    root.title("Game Selection")
    root.geometry("500x500")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")
    style.configure("TLabel", foreground=LABEL_TEXT_COLOR)  # Modify Label's Foreground color

    # Add a header label
    header_label = ttk.Label(
        root,
        text="Choose a Game",
        font=("Arial", 24, "bold"),
        foreground="#ffffff",
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)

    # Create buttons for game selection
    gamble_button = ttk.Button(
        root,
        text="Gamble",
        command=lambda: game_selected("Gamble"),
        width=20,
        style="TButton",
    )
    snake_button = ttk.Button(
        root,
        text="Snake Game",
        command=lambda: game_selected("Snake Game"),
        width=20,
        style="TButton",
    )
    invaders_button = ttk.Button(
        root,
        text="Space Invaders",
        command=lambda: game_selected("Space Invaders"),
        width=20,
        style="TButton",
    )

    # Add buttons to the window
    gamble_button.pack(pady=10)
    snake_button.pack(pady=10)
    invaders_button.pack(pady=10)

    # Add a Check Scores button
    check_scores_button = ttk.Button(
        root,
        text="Check Scores",
        command=lambda: score_window(root),
        width=20,
        style="TButton",
    )
    check_scores_button.pack(pady=20)

    # Add a logout button
    logout_button = ttk.Button(
        root,
        text="Logout",
        command=lambda: login_window(root),
        width=20,
        style="TButton",
    )
    logout_button.pack(pady=10)

    # Start the main event loop
    # root.mainloop()


# Verify Login
def verify_login(window, username, password, secondary=False):
    if username == "ADMIN" and password == "ADMIN":
        admin_window(window)
        return
    query = f"SELECT USER_PASSWORD FROM USERS_LOGIN WHERE USERNAME = '{username}';"
    password_in_db = execute_query(query)
    if password_in_db and password == password_in_db[0][0]:
        if not secondary:
            global current_user, current_password
            current_user = username
            current_password = password
            play_window(window)
        else:
            global secondary_user, secondary_password
            secondary_user = username
            secondary_password = password
            play_window(window)
            if current_user != secondary_user:
                output_gamble = gamble_game(execute_query, current_user, secondary_user)
                if output_gamble:
                    score1, score2 = output_gamble
                query = f"UPDATE GAMBLE_GAME_POINTS SET SCORE = {score1} WHERE USERNAME = '{current_user}';"
                execute_query(query)
                query = f"UPDATE GAMBLE_GAME_POINTS SET SCORE = {score2} WHERE USERNAME = '{secondary_user}';"
                execute_query(query)
            else:
                invalid_login_label = ttk.Label(
                    window,
                    text="Invalid Login",
                    font=("Arial", 12, "bold"),
                    foreground=LABEL_TEXT_COLOR,
                    background=LABEL_BACKGROUND_COLOR,
                )
                invalid_login_label.pack(pady=10)
    else:
        # Create Label Invalid Login
        invalid_login_label = ttk.Label(
            window,
            text="Invalid Login",
            font=("Arial", 12, "bold"),
            foreground=LABEL_TEXT_COLOR,
            background=LABEL_BACKGROUND_COLOR,
        )
        invalid_login_label.pack(pady=10)


# Login Window
def login_window(window, secondary=False):
    root = window
    # Clear the window
    clear_window(root)
    root.title("Login")
    root.geometry("500x500")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")

    # Add a header label
    header_label = ttk.Label(
        root,
        text="Login",
        font=("Arial", 24, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)

    # Add a username label and entry
    username_label = ttk.Label(
        root,
        text="Username",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    username_label.pack(pady=10)
    username_entry = ttk.Entry(root, font=("Arial", 12))
    username_entry.pack(pady=10)

    # Add a password label and entry
    password_label = ttk.Label(
        root,
        text="Password",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    password_label.pack(pady=10)
    password_entry = ttk.Entry(root, font=("Arial", 12), show="*")
    password_entry.pack(pady=10)

    # Add a login button
    login_button = ttk.Button(
        root,
        text="Login",
        command=lambda: verify_login(
            root, username_entry.get(), password_entry.get(), secondary=secondary
        ),
        width=20,
        style="TButton",
    )
    login_button.pack(pady=10)

    # Add a register button
    register_button = ttk.Button(
        root,
        text="Register New User",
        command=lambda: register_window(root),
        width=20,
        style="TButton",
    )
    register_button.pack(pady=10)

    # Add Exit Button
    exit_button = ttk.Button(
        root,
        text="Exit",
        command=lambda: window.destroy(),
        width=20,
        style="TButton",
    )
    exit_button.pack(pady=10)


# Register User
def register_user(window, username, password, phone, email):
    print("Username:", username)
    print("Password:", password)
    print("Phone:", phone)
    print("Email:", email)
    query = f"INSERT INTO USERS_LOGIN (USERNAME, USER_PASSWORD) VALUES ('{username}', '{password}');"
    execute_query(query)
    query = f"INSERT INTO USER_DETAILS (USERNAME, PHONE, EMAIL) VALUES ('{username}', '{phone}', '{email}');"
    execute_query(query)

    # Create Label User Registered
    registered_label = ttk.Label(
        window,
        text="User Registered",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    registered_label.pack(pady=10)


# Register Window
def register_window(window):
    root = window
    # Clear the window
    clear_window(root)
    root.title("Register")
    root.geometry("500x500")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")

    # Add a header label
    header_label = ttk.Label(
        root,
        text="Register",
        font=("Arial", 24, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)

    # Add a username label and entry
    username_label = ttk.Label(
        root,
        text="Username",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    username_label.pack(pady=10)

    username_entry = ttk.Entry(root, font=("Arial", 12))
    username_entry.pack(pady=5)

    # Add a password label and entry
    password_label = ttk.Label(
        root,
        text="Password",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    password_label.pack(pady=10)

    password_entry = ttk.Entry(root, font=("Arial", 12), show="*")
    password_entry.pack(pady=5)

    # Add Phone Number label and entry
    phone_label = ttk.Label(
        root,
        text="Phone Number",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    phone_label.pack(pady=10)

    phone_entry = ttk.Entry(root, font=("Arial", 12))
    phone_entry.pack(pady=5)

    # Add Email label and entry
    email_label = ttk.Label(
        root,
        text="Email",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    email_label.pack(pady=10)

    email_entry = ttk.Entry(root, font=("Arial", 12))
    email_entry.pack(pady=5)

    # Add a register button
    register_button = ttk.Button(
        root,
        text="Register",
        command=lambda: register_user(
            root,
            username_entry.get(),
            password_entry.get(),
            phone_entry.get(),
            email_entry.get(),
        ),
        width=20,
        style="TButton",
    )
    register_button.pack(pady=10)

    # Add a back button
    back_button = ttk.Button(
        root,
        text="Back",
        command=lambda: login_window(root),
        width=20,
        style="TButton",
    )
    back_button.pack(pady=10)


# Scrollable Window for diplaying data
def scrollable_window(window, title, data, back_window=None):
    clear_window(window)
    root = window
    root.title(title)
    root.geometry("500x500")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")

    # Add a header label
    header_label = ttk.Label(
        root,
        text=title,
        font=("Arial", 24, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)

    # Add a Scrollable Frame to print each row of data
    canvas = tk.Canvas(root, bg=LABEL_BACKGROUND_COLOR)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    frame = ttk.Frame(canvas, style="TButton")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    for row in data:
        row_label = ttk.Label(
            frame,
            text=row,
            font=("Arial", 12, "bold"),
            foreground=LABEL_TEXT_COLOR,
            background=LABEL_BACKGROUND_COLOR,
        )
        row_label.pack(pady=10)

    if not back_window:
        back_window = score_window
    
    # Add a back button
    back_button = ttk.Button(
        root,
        text="Back",
        command=lambda: back_window(root),
        width=20,
        style="TButton",
    )
    back_button.pack(pady=10)


# Score Window
def score_window(root):
    clear_window(root)
    root.title("Scores")
    root.geometry("500x500")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")

    # Add a header label
    header_label = ttk.Label(
        root,
        text="Scores",
        font=("Arial", 24, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)

    # Add a score button
    score_button = ttk.Button(
        root,
        text="Gamble Game",
        command=lambda: gamble_game_scores_window(root),
        width=20,
        style="TButton",
    )
    score_button.pack(pady=10)

    # Add a score button
    score_button = ttk.Button(
        root,
        text="Snake Game",
        command=lambda: snake_game_scores_window(root),
        width=20,
        style="TButton",
    )
    score_button.pack(pady=10)

    # Add a score button
    score_button = ttk.Button(
        root,
        text="Space Invaders",
        command=lambda: space_invaders_game_scores_window(root),
        width=20,
        style="TButton",
    )
    score_button.pack(pady=10)

    # Add a back button
    back_button = ttk.Button(
        root,
        text="Back",
        command=lambda: play_window(root),
        width=20,
        style="TButton",
    )
    back_button.pack(pady=10)


# Gamble Game Scores Window
def gamble_game_scores_window(window):
    clear_window(window)
    root = window
    root.title("Gamble Game Scores")
    root.geometry("500x500")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")

    # Add a header label
    header_label = ttk.Label(
        root,
        text="Gamble Game Scores",
        font=("Arial", 24, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)

    # Select all gamble scores from the database user current_user
    def all_gamble_scores():
        query = f"SELECT * FROM GAMBLE_GAME_POINTS;"
        results = execute_query(query)
        scrollable_window(root, "Gamble Game Scores", results)

    all_gamble_scores_button = ttk.Button(
        root,
        text="All Gamble Scores",
        command=all_gamble_scores,
        width=20,
        style="TButton",
    )
    all_gamble_scores_button.pack(pady=10)

    # Select all gambles scores of current_user from the database
    def my_gamble_scores():
        query = f"""SELECT USER1, USER2, GAMBLE FROM GAMBLE_GAME_GAMBLES WHERE USER1 = '{current_user}'
                    UNION
                    SELECT USER2, USER1, -GAMBLE AS GAMBLE FROM GAMBLE_GAME_GAMBLES WHERE USER2 = '{current_user}';"""
        results = execute_query(query)
        scrollable_window(root, "Gamble Game Gambles", results)

    my_gamble_scores_button = ttk.Button(
        root,
        text="My Gamble Scores",
        command=my_gamble_scores,
        width=20,
        style="TButton",
    )
    my_gamble_scores_button.pack(pady=10)

    # Add a back button
    back_button = ttk.Button(
        root,
        text="Back",
        command=lambda: score_window(root),
        width=20,
        style="TButton",
    )
    back_button.pack(pady=10)


# Snake Game Scores Window
def snake_game_scores_window(window):
    clear_window(window)
    root = window
    root.title("Snake Game Scores")
    root.geometry("500x500")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")

    # Add a header label
    header_label = ttk.Label(
        root,
        text="Snake Game Scores",
        font=("Arial", 24, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)

    # Select all snake scores from the database
    def all_snake_scores():
        query = f"SELECT USERNAME, SCORE FROM SNAKE_GAME ORDER BY SNAKE_GAME_ID DESC;"
        results = execute_query(query)
        scrollable_window(root, "Snake Game Scores", results)

    all_snake_scores_button = ttk.Button(
        root,
        text="All Snake Game Scores",
        command=all_snake_scores,
        width=20,
        style="TButton",
    )
    all_snake_scores_button.pack(pady=10)

    # Snake Scores of current_user
    def my_snake_scores():
        query = f"SELECT USERNAME, SCORE FROM SNAKE_GAME WHERE USERNAME = '{current_user}' ORDER BY SCORE DESC;"
        results = execute_query(query)
        scrollable_window(root, "Snake Game Scores", results)

    my_snake_scores_button = ttk.Button(
        root,
        text="My Snake Game Scores",
        command=my_snake_scores,
        width=20,
        style="TButton",
    )
    my_snake_scores_button.pack(pady=10)

    # High Scores of Snake Game
    def high_snake_scores():
        query = f"SELECT USERNAME, SCORE FROM SNAKE_GAME ORDER BY SCORE DESC;"
        results = execute_query(query)
        scrollable_window(root, "Snake Game High Scores", results)

    high_snake_scores_button = ttk.Button(
        root,
        text="High Snake Game Scores",
        command=high_snake_scores,
        width=20,
        style="TButton",
    )
    high_snake_scores_button.pack(pady=10)

    # High Scores of Each User in Snake Game
    def high_snake_scores_user():
        query = f"SELECT USERNAME, MAX(SCORE) as PERSONAL_HIGH FROM SNAKE_GAME GROUP BY USERNAME;"
        results = execute_query(query)
        scrollable_window(root, "Snake Game High Scores", results)

    high_snake_scores_user_button = ttk.Button(
        root,
        text="Highscore of Each User in Snake Game",
        command=high_snake_scores_user,
        width=20,
        style="TButton",
    )
    high_snake_scores_user_button.pack(pady=10)

    # Add a back button
    back_button = ttk.Button(
        root,
        text="Back",
        command=lambda: score_window(root),
        width=20,
        style="TButton",
    )
    back_button.pack(pady=10)

# Space Invaders Game Scores Window
def space_invaders_game_scores_window(window):
    clear_window(window)
    root = window
    root.title("Space Invaders Game Scores")
    root.geometry("500x500")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")

    # Add a header label
    header_label = ttk.Label(
        root,
        text="Space Invaders Game Scores",
        font=("Arial", 24, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)

    # Select all space invaders scores from the database
    def all_space_invaders_scores():
        query = f"SELECT USERNAME, SCORE FROM SPACE_INVADERS_GAME ORDER BY SPACE_INVADERS_GAME_ID DESC;"
        results = execute_query(query)
        scrollable_window(root, "Space Invaders Game Scores", results)

    all_space_invaders_scores_button = ttk.Button(
        root,
        text="All Space Invaders Scores",
        command=all_space_invaders_scores,
        width=20,
        style="TButton",
    )
    all_space_invaders_scores_button.pack(pady=10)

    # Space Invaders Scores of current_user
    def my_space_invaders_scores():
        query = f"SELECT USERNAME, SCORE FROM SPACE_INVADERS_GAME WHERE USERNAME = '{current_user}' ORDER BY SCORE DESC;"
        results = execute_query(query)
        scrollable_window(root, "Space Invaders Game Scores", results)

    my_space_invaders_scores_button = ttk.Button(
        root,
        text="My Space Invaders Scores",
        command=my_space_invaders_scores,
        width=20,
        style="TButton",
    )
    my_space_invaders_scores_button.pack(pady=10)

    # High Scores of Space Invaders Game
    def high_space_invaders_scores():
        query = f"SELECT USERNAME, SCORE FROM SPACE_INVADERS_GAME ORDER BY SCORE DESC;"
        results = execute_query(query)
        scrollable_window(root, "Space Invaders Game High Scores", results)

    high_space_invaders_scores_button = ttk.Button(
        root,
        text="High Space Invaders Scores",
        command=high_space_invaders_scores,
        width=20,
        style="TButton",
    )
    high_space_invaders_scores_button.pack(pady=10)

    # High Scores of Each User in Space Invaders Game
    def high_space_invaders_scores_user():
        query = f"SELECT USERNAME, MAX(SCORE) as PERSONAL_HIGH FROM SPACE_INVADERS_GAME GROUP BY USERNAME;"
        results = execute_query(query)
        scrollable_window(root, "Space Invaders Game High Scores", results)

    high_space_invaders_scores_user_button = ttk.Button(
        root,
        text="Highscore of Each User in Space Invaders Game",
        command=high_space_invaders_scores_user,
        width=20,
        style="TButton",
    )
    high_space_invaders_scores_user_button.pack(pady=10)

    # Add a back button
    back_button = ttk.Button(
        root,
        text="Back",
        command=lambda: score_window(root),
        width=20,
        style="TButton",
    )
    back_button.pack(pady=10)


# Admin Window
def admin_window(window):
    clear_window(window)    
    root = window
    root.title("Admin")
    root.geometry("500x500")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")
    
    # Add a header label
    header_label = ttk.Label(
        root,
        text="Admin",
        font=("Arial", 24, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)
    
    # Button to view all users
    all_users_button = ttk.Button(
        root,
        text="View All Users",
        command=lambda: scrollable_window(root, "All Users", execute_query("SELECT * FROM USERS_INFO;"), back_window=admin_window),
        width=20,
        style="TButton",
    )
    all_users_button.pack(pady=10)
    
    # Delete a user
    delete_user_button = ttk.Button(
        root,
        text="Delete User",
        command=lambda: delete_user_window(root),
        width=20,
        style="TButton",
    )
    delete_user_button.pack(pady=10)
    
    # Update user details
    update_user_button = ttk.Button(
        root,
        text="Update User",
        command=lambda: update_user_window(root),
        width=20,
        style="TButton",
    )
    update_user_button.pack(pady=10)
    
    # Find users who never played a game
    no_users_query = """
    SELECT USERNAME 
    FROM USERS_LOGIN 
    WHERE USERNAME NOT IN (
            SELECT USERNAME FROM SNAKE_GAME
        ) AND
        USERNAME NOT IN (
            SELECT USERNAME FROM SPACE_INVADERS_GAME
        ) AND
        USERNAME NOT IN (
            SELECT USER1 FROM GAMBLE_GAME_GAMBLES
        ) AND
        USERNAME NOT IN (
            SELECT USER2 FROM GAMBLE_GAME_GAMBLES
        );
    ;"""
    no_game_users_button = ttk.Button(
        root,
        text="Users who never played a game",
        command=lambda: scrollable_window(root, "Users who never played a game", execute_query(no_users_query), back_window = admin_window),
        width=20,
        style="TButton",
    )
    no_game_users_button.pack(pady=10)
    
    # Add a back button
    back_button = ttk.Button(
        root,
        text="Back",
        command=lambda: login_window(root),
        width=20,
        style="TButton",
    )
    back_button.pack(pady=10)


# Delete User Window
def delete_user_window(window):
    clear_window(window)
    root = window
    root.title("Delete User")
    root.geometry("500x600")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")

    # Add a header label
    header_label = ttk.Label(
        root,
        text="Delete User",
        font=("Arial", 24, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)

    # Add a username label and entry
    username_label = ttk.Label(
        root,
        text="Username",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    username_label.pack(pady=10)
    username_entry = ttk.Entry(root, font=("Arial", 12))
    username_entry.pack(pady=10)

    # Add a Find Details button
    find_details_button = ttk.Button(
        root,
        text="Find Details",
        command=lambda: find_user_details(username_entry.get()),
        width=20,
        style="TButton",
    )
    find_details_button.pack(pady=10)

    # Password Label
    password_label = ttk.Label(
        root,
        text="Password: ",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    password_label.pack(pady=10)

    # Phone Label
    phone_label = ttk.Label(
        root,
        text="Phone: ",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    phone_label.pack(pady=10)

    # Email Label
    email_label = ttk.Label(
        root,
        text="Email: ",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    email_label.pack(pady=10)

    # Find Details Function
    def find_user_details(username):
        query = f"SELECT * FROM USER_INFO WHERE USERNAME = '{username}';"
        results = execute_query(query)
        if results:
            password_label.config(text="Password: " + results[0][1])
            phone_label.config(text="Phone: " + results[0][2])
            email_label.config(text="Email: " + results[0][3])
        else:
            password_label.config(text="Password: ")
            phone_label.config(text="Phone: ")
            email_label.config(text="Email: ")

    # Add a Delete User button
    delete_user_button = ttk.Button(
        root,
        text="Delete User",
        command=lambda: execute_query(f"DELETE FROM USERS_LOGIN WHERE USERNAME = '{username_entry.get()}';"),
        width=20,
        style="TButton",
    )
    delete_user_button.pack(pady=10)

    # Add a back button
    back_button = ttk.Button(
        root,
        text="Back",
        command=lambda: admin_window(root),
        width=20,
        style="TButton",
    )
    back_button.pack(pady=10)    


# Update User Window
def update_user_window(window):
    clear_window(window)
    root = window
    root.title("Update User")
    root.geometry("500x600")  # Set the window size
    root.configure(bg=BACKGROUND_COLOR)  # Set the background color
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), foreground="#000000")
    
    # Update User Function
    def update_user(username, password, phone, email):
        query = f"CALL UpdateUserDetails('{username}', '{password}', '{phone}', '{email}');"
        execute_query(query)

    # Find User Details Function
    def find_user_details(username):
        query = f"SELECT USER_PASSWORD, PHONE, EMAIL FROM USERS_INFO WHERE USERNAME = '{username}';"
        result = execute_query(query)
        if result:
            password_label.config(text="Password: " + result[0][0])
            phone_label.config(text="Phone: " + result[0][1])
            email_label.config(text="Email: " + result[0][2])
        else:
            password_label.config(text="Password: ")
            phone_label.config(text="Phone: ")
            email_label.config(text="Email: ")

    # Add a header label
    header_label = ttk.Label(
        root,
        text="Update User",
        font=("Arial", 24, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    header_label.pack(pady=20)

    # Add a username label and entry
    username_label = ttk.Label(
        root,
        text="Username",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    username_label.pack(pady=10)
    username_entry = ttk.Entry(root, font=("Arial", 12))
    username_entry.pack(pady=10)

    # Add a Find Details button
    find_details_button = ttk.Button(
        root,
        text="Find Details",
        command=lambda: find_user_details(username_entry.get()),
        width=20,
        style="TButton",
    )
    find_details_button.pack(pady=10)

    # Password Label
    password_label = ttk.Label(
        root,
        text="Password: ",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    password_label.pack(pady=10)
    # Password Entry
    password_entry = ttk.Entry(root, font=("Arial", 12))
    password_entry.pack(pady=10)
    
    # Phone Label
    phone_label = ttk.Label(
        root,
        text="Phone: ",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    phone_label.pack(pady=10)
    # Phone Entry
    phone_entry = ttk.Entry(root, font=("Arial", 12))
    phone_entry.pack(pady=10)
    
    # Email Label
    email_label = ttk.Label(
        root,
        text="Email: ",
        font=("Arial", 12, "bold"),
        foreground=LABEL_TEXT_COLOR,
        background=LABEL_BACKGROUND_COLOR,
    )
    email_label.pack(pady=10)
    # Email Entry
    email_entry = ttk.Entry(root, font=("Arial", 12))
    email_entry.pack(pady=10)
    
    # Add a Update User button
    update_user_button = ttk.Button(
        root,
        text="Update User",
        command=lambda: update_user(username_entry.get(), password_entry.get(), phone_entry.get(), email_entry.get()),
        width=20,
        style="TButton",
    )
    update_user_button.pack(pady=10)

    # Add a back button
    back_button = ttk.Button(
        root,
        text="Back",
        command=lambda: admin_window(root),
        width=20,
        style="TButton",
    )
    back_button.pack(pady=10)


main_window = tk.Tk()
login_window(main_window)
main_window.mainloop()
print("Exiting...")
cursor.close()
connection.close()
sys.exit(0)


