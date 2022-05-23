import arcade
import GameRun
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680

class TuToView(arcade.View):
    def __init__(self):
        super().__init__()
        self.backgroundImg = arcade.load_texture("/GameOfTheYear/Assets/BackgroundImg/menubg.jpg")
    def on_show(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)
    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_texture_rectangle(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT / 2,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            texture=self.backgroundImg,
        )     

        arcade.draw_text(
            "Click to play game",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 40,
            arcade.color.RED_BROWN,
            font_size=40,
            anchor_x="center",
        )
        
        arcade.draw_text(
            "Move: W, S, A, D",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 30,
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
        gameRunView = GameRun.GameView()
        self.window.show_view(gameRunView)
