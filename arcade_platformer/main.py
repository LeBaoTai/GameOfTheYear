"""
GeaMonkee's Game
"""
import arcade
import pathlib
import os
import math

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "GeaMonkee's Adventure"

# Shooting Constants
SPRITE_SCALING_LASER = 0.8
SHOOT_SPEED = 15
BULLET_SPEED = 12
BULLET_DAMAGE = 50

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# Assets path
ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
MAP_WIDTH = 50 * 64
MAP_HEIGHT = 20 * 64
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# Timer
TIME_LIMIT = 60

# Total levels
LEVELS = 5

# Player starting position
PLAYER_START_X = 64
PLAYER_START_Y = 225

# Layer Names from our TileMap
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DONT_TOUCH = "Don't Touch"
LAYER_NAME_DOOR = "Doors"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_BULLETS = "Bullets"

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class Entity(arcade.Sprite):
    def __init__(self, name_file, custom_scale = 1):
        super().__init__()
        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = custom_scale
        self.character_face_direction = RIGHT_FACING

        # main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"
        main_path = ASSETS_PATH / 'images' / 'Enemies'

        self.idle_texture_pair = load_texture_pair(main_path / f"{name_file}.png")

        # Load textures for walking
        self.walk_textures = []
        self.walk_textures.append(load_texture_pair(main_path / f"{name_file}.png"))
        self.walk_textures.append(load_texture_pair(main_path / f"{name_file}_move.png"))

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.hit_box = self.texture.hit_box_points

class Enemy(Entity):
    def __init__(self, name_file, custom_scale = 1):

        # Setup parent class
        super().__init__(name_file, custom_scale)
        self.should_update_walk = 0
    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x > 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x < 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 1:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1

class SlimeGreen(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("slimeGreen")
        self.health = 50
        self.points = 20

class SlimeBlue(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("slimeBlue")
        self.health = 50
        self.points = 20

class Saw(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("saw", 0.5)
        self.health = 9999999

class SawHalf(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("sawHalf")
        self.health = 50

class Fly(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("fly", 0.5)
        self.health = 50
        self.points = 30


class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()
        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = ASSETS_PATH / 'images' /'Players'
        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(main_path / f"alienGreen_stand.png")
        self.jump_texture_pair = load_texture_pair(main_path / f"alienGreen_jump.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(2):
            texture = load_texture_pair(main_path / f"alienGreen_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(main_path / f"alienGreen_climb1.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(main_path / f"alienGreen_climb2.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 1:
            self.cur_texture = 0    
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]

class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        arcade.draw_text(
            "Main Menu - Click to play game",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
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
        game_view = GameView()
        self.window.show_view(game_view)

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # Set the path to start with this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.shoot_pressed = False
        # Our Scene Object
        self.scene = None

        # Our TileMap Object
        self.tile_map = None
        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Our TileMap Object
        self.tile_map = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

        # Shooting mechanics
        self.can_shoot = False
        self.shoot_timer = 0

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Level
        self.level = 2

        # Lives
        self.lives = 3;

        # Times
        self.times = TIME_LIMIT;

        # Highest Score
        self.high_score = 0;

        self.left_down = False;
        self.right_down = False;
        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        arcade.set_background_color((208,244,247))

    def setup(self, prev_score = 0):
        """Set up the game here. Call this function to restart the game."""
        
        # Set up the Cameras
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        
        # Map name
        map_path = pathlib.Path(__file__).resolve().parent.parent / 'arcade_platformer'
        map_name = map_path / f"platform_level_0{self.level}.json"
        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True,
            },
        }
        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.score = prev_score;

        # Add Player Spritelist before "Foreground" layer. This will make the foreground
        # be drawn after the player, making it appear to be in front of the Player.
        # Setting before using scene.add_sprite allows us to define where the SpriteList
        # will be in the draw order. If we just use add_sprite, it will be appended to the
        # end of the order.
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite_list_after(LAYER_NAME_PLAYER, LAYER_NAME_BACKGROUND)
        self.scene.add_sprite_list_after(LAYER_NAME_PLAYER, LAYER_NAME_LADDERS)
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
        # --- Load in a map from the tiled editor ---
        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # -- Enemies
        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]
        for my_object in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            enemy_type = my_object.properties["type"]
            if enemy_type == "slimeGreen":
                enemy = SlimeGreen()
            elif enemy_type == "saw":
                enemy = Saw();
            elif enemy_type == "slimeBlue":
                enemy = SlimeBlue();
            elif enemy_type == "fly":
                enemy = Fly();
            else:
                raise Exception(f"Unknown enemy type {enemy_type}.")
            enemy.center_x = math.floor(
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
            )
            if "boundary_left" in my_object.properties:
                enemy.boundary_left = my_object.properties["boundary_left"]
            if "boundary_right" in my_object.properties:
                enemy.boundary_right = my_object.properties["boundary_right"]
            if "change_x" in my_object.properties:
                enemy.change_x = my_object.properties["change_x"]
            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)
        
        # Add bullet spritelist to Scene
        self.scene.add_sprite_list(LAYER_NAME_BULLETS)
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            gravity_constant=GRAVITY, 
            walls=self.scene["Platforms"],
            platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
            ladders=self.scene[LAYER_NAME_LADDERS],
        )

    def on_show(self):
        self.setup()

    def on_draw(self):
        """Render the screen."""

        self.clear()

        # Activate our Camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )
        lives_left = f"Lives: {self.lives}"
        arcade.draw_text(
            lives_left,
            10,
            620,
            arcade.csscolor.BLACK,
            18,
        )

        times_left = f"Times: {math.floor(self.times)}"
        arcade.draw_text(
            times_left,
            880,
            620,
            arcade.csscolor.BLACK,
            18,
        )
    
    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            if self.player_sprite.center_x > 3175:
                self.player_sprite.change_x = 0
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            if self.player_sprite.center_x < 32:
                self.player_sprite.change_x = 0
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.left_down = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.right_down = True
        if key == arcade.key.SPACE:
            self.shoot_pressed = True
        self.process_keychange()
    
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
            self.left_down = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            self.right_down = False

        if key == arcade.key.SPACE:
            self.shoot_pressed = False
        self.process_keychange()
    
    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()
        self.times -= delta_time
        if self.times < 0:
            arcade.play_sound(self.game_over)
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            self.lives -= 1
            self.high_score = self.score if (self.score > self.high_score) else self.high_score;
            self.score = 0;
            self.times = TIME_LIMIT;
            if (self.lives == 0):
                game_over = GameOverView(self.high_score)
                self.window.show_view(game_over)
                return
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        if self.can_shoot:
            if self.shoot_pressed:
                arcade.play_sound(self.shoot_sound)
                main_path = ASSETS_PATH / 'images' / 'Particles'
                bullet = arcade.Sprite(
                    main_path / f"fireball_1.png",
                    SPRITE_SCALING_LASER,
                )
                if self.player_sprite.facing_direction == RIGHT_FACING:
                    bullet.change_x = BULLET_SPEED
                else:
                    bullet.change_x = -BULLET_SPEED

                bullet.center_x = self.player_sprite.center_x
                bullet.center_y = self.player_sprite.center_y - 32
                self.scene.add_sprite(LAYER_NAME_BULLETS, bullet)
                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == SHOOT_SPEED:
                self.can_shoot = True
                self.shoot_timer = 0


        # Position the camera
        self.center_camera_to_player()

        # Update Animations
        self.scene.update_animation(
            delta_time, [LAYER_NAME_COINS, LAYER_NAME_BACKGROUND, LAYER_NAME_PLAYER, LAYER_NAME_ENEMIES]
        )

        # Update walls, used with moving platforms
        self.scene.update([LAYER_NAME_MOVING_PLATFORMS, LAYER_NAME_ENEMIES, LAYER_NAME_BULLETS])

        # See if the enemy hit a boundary and needs to reverse direction.
        for enemy in self.scene[LAYER_NAME_ENEMIES]:
            if (
                enemy.boundary_right
                and enemy.right > enemy.boundary_right
                and enemy.change_x > 0
            ):
                enemy.change_x *= -1

            if (
                enemy.boundary_left
                and enemy.left < enemy.boundary_left
                and enemy.change_x < 0
            ):
                enemy.change_x *= -1

        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[LAYER_NAME_COINS],
                self.scene[LAYER_NAME_ENEMIES],
                self.scene["Doors"]
            ],
        )

        for bullet in self.scene[LAYER_NAME_BULLETS]:
            hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene[LAYER_NAME_ENEMIES],
                    self.scene[LAYER_NAME_PLATFORMS],
                    self.scene[LAYER_NAME_MOVING_PLATFORMS],
                ],
            )

            if hit_list:
                bullet.remove_from_sprite_lists()

                for collision in hit_list:
                    if (
                        self.scene[LAYER_NAME_ENEMIES]
                        in collision.sprite_lists
                    ):
                        # The collision was with an enemy
                        collision.health -= BULLET_DAMAGE

                        if collision.health <= 0:
                            self.score += collision.points
                            collision.remove_from_sprite_lists()

                        # Hit sound
                        arcade.play_sound(self.hit_sound)

                return
            if (bullet.right < 0) or (
                bullet.left
                > (self.tile_map.width * self.tile_map.tile_width) * TILE_SCALING
            ):
                bullet.remove_from_sprite_lists()

        for collision in player_collision_list:

            if self.scene[LAYER_NAME_ENEMIES] in collision.sprite_lists:
                arcade.play_sound(self.game_over)
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y
                self.lives -= 1
                self.high_score = self.score if (self.score > self.high_score) else self.high_score;
                self.score = 0;
                self.times = TIME_LIMIT;
                if (self.lives == 0):
                    game_over = GameOverView(self.high_score)
                    self.window.show_view(game_over)
                return
            if self.scene["Doors"] in collision.sprite_lists:
                # Advance to the next level
                self.level += 1;
                self.score += math.floor(self.times * 10);
                self.lives = 3;
                if self.level == LEVELS:
                    game_complete = GameCompleteView(self.high_score)
                    self.window.show_view(game_complete)
                    return
                # Load the next level
                self.times = TIME_LIMIT
                self.setup(self.score)
            else:
                # Figure out how many points this coin is worth
                if "point_value" not in collision.properties:
                    print("Warning, collected a coin without a Points property.")
                else:
                    points = int(collision.properties["point_value"])
                    self.score += points

                # Remove the coin
                collision.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            arcade.play_sound(self.game_over)
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            self.lives -= 1
            self.high_score = self.score if (self.score > self.high_score) else self.high_score;
            self.score = 0;
            self.times = TIME_LIMIT;
            if (self.lives == 0):
                game_over = GameOverView(self.high_score)
                self.window.show_view(game_over)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]
        ):
            arcade.play_sound(self.game_over)
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            self.lives -= 1
            self.high_score = self.score if (self.score > self.high_score) else self.high_score;
            self.score = 0;
            self.times = TIME_LIMIT;
            if (self.lives == 0):
                game_over = GameOverView(self.high_score)
                self.window.show_view(game_over)
    
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        # print(screen_center_x, screen_center_y)
        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        if screen_center_x > 2200:
            screen_center_x = 2200
        if screen_center_y > 624:
            screen_center_y = 624
        player_centered = screen_center_x, screen_center_y
        # print(player_centered)
        self.camera.move_to(player_centered)

class GameOverView(arcade.View):
    """Class to manage the game overview"""
    def __init__(self, high_score = 0 ):
        super().__init__();
        self.high_score = high_score
    def on_show(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_text(
            "Game Over",
            SCREEN_WIDTH / 2,\
            SCREEN_HEIGHT / 2 + 100,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )
        arcade.draw_text(
            "High Score: " + str(self.high_score),
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 ,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

        arcade.draw_text(
            "Click to return to main menu!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        menu_view = MainMenu()
        self.window.show_view(menu_view)

class GameCompleteView(arcade.View):
    """Class to manage the game overview"""
    def __init__(self, high_score = 0 ):
        super().__init__();
        self.high_score = high_score
    def on_show(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_text(
            "Thanks for playing!",
            SCREEN_WIDTH / 2,\
            SCREEN_HEIGHT / 2 + 200,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )
        arcade.draw_text(
            "You completed Geamonkee Adventure!",
            SCREEN_WIDTH / 2,\
            SCREEN_HEIGHT / 2 + 100,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )
        arcade.draw_text(
            "High Score: " + str(self.high_score),
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 ,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

        arcade.draw_text(
            "Click to return to main menu!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        menu_view = MainMenu()
        self.window.show_view(menu_view)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()