import json
from helper import *
import random

def winner(choice):
    """
    Defining the winner based on the choice
    """
    if choice == "r":
        return "p"
    elif choice == "p":
        return "s"
    else:
        return "r"

def models(model_number, choices = None):

    if model_number == 1:
        """
        Model 1
        Predicting the output based on the user's last round choice
        """
        if not choices:
            return winner(winner(read_data(1)))
        else:
            return winner(read_data(1))
    
    if model_number == 2:
        """
        Model 2
        Move based on the last 3 rounds
        """
        try:
            r1, r2, r3 = choices[-3], choices[-2], choices[-1]

            if (r1 == r2) and (r2 == r3):
                return winner(r1)
            elif (r1 == r2):
                return winner(r1)
            elif (r1 == r3):
                return winner(r2)
            elif (r2 == r3):
                return winner(r2)
            else:
                return winner(r1)
        except:
            try:
                r1, r2 = choices[-2], choices[-1]

                if (r1 == r2):
                    return winner(r1)
                else:
                    return winner(r2)
            except:
                return models(1, choices)
        
    if model_number == 3:
        """
        Model 3
        Most commonly used choice
        """
        rc, sc, pc = choices.count("r"), choices.count("p"), choices.count("s")
    
        if (rc > sc and rc > pc):
            return "p"
        elif (sc > pc and sc > rc):
            return "r"
        else:
            return "s"
    
    if model_number == 4:
        """
        Model 4
        Least commonly used choice
        """
        rc, sc, pc = choices.count("r"), choices.count("p"), choices.count("s")
    
        if (rc < sc and rc < pc):
            return "p"
        elif (sc < pc and sc < rc):
            return "r"
        else:
            return "s"

    if model_number == 5:
        """
        Model 5
        random
        """
        return random.choice(["r", "p", "s"])

    if model_number == 6:
        """
        Model 6
        Most common choice which succeeds the last two choices you used
        """
        if len(choices) < 3:
            return random.choice(["r", "p", "s"])

        else: #this could be made way more efficient, but will suffice for now, O(n)
            last_choices_dict = {
                'rr': {'r': 0, 'p': 0, 's': 0},
                'rp': {'r': 0, 'p': 0, 's': 0},
                'rs': {'r': 0, 'p': 0, 's': 0},
                'pr': {'r': 0, 'p': 0, 's': 0},
                'pp': {'r': 0, 'p': 0, 's': 0},
                'ps': {'r': 0, 'p': 0, 's': 0},
                'sr': {'r': 0, 'p': 0, 's': 0},
                'sp': {'r': 0, 'p': 0, 's': 0},
                'ss': {'r': 0, 'p': 0, 's': 0}
                }

        for c in range(len(choices) - 2):
            last_2_choices = choices[c+1] + choices[c]
            last_choices_dict[last_2_choices][choices[c+2]] += 1

        current_last_2 = choices[-2] + choices[-1]
        m6choice = max(last_choices_dict[current_last_2], key = lambda x: last_choices_dict[current_last_2][x])
        # ^ finds key correspoding to max value in dict
        return m6choice


def calc_score(record):
    """
    Calculates score for the model
    """
    numerator = 0
    denominator = 0
    for i in range(len(record)):
        numerator += (record[i] * (i ** 2))
        denominator += (i ** 2)
    try:
        score = numerator / denominator
    except ZeroDivisionError:
        score = 0
    return score


def choose_model():
    """
    Chooses the model based on the score
    """
    datalist = read_data(2)
    #print(datalist)  //very useful for debugging

    if not datalist:
        return models(1)
    else:
        scores = [calc_score(i) for i in datalist]

        max_score = scores.index(max(scores))
        record = read_data(3)

        return models(max_score + 1, record)


def rate_all_models(user):
    """
    Rates all the models based on the output it predicted.
    """
    data = read_data(3)
    model_choices = [models(i, data) for i in range(1, number_of_models + 1)]
    winners = [declare_winner(user, model_choices[i - 1]) for i in range(1, number_of_models + 1)]
    datalist = read_data(2)

    for i in range(len(winners)):
        if winners[i] == "Player":
            datalist[i].append(-1)
        if winners[i] == "Computer":
            datalist[i].append(1)
        if winners[i] == "Draw":
            datalist[i].append(0)

    with open("logs.json", "r") as fp:
        data = json.load(fp)

    if data["Round"] == 1:
        data["1"] = datalist[0]
        for i in range(2, number_of_models + 1):
            data[str(i)] = [0]
    else:
        for i in range(len(datalist)):
            data[str(i+1)] = list(datalist[i])

    data["Choices"].append(user)
    data["Last"] = user
    data["Round"] += 1

    with open("logs.json", "w") as f:
        json.dump(data, f, indent = 2)


