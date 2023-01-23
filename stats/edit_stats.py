import json


# Functions will raise errors when the wrong type of data is passed in
# Opens a file, modifies the data, then saves the file

# Reset the stats
def reset() -> None:
    with open("stats/stats.json") as file:
        data = json.load(file)

    # Set each value to 0
    for key in data:
        data[key] = 0

    with open("stats/stats.json", "w") as file:
        json.dump(data, file, indent=4)


# Add a win to the stats
def add_win() -> None:
    with open("stats/stats.json") as file:
        data = json.load(file)

    data["wins"] += 1
    data["games_played"] += 1
    data["win-rate"] = data["wins"] / data["games_played"]

    with open("stats/stats.json", "w") as file:
        json.dump(data, file, indent=4)


# Add a loss to the stats
def add_loss() -> None:
    with open("stats/stats.json") as file:
        data = json.load(file)

    data["losses"] += 1
    data["games_played"] += 1
    data["win-rate"] = data["wins"] / data["games_played"]

    with open("stats/stats.json", "w") as file:
        json.dump(data, file, indent=4)


def add_tie() -> None:
    with open("stats/stats.json") as file:
        data = json.load(file)

    data["ties"] += 1
    data["games_played"] += 1
    data["win-rate"] = data["wins"] / data["games_played"]

    with open("stats/stats.json", "w") as file:
        json.dump(data, file, indent=4)


# Add time in seconds
def add_time(time: int) -> None:
    if type(time) != int:
        raise TypeError("Time must be an integer.")
    elif time < 0:
        raise ValueError("Time must be a positive integer.")

    with open("stats/stats.json") as file:
        data = json.load(file)

    data["total_time"] += time

    with open("stats/stats.json", "w") as file:
        json.dump(data, file, indent=4)
