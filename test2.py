# Resize all files in cards to 150 width
from PIL import Image

suits = ["diamonds", "clubs", "hearts", "spades"]
values = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]

for i in range(13):
    for j in range(4):
        im = Image.open(f"./cards/{values[i]}_of_{suits[j]}.png")
        im.thumbnail((150, 225))
        im.save(f"./cards/{values[i]}_of_{suits[j]}.png")
