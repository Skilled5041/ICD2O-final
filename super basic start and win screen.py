from graphics import * 
window=GraphWin(1200, 800)
def WinWindow():
 
        Rectanglecoveringscreen = Rectangle(Point(0,0),Point(800,600))
       
        Rectanglecoveringscreen.setFill("lightblue")
        Rectanglecoveringscreen.setOutline("lightblue")
        Rectanglecoveringscreen.draw(window)
 
 
 
        win_message = Text(Point(400, 200), "CONGRATS YOU WON!!!!")
        win_message.setFace('times roman')
        win_message.setTextColor('green')
        win_message.setStyle('bold')
        win_message.setSize(35)
        win_message.draw(window)
        start_button = Rectangle(Point(150, 400), Point(350, 500))
        start_button.draw(window)
        start_button.setFill("green")
        start_text = Text(Point(250, 450), "New Game")
        start_text.setTextColor("black")
        start_text.setSize(20)
        start_text.draw(window)
 
        quit_button = Rectangle(Point(450, 400), Point(650, 500))
        quit_button.setFill("red")
        quit_button.draw(window)
        quit_text = Text(Point(550, 450), "Quit")
        quit_text.setTextColor("black")
        quit_text.setSize(20)
        quit_text.draw(window)
 
        while True:
            pt = window.getMouse()
 
            if 150 <= pt.getX() <= 350 and 400 <= pt.getY() <= 500:
                window.close()
               
            elif 450 <= pt.getX() <= 650 and 400 <= pt.getY() <= 500:
                quit_text=Text(Point(400,300), "Quitting the game...")
                quit_text.setSize(20)
                quit_text.draw(window)
                time.sleep(1)
                sys.exit()
               
 
 
 
 
 
def LostWindow():
    lost_window = GraphWin("Lost Game", 1200, 800)
    lost_window.setBackground(color_rgb(255,204,203))

    lost_message = Text(Point(400, 200), "Sorry you Lost ")
    lost_message.setFace('times roman')
    lost_message.setTextColor('red')
    lost_message.setStyle('bold')
    lost_message.setSize(35)
    lost_message.draw(lost_window)
    lost_window.update()

    start_button2 = Rectangle(Point(150, 400), Point(350, 500))
    start_button2.draw(lost_window)
    start_button2.setFill("green")
    start_text2 = Text(Point(250, 450), "New Game")
    start_text2.setTextColor("black")
    start_text2.setSize(20)
    start_text2.draw(lost_window)

    quit_button2 = Rectangle(Point(450, 400), Point(650, 500))
    quit_button2.setFill("red")
    quit_button2.draw(lost_window)
    quit_text2 = Text(Point(550, 450), "Quit")
    quit_text2.setTextColor("black")
    quit_text2.setSize(20)
    quit_text2.draw(lost_window)

    while True:
        pt = lost_window.getMouse()

        if 150 <= pt.getX() <= 350 and 400 <= pt.getY() <= 500:
            lost_window.close()
          
        elif 450 <= pt.getX() <= 650 and 400 <= pt.getY() <= 500:
            quit_text=Text(Point(400,300), "Quitting the game...")
            quit_text.setSize(20)
            quit_text.draw(lost_window)
            time.sleep(1)
            sys.exit()
