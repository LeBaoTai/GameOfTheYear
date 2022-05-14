#import module
import arcade

# #import file
import GameMenu

#size window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680
SCREEN_TITLE = "Game of the year"

def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = GameMenu.MainMenu()  
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()