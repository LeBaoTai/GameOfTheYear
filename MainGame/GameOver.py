import arcade
import GameMenu

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680

class GameOverView(arcade.View):
    """Class to manage the game overview"""
    def __init__(self, score):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.score = score

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

        quitGameButton = arcade.gui.UIFlatButton(text="Quit", width=200, style=quitGameStyle)
        newGameButton = arcade.gui.UIFlatButton(text="New Game", width=200, style=newGameStyle)
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)
        self.v_box.add(newGameButton)
        self.v_box.add(quitGameButton)
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box
            )
        )
        
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
        self.manager.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = GameMenu.MainMenu()
        self.window.show_view(game_view)