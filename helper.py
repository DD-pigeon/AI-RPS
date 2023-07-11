import json

number_of_models = 6


def read_data(flag):
    """
    Reading and unpacking the data from the json file
    """
    with open("logs.json", "r") as fp:
        data = json.load(fp)

    model_data = [data[str(i)] for i in range(1, number_of_models + 1)]

    choices = data["Choices"]

    last = data["Last"]

    if flag == 1:
        return last
    
    if flag == 2:
        return model_data
    
    if flag == 3:
        return choices
    
def declare_winner(player, comp):
    """
    Compares the choices, and finds a winner.
    """
    choice = player + comp

    combinations = {
        "rp" : "Computer",
        "ps" : "Computer",
        "sr" : "Computer",
        "rs" : "Player",
        "pr" : "Player",
        "sp" : "Player"
    }

    try:
        winner = combinations[choice]
    except KeyError:
        winner = "Draw"

    return winner

def final_score():
    with open('logs.json', 'r') as fp:
        data = json.load(fp)

    pscore, cscore = data["Player"], data["Computer"]

    if pscore > cscore:
        print("Player wins!")
    elif cscore > pscore:
        print("Computer wins!")
    else:
        print("The game has ended in a tie.")

def clean_logs():
    """
    Cleans the logs file before the start of the game.
    """
    try:
        with open("logs.json", "r") as fp:
            data = json.load(fp)

    except FileNotFoundError:
        data = {"Choices": []}
        fp = open("logs.json", "a")
        json.dump(data, fp, indent= 2)
        fp.close()

    
    try:
        last_played = data["Choices"][-1]
    except IndexError:
        last_played = "r"

    new_data = {
        "Choices": [],
        "Player": 0,
        "Computer": 0,
        "Round": 0,
        "Last": last_played
    }

    for i in range(1, number_of_models + 1):
        new_data[str(i)] = []

    with open("logs.json", "w") as f:
        json.dump(new_data, f, indent = 2)

    print("Data cleaned.")

def return_choice(choice):
    """
    Returns the value from the input key choice. 
    """
    if choice == "r":
        return "Rock"
    elif choice == "s":
        return "Scissor"
    else:
        return "Paper"

def tally_scores(winner):
    """
    Updates scores post round.
    """
    with open("logs.json", "r") as fp:
        data = json.load(fp)

    if winner == "Computer":
        data["Computer"] += 1
    elif winner == "Player":
        data["Player"] += 1
    
    with open("logs.json", "w") as f:
        json.dump(data, f, indent = 2)

    print(f"Score:\nPlayer {data['Player']} - {data['Computer']} Computer")

def find_ai_accuracy(games):
    """
    Finds the ending accuracy of the AI model, given number of games
    """
    with open("logs.json", "r") as fp:
        data = json.load(fp)

    model_accuracy = round(((data["Computer"]/games) * 100), 2)

    print(f"Final model accuracy: {model_accuracy}%")

    return model_accuracy / 100
