from ai import *
from helper import *
#import random (needed for it to play against a prng if necessary)

def number_of_games():
    """
    Asks user for number of games to be played
    """
    while True:
        games = input("Enter the number of games you wish to play: ")
        try:
            games = int(games)
            return games

        except ValueError:
            print("Wrong input. Please enter an integer only.")
            pass


def get_input():
    """
    Gets an input from the user.
    """
    while True:
        choice = input("Enter your choice: [Rock (R), Paper (P), Scissor (S)]\n> ")
        choice = choice.strip().lower()

        if choice not in ["rock", "paper", "scissor", "r", "p", "s"]:
            print("Wrong input. Please enter from the options only.")
        else:
            break

    if choice in ["rock", "r"]:
        return "r"
    elif choice in ["paper", "p"]:
        return "p"
    else:
        return "s"

def current_round():
    """
    Provides the data for the current round.
    """
    ai_choice = choose_model()
    choice = get_input()
    #choice = random.choice(["r", "p", "s"])

    print(f"User - {return_choice(choice)} : {return_choice(ai_choice)} - Computer")

    current = declare_winner(choice, ai_choice)
    rate_all_models(choice)

    if current != "Draw":
        print(f"This round has been won by {current}.")
    else:
        print(f"This round is a draw.")

    tally_scores(current)

#__main__
print("Rock, Paper, Scissor game")
#win_percentages = []
clean_logs()
total_games = number_of_games()
for i in range(total_games):
    current_round()
final_score()
find_ai_accuracy(total_games)


