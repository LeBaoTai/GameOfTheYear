#import file or module
import arcade
import arcade.gui
from pygame import MIDIIN
import GameRun
import GameTuto
import GameMenu

#size window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680
SCREEN_TITLE = "Game of the year"

class NewGameInMenu(arcade.View):
    def __init__(self):
        super().__init__()
        gameRun = GameRun.GameView()
        self.window.show_view(gameRun)

class GameTutoInMenu(arcade.View):
    def __init__(self):
        super().__init__()
        gameTuto = GameTuto.TuToView()
        self.window.show_view(gameTuto)
        
class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""
    def __init__(self):
        super().__init__()
        self.backgroundImg = arcade.load_texture("/GameOfTheYear/Assets/BackgroundImg/menubg.jpg")
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        newGameStyle = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": (21, 19, 21),

            # used if button is pressed
            "border_color_pressed": arcade.color.WHITE,  # also used when hovered
        }

        quitGameStyle = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.REDWOOD,

            # used if button is pressed
            "border_color_pressed": arcade.color.WHITE,  # also used when hovered
        }

        tutoGameStyle = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.BABY_BLUE_EYES,

            # used if button is pressed
            "border_color_pressed": arcade.color.WHITE,  # also used when hovered
        }
        
        quitGameButton = arcade.gui.UIFlatButton(text="Quit", width=200, style=quitGameStyle)
        newGameButton = arcade.gui.UIFlatButton(text="New Game", width=200, style=newGameStyle)
        tutoGameButton = arcade.gui.UIFlatButton(text="Tutorial", width=200, style=tutoGameStyle)
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)
        self.v_box.add(newGameButton)
        self.v_box.add(tutoGameButton)
        self.v_box.add(quitGameButton)

        @tutoGameButton.event("on_click")
        def click(event):
            GameTutoInMenu()
            self.manager.disable()
        @newGameButton.event("on_click")
        def click(event):
            NewGameInMenu()
            self.manager.disable()
        @quitGameButton.event("on_click")
        def click(event):
            arcade.exit()

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box
            )
        )
        
    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)
        
    def on_draw(self):
        
        """Draw the menu"""
        self.clear()   
        arcade.draw_texture_rectangle(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT / 2,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            texture=self.backgroundImg,
        ) 

        arcade.draw_text(
            "GeaMonKee Studio",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 180,
            arcade.color.RADICAL_RED,
            font_size=40,
            anchor_x="center",
        )
        self.manager.draw()
