import arcade
import GameMenu

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680

class GameOverView(arcade.View):
    """Class to manage the game overview"""
    def __init__(self, score):
        super().__init__()
        self.score = score
    def on_show(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_text(
            "Game Over",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 60,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )
        arcade.draw_text(
            f'Your Score: {self.score}',
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )
        arcade.draw_text(
            'Click to back to menu',
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 40,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = GameMenu.MainMenu()
        self.window.show_view(game_view)