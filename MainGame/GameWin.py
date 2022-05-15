import arcade
import GameMenu

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680

class GameWinView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score
    
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)
    
    def on_draw(self):
        self.clear()
        
        arcade.draw_text (
            f'Congratulations on completing the game!',
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 40,
            arcade.color.ATOMIC_TANGERINE,
            30,
            anchor_x= 'center'
        )
        
        arcade.draw_text (
            f'Your Score: {self.score}',
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 20,
            arcade.color.ATOMIC_TANGERINE,
            30,
            anchor_x= 'center'
        )
        
        arcade.draw_text (
            'Click to back to menu',
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 50,
            arcade.color.ATOMIC_TANGERINE,
            30,
            anchor_x= 'center'
        )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        game_view = GameMenu.MainMenu()
        self.window.show_view(game_view)