import json


def reset():
    with open("stats.json") as file:
        data = json.load(file)

    data["games_played"] = 0
    data["wins"] = 0
    data["losses"] = 0
    data["win-rate"] = 0
    data["total_time"] = 0

    with open("stats.json", "w") as file:
        json.dump(data, file, indent=4)


def add_win():
    with open("stats.json") as file:
        data = json.load(file)

    data["wins"] += 1
    data["games_played"] += 1
    data["win-rate"] = data["wins"] / data["games_played"]

    with open("stats.json", "w") as file:
        json.dump(data, file, indent=4)


def add_loss():
    with open("stats.json") as file:
        data = json.load(file)

    data["losses"] += 1
    data["games_played"] += 1
    data["win-rate"] = data["wins"] / data["games_played"]

    with open("stats.json", "w") as file:
        json.dump(data, file, indent=4)


def add_time(time):
    with open("stats.json") as file:
        data = json.load(file)

    data["total_time"] += time

    with open("stats.json", "w") as file:
        json.dump(data, file, indent=4)
