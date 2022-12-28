import pyautogui
import time

pyautogui.moveTo(650, 825, duration=0.25)
time.sleep(0.5)

for i in range(10):
    # pyautogui.drag(620, 0, 1.5, button='left')
    # pyautogui.move(-620, -18, 0)
    pyautogui.drag(0, -600, 1.5, button='left')
    pyautogui.move(18, 600, 0)
