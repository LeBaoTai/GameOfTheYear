#import zone
import arcade

#huong nhin nhan vat
RIGHT_FACING = 0
LEFT_FACING = 1
CHARACTER_SCALING = 1


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0

        
        # neu la player thi dung file trong folder AmimatedCharacter
        if name_folder == 'player' and name_file == 'player':
            self.scale = CHARACTER_SCALING/2
            main_path = f"/GameOfTheYear/AnimatedCharacter/{name_folder}/{name_file}"
            self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
            self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")

            # Load textures for walking
            self.walk_textures = []
            for i in range(1, 3):
                texture = load_texture_pair(f"{main_path}_walk{i}.png")
                self.walk_textures.append(texture)

            # Load textures for climbing
            self.climbing_textures = []
            texture = arcade.load_texture(f"{main_path}_climb1.png")
            self.climbing_textures.append(texture)
            texture = arcade.load_texture(f"{main_path}_climb2.png")
            self.climbing_textures.append(texture)
        
        # nguoc lai dung file tren module 
        else:
            self.scale = CHARACTER_SCALING
            main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"
            
            self.walk_textures = []
            for i in range(8):
                texture = load_texture_pair(f"{main_path}_walk{i}.png")
                self.walk_textures.append(texture)
            self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
            
        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

        self.should_update_walk = 0

class Enemy(Entity):
    def __init__(self, name_folder, name_file):

        # Setup parent class
        super().__init__(name_folder, name_file)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1


class RobotEnemy(Enemy):
    def __init__(self):
        # Set up parent class
        super().__init__("robot", "robot")
        self.health = 90


class ZombieEnemy(Enemy):
    def __init__(self):
        # Set up parent class
        super().__init__("zombie", "zombie")
        self.health = 80

class PlayerCharacter(Entity):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__("player", "player")

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

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
        elif self.change_y < 0 and not self.is_on_ladder:
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
