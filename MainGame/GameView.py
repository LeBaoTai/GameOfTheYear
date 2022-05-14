#import module
import math
import os
import arcade

#import file
from Entity import *
from GameOverView import GameOverView

# vi tri bat dau cua nhan vat
PLAYER_START_X = 2
PLAYER_START_Y = 1

# to do vat ly cua vien dan
SPRITE_SCALING_LASER = 0.8
SHOOT_SPEED = 15
BULLET_SPEED = 12
BULLET_DAMAGE = 25

# toc do vat ly cua nhan vat
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 25

# tao khoang cach toi thieu giua nhan vat va moi canh cua man hinh
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

# khai bai ten chung cho cac layer
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_BULLETS = "Bullets"

#scaling player, tile,.....
TILE_SCALING = 0.5
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

class GameView(arcade.View):
    '''Chuong trinh chinh cua tro choi'''
    def __init__(self):
        super().__init__()
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        '''
        khai bao bien cho game
        '''
        #khai bao tile map
        self.tileMap = None

        #khai bao scene de ve tile map, nhan vat, ...
        self.scene = None
        
        #khai bao bien dem level de chuyen canh
        self.level = 1
        
        # khai bao bien di chuyen
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        

        
        #khai bao sprite Nhan vat
        self.playerSprite = None
        
        #khai bao vat ly
        self.physicEngine = None
        
        #khai bao camera
        self.camera = None
        self.gui_camera = None
        
        #khai bao diem
        self.score = 0
        
        # khai bao ban sung
        self.shoot_pressed = False
        self.can_shoot = False
        self.shoot_timer = 0

        # khai bao am thanh game
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

    def setup(self):
        #camera
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        
        #tile map
        mapName = f'/GameOfTheYear/Level/level_{self.level}.json'
        layerOptions = {
            LAYER_NAME_PLATFORMS: {
                'use_spatial_hash': True,
            },
            LAYER_NAME_MOVING_PLATFORMS: {
                'use_spatial_hash': True
            },
            LAYER_NAME_LADDERS: {
                'use_spatial_hash': True,
            },
            LAYER_NAME_COINS: {
                'use_spatial_hash': True
            }
        }
        self.tileMap = arcade.load_tilemap(mapName, TILE_SCALING, layerOptions)
        
        #load tile map vao scene
        self.scene = arcade.Scene.from_tilemap(self.tileMap)   
        
        # Keep track of the score
        self.score = 0

        # Shooting mechanics
        self.can_shoot = True
        self.shoot_timer = 0

        # Set up the player, specifically placing it at these coordinates.
        self.playerSprite = PlayerCharacter()
        self.playerSprite.center_x = (
            self.tileMap.tile_width * TILE_SCALING * PLAYER_START_X
        )
        self.playerSprite.center_y = (
            self.tileMap.tile_height * TILE_SCALING * PLAYER_START_Y + 100
        )
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.playerSprite)
        self.scene.add_sprite_list_after(LAYER_NAME_PLAYER, LAYER_NAME_FOREGROUND)
        # -- Enemies
        enemies_layer = self.tileMap.object_lists[LAYER_NAME_ENEMIES]

        for my_object in enemies_layer:
            cartesian = self.tileMap.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            enemy_type = my_object.properties["type"]
            if enemy_type == "robot":
                enemy = RobotEnemy()
            elif enemy_type == "zombie":
                enemy = ZombieEnemy()
            enemy.center_x = math.floor(
                cartesian[0] * TILE_SCALING * self.tileMap.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tileMap.tile_height * TILE_SCALING)
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

        # --- Other stuff
        # # Set the background color
        # if self.tileMap.background_color:
        #     arcade.set_background_color(self.tileMap.background_color)

        # Create the 'physics engine'
        self.physicEngine = arcade.PhysicsEnginePlatformer(
            self.playerSprite,
            platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
            gravity_constant=GRAVITY,
            ladders=self.scene[LAYER_NAME_LADDERS],
            walls=self.scene[LAYER_NAME_PLATFORMS]
        )
        
        
    def on_show(self):
        self.setup()

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        #camera nhan vat
        self.camera.use()

        # ve tile map va nhan vat
        self.scene.draw()

        # bat cameragui truoc khi ve cac phan tu
        self.gui_camera.use()

        # hien thi diem
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )
        
    def process_keychange(self):
        '''Ham xu ly tha/nhan phim hoac khi di chuyen tren thang'''
        # xu ly len/xuong
        if self.up_pressed and not self.down_pressed:
            if self.physicEngine.is_on_ladder():
                self.playerSprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physicEngine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.playerSprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physicEngine.is_on_ladder():
                self.playerSprite.change_y = -PLAYER_MOVEMENT_SPEED

        # xu ly di chuyen tren thang
        if self.physicEngine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.playerSprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.playerSprite.change_y = 0

        # xu ly trai/phai
        if self.right_pressed and not self.left_pressed:
            self.playerSprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.playerSprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.playerSprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Ham dc goi khi nhan phim"""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.SPACE:
            self.shoot_pressed = True

        # phong to thu nho camera
        if key == arcade.key.PLUS:
            self.camera.zoom(0.01)
        elif key == arcade.key.MINUS:
            self.camera.zoom(-0.01)

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        '''Ham duoc goi khi tha phim'''
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        if key == arcade.key.SPACE:
            self.shoot_pressed = False

        self.process_keychange()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.camera.zoom(-0.01 * scroll_y)

    def center_camera_to_player(self, speed=0.2):
        screen_center_x = self.camera.scale * (self.playerSprite.center_x - (self.camera.viewport_width / 2))
        screen_center_y = self.camera.scale * (self.playerSprite.center_y - (self.camera.viewport_height / 2))
        
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = (screen_center_x, screen_center_y)    

        self.camera.move_to(player_centered, speed)
        
    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physicEngine.update()

        # Update animations
        if self.physicEngine.can_jump():
            self.playerSprite.can_jump = False
        else:
            self.playerSprite.can_jump = True

        if self.physicEngine.is_on_ladder() and not self.physicEngine.can_jump():
            self.playerSprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.playerSprite.is_on_ladder = False
            self.process_keychange()

        if self.can_shoot:
            if self.shoot_pressed:
                arcade.play_sound(self.shoot_sound)
                bullet = arcade.Sprite(
                    "/GameOfTheYear/Assets/Bullets/skill1.png",
                    SPRITE_SCALING_LASER,
                )

                if self.playerSprite.facing_direction == RIGHT_FACING:
                    bullet.change_x = BULLET_SPEED
                else:
                    bullet.change_x = -BULLET_SPEED

                bullet.center_x = self.playerSprite.center_x
                bullet.center_y = self.playerSprite.center_y

                self.scene.add_sprite(LAYER_NAME_BULLETS, bullet)

                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == SHOOT_SPEED:
                self.can_shoot = True
                self.shoot_timer = 0

        # Update Animations
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_COINS,
                LAYER_NAME_BACKGROUND,
                LAYER_NAME_PLAYER,
                LAYER_NAME_ENEMIES,
            ],
        )

        # Update moving platforms, enemies, and bullets
        self.scene.update(
            [LAYER_NAME_MOVING_PLATFORMS, LAYER_NAME_ENEMIES, LAYER_NAME_BULLETS]
        )

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
                            collision.remove_from_sprite_lists()
                            self.score += 20

                        # Hit sound
                        arcade.play_sound(self.hit_sound)

                return

            if (bullet.right < 0) or (
                bullet.left
                > (self.tileMap.width * self.tileMap.tile_width) * TILE_SCALING
            ):
                bullet.remove_from_sprite_lists()

        player_collision_list = arcade.check_for_collision_with_lists(
            self.playerSprite,
            [
                self.scene[LAYER_NAME_COINS],
                self.scene[LAYER_NAME_ENEMIES],
            ],
        )

        # Loop through each coin we hit (if any) and remove it
        for collision in player_collision_list:

            if self.scene[LAYER_NAME_ENEMIES] in collision.sprite_lists:
                arcade.play_sound(self.game_over)
                game_over = GameOverView()
                self.window.show_view(game_over)
                return
            else:

                points = int(collision.properties["point"])
                self.score += points

                # Remove the coin
                collision.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)

        # Position the camera
        self.center_camera_to_player()
