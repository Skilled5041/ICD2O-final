import json


def change_music_volume(volume: float) -> None:
    if type(volume) != float and type(volume) != int:
        raise TypeError("Volume must be a number between 0 and 1.")
    elif volume < 0 or volume > 1:
        raise ValueError("Volume must be between 0 and 1.")

    with open("settings/settings.json") as file:
        data = json.load(file)

    data["music_volume"] = volume

    with open("settings/settings.json", "w") as file:
        json.dump(data, file, indent=4)


def change_sfx_volume(volume: float) -> None:
    if type(volume) != float and type(volume) != int:
        raise TypeError("Volume must be a number between 0 and 1.")
    elif volume < 0 or volume > 1:
        raise ValueError("Volume must be between 0 and 1.")

    with open("settings/settings.json") as file:
        data = json.load(file)

    data["sfx_volume"] = volume

    with open("settings/settings.json", "w") as file:
        json.dump(data, file, indent=4)


def get_music_volume() -> float:
    with open("settings/settings.json") as file:
        data = json.load(file)
    return data["music_volume"]


def get_sfx_volume() -> float:
    with open("settings/settings.json") as file:
        data = json.load(file)
    return data["sfx_volume"]
