#import file or module
import arcade
import GameRun

#size window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680

class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""
    
    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        arcade.draw_text(
            "GeaMonkee Studio present - A platform Game",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 60,
            arcade.color.BABY_BLUE,
            font_size=30,
            anchor_x="center",
        )
        arcade.draw_text(
            "Main Menu - Click to play game",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.RED_BROWN,
            font_size=30,
            anchor_x="center",
        )
        
        arcade.draw_text(
            "Move: W, S, A, D",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 40,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )
        
        arcade.draw_text(
            "Attack: SPACE",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 80,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = GameRun.GameView()
        self.window.show_view(game_view)
