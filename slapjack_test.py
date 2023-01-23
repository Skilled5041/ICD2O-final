from graphics import *
import random
from graphics_elements import Button

def win_window(window):
    window.setBackground(color_rgb(113, 203, 255))
    win_message = Text(Point(600, 200), "Congrats, you won!")
    win_message.setStyle('bold')
    win_message.setSize(36)
    win_message.draw(window)

    new_game_btn = Button(Point(250, 400), Point(450, 500), "New Game")
    new_game_btn.body.setFill("green")
    new_game_btn.label.setSize(24)
    new_game_btn.draw(window)

    main_menu_btn = Button(Point(750, 400), Point(950, 500), "Quit")
    main_menu_btn.body.setFill("red")
    main_menu_btn.label.setSize(24)
    main_menu_btn.draw(window)


    if not window.isClosed():
        while True:
            
            click1=window.getMouse()
            if new_game_btn.inside(click1):
                window.close()
                main()
                
            if main_menu_btn.inside(click1):
                quit_text=Text(Point(600,600), "Quitting the game...")
                quit_text.setSize(20)
                quit_text.draw(window)
                time.sleep(1)
                sys.exit()


def lose_window(window):
    window.setBackground(color_rgb(255, 204, 203))

    lost_message = Text(Point(600, 200), "You Lost :(")
    lost_message.setStyle('bold')
    lost_message.setSize(36)
    lost_message.draw(window)

    new_game_btn = Button(Point(250, 400), Point(450, 500), "New Game")
    new_game_btn.body.setFill("green")
    new_game_btn.label.setSize(24)
    new_game_btn.draw(window)

    main_menu_btn = Button(Point(750, 400), Point(950, 500), "Quit")
    main_menu_btn.body.setFill("red")
    main_menu_btn.label.setSize(24)
    main_menu_btn.draw(window)
    

   
    if not window.isClosed():

            if new_game_btn.bind_click(window, lambda *args: None):
                window.close()
                main()
                
            if main_menu_btn.bind_click(window,lambda *args: None):
                quit_text=Text(Point(600,600), "Quitting the game...")
                quit_text.setSize(20)
                quit_text.draw(window)
                time.sleep(1)
                sys.exit()




def generate_random_card():
    suits = ["spades", "diamonds", "hearts", "clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
    suit = random.choice(suits)
    value = random.choice(values)
    return f"./cards/{value}_of_{suit}.png", value



def display_card(card_file, window):
    card_image = Image(Point(600, 250), card_file)
    card_image.draw(window)

def main():
    win = GraphWin("Slapjack", 1200, 800)
    reveal_button = Button(Point(250, 550), Point(550, 700), "REVEAL")
    reveal_button.body.setFill("green")
    reveal_button.label.setSize(24)
    reveal_button.draw(win)
    
    slap_button = Button(Point(750, 550), Point(1050, 700), "SLAP")
    slap_button.body.setFill("red")
    slap_button.label.setSize(24)
    slap_button.draw(win)
    while True:

        
        click1=win.getMouse()
        
        slap_button.body.setFill("red")
        slap_button.label.setSize(24)
        if reveal_button.inside(click1):
            card_file,value = generate_random_card()
            display_card(card_file, win)
            slap_button.undraw(win)
            x1 = random.randint(50,900)
            x2= x1+200
            y1= random.randint(100,900)
            y2= y1+200
            if x1 > 150 or x2 <650 or y1 > 650 or y2 < 800:
                x1 = random.randint(50,900)
                x2= x1+200
                y1= random.randint(100,900)
                y2= y1+200
            slap_button = Button(Point(x1, y1), Point(x2, y2), "SLAP")
            slap_button.label.setSize(24)
            slap_button.body.setFill("red")
            slap_button.draw(win)
            
        elif slap_button.inside(click1):
            if value =="jack":
                print ("you win")
                reveal_button.undraw(win)
                slap_button.undraw(win)
                win_window(win)
                
                
                
            else:
                print ("you lose")
                lose_window(win)
                reveal_button.undraw(win)
                slap_button.undraw(win)
                
                
        else:
            pass
        
main()
