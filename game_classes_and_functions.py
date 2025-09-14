import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import random
import math
from playsound import playsound
from threading import Thread
pygame.font.init()

small_font = pygame.font.SysFont('Press Start 2P', 20)

# ⬇️FUNCTIONS⬇️

def cut_spritesheet(sprite_list, image, width, height, start_x, start_y):
    for y in range(start_x, image.get_height(), height):
        for x in range(start_y, image.get_width(), width):
            sprite = image.subsurface(pygame.Rect(x, y, width, height))
            sprite_list.append(sprite)

def play_sound(name, mute, music, music_is_playing):
    if mute == False:
        if name != 'forest_music':
            playsound(name)
        elif name == 'forest_music':
            music.play(loops=-1)
            music_is_playing = True

def load_pygame(mute, music, music_is_playing):
    screen = pygame.display.set_mode((1008, 640))
    pygame.display.set_caption('stabby-stabby game')
    Thread(target=lambda: play_sound('start.mp3', mute, music, music_is_playing)).start()
    Thread(target=lambda: play_sound('forest_music', mute, music, music_is_playing)).start()
    return screen


def stop_or_play_music(name, music_is_playing, change):
    if music_is_playing == True:
        if change == True:
            name.stop()
        return music_is_playing
        music_is_playing = False
    elif music_is_playing == False:
        if change == True:
            name.play(loops=-1)
        return music_is_playing
        music_is_playing = True

def load_map(current_map):
    return pytmx.load_pygame(current_map, pixelalpha = True)

# ⬇️CLASSES⬇️

hero_img = pygame.image.load('$PixelPrince.png')
hero_sprites = []
cut_spritesheet(hero_sprites, hero_img, 48, 64, 0, 0)

class Player:
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.current_sprite = 0
        self.state = "idle"
        self.arrows = 50
        self.width = 48
        self.height = 64
        self.helmets = 0
        self.potions = 0
        self.maps = 0
        self.rings = 0
        self.necklaces = 0
        self.crowns = 0
        self.pearls = 0
        self.shells = 0
        self.inventory = {"sword": 1, "arrows": 50, "gems": 0}
        
        self.animations = {
            "idle_up": hero_sprites[0:3],
            "idle_right": hero_sprites[3:6],
            "idle_left": hero_sprites[6:9],
            "idle_down": hero_sprites[9:12],
            "moving_down": hero_sprites[12:15],
            "moving_left": hero_sprites[15:18],
            "moving_right": hero_sprites[18:21],
            "moving_up": hero_sprites[21:24],
            "attacking_down": hero_sprites[24:27],
            "attacking_left": hero_sprites[27:30],
            "attacking_right": hero_sprites[30:33],
            "attacking_up": hero_sprites[33:36]
        }

    def update(self):
        # Cycle through the sprites for animation
        self.current_sprite = (self.current_sprite + 1) % len(self.animations[self.state])

    def draw(self, screen):
        #pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(504, 320, self.width, self.height), 2)
        screen.blit(self.animations[self.state][self.current_sprite], (screen.get_width() // 2, screen.get_height() // 2))

# NPC class
bearded_villager_down = pygame.image.load('NPCs/Citizen/PNG/Front/PNG Sequences/Idle/idle.png')
bearded_villager_left = pygame.image.load('NPCs/Citizen/PNG/Side/PNG Sequences/Idle/idle.png')
bearded_villager_up = pygame.image.load('NPCs/Citizen/PNG/Back/PNG Sequences/Idle/idle.png')

artist_down = pygame.image.load('NPCs/Artist/PNG/Front/PNG Sequences/Idle/idle.png')
artist_left = pygame.image.load('NPCs/Artist/PNG/Side/PNG Sequences/Idle/idle.png')
artist_up = pygame.image.load('NPCs/Artist/PNG/Back/PNG Sequences/Idle/idle.png')

astrologer_down = pygame.image.load('NPCs/Astrologer/PNG/Front/PNG Sequences/Idle/idle.png')
astrologer_left = pygame.image.load('NPCs/Astrologer/PNG/Side/PNG Sequences/Idle/idle.png')
astrologer_up = pygame.image.load('NPCs/Astrologer/PNG/Back/PNG Sequences/Idle/idle.png')

hunter = pygame.image.load('NPCs2/Hunter/PNG/PNG Sequences/Idle/idle.png')
herbalist = pygame.image.load('NPCs2/Herbalist/PNG/PNG Sequences/Idle/idle.png')
jeweler = pygame.image.load('NPCs2/Jeweler/PNG/PNG Sequences/Idle/idle.png')
blacksmith = pygame.image.load('NPCs2/Blacksmith/PNG/PNG Sequences/Idle/idle.png')

blacksmith2 = pygame.image.load('NPCs3/Blacksmith/PNG/PNG Sequences/Idle/idle.png')
jeweler2 = pygame.image.load('NPCs3/Jeweler/PNG/PNG Sequences/Idle/idle.png')
sage = pygame.image.load('NPCs3/Sage/PNG/PNG Sequences/Idle/idle.png')
warlord = pygame.image.load('NPCs3/Warlord/PNG/PNG Sequences/Idle/idle.png')

speech_bubble = pygame.image.load('NPCs/Citizen/popup/PNG/popup_1.png')
speech_bubble2 = pygame.image.load('NPCs/Citizen/popup/PNG/popup_2.png')

class NPC:
    def __init__(self, x, y, kind, direction, offset_x, offset_y, speech, is_shopkeeper):
        self.move_x = 0
        self.move_y = 0
        self.width = 64
        self.height = 64
        self.kind = kind
        self.speech = speech
        self.speech_condition = False
        self.direction = direction
        self.is_shopkeeper = is_shopkeeper
        if self.is_shopkeeper == True:
            self.shopkeeper_speech_num = random.randint(0, 1)
        self.down_images = {
            "bearded_villager": bearded_villager_down,
            "herbalist": herbalist,
            "artist": artist_down,
            "astrologer": astrologer_down,
            "hunter": hunter,
            "jeweler": jeweler,
            "blacksmith": blacksmith,
            "blacksmith2": blacksmith2,
            "jeweler2": jeweler2,
            "sage": sage,
            "warlord": warlord
            }
        self.left_images = {
            "bearded_villager": bearded_villager_left,
            "artist": artist_left,
            "astrologer": astrologer_left
            }
        self.up_images = {
            "bearded_villager": bearded_villager_up,
            "artist": artist_up,
            "astrologer": astrologer_up
            }
        self.start_x = x
        self.start_y = y
        self.x = self.start_x + offset_x + self.move_x
        self.y = self.start_y + offset_y + self.move_y
        if self.direction == "down":
            self.big_image = self.down_images[self.kind]
        if self.direction == "up":
            self.big_image = self.up_images[self.kind]
        if self.direction == "left":
            self.big_image = self.left_images[self.kind]
        self.image = pygame.transform.scale(self.big_image, (64, 64))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, screen):
        #pygame.draw.rect(screen, (0, 255, 255), self.rect, 2)
        screen.blit(self.image, (self.x, self.y))

    def talk(self, screen, text, font):
        text_surface = font.render(text, True, (0, 0, 0))  # Black text
        bubble_rect = speech_bubble.get_rect(center=(self.x + 180, self.y + 150))  # Position the speech bubble above the NPC
        text_rect = text_surface.get_rect(center=(bubble_rect.x + 20, bubble_rect.y + 20))
        screen.blit(pygame.transform.scale(speech_bubble, (64, 64)), bubble_rect) # blit speech bubble
        screen.blit(text_surface, text_rect) # blit text
        
    def is_close(self, player, threshold=1000):
        #Check if the player is within a certain distance from the NPC.
        distance = ((player.x - self.x) ** 2 + (player.y - self.y) ** 2) ** 0.5
        return distance <= threshold

    def interact(self, screen, text, text_line_2, font):
        text_surface = font.render(text, True, (0, 0, 0))  # Black text
        text_surface2 = font.render(text_line_2, True, (0, 0, 0))
        bubble_rect2 = speech_bubble2.get_rect(center=(400, 800))
        text_rect = text_surface.get_rect(center=(bubble_rect2.x + 28, bubble_rect2.y + 20))
        text_rect2 = text_surface2.get_rect(center=(bubble_rect2.x + 28, bubble_rect2.y + 50))
        screen.blit(pygame.transform.scale(speech_bubble2, (220, 88)), bubble_rect2) # blit speech bubble
        screen.blit(text_surface, text_rect) # blit text
        screen.blit(text_surface2, text_rect2)
        pygame.draw.rect(screen, (0, 255, 255), self.rect, 2)

    def mouse_is_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False
    
# slime class
blue_slime_idle = pygame.image.load('slime_monsters/Blue_Slime/idle.png')
blue_slime_attack = pygame.image.load('slime_monsters/Blue_Slime/Attack_3.png')
blue_slime_death = pygame.image.load('slime_monsters/Blue_Slime/Dead.png')

green_slime_idle = pygame.image.load('slime_monsters/Green_Slime/Idle.png')
green_slime_attack = pygame.image.load('slime_monsters/Green_Slime/Attack_3.png')
green_slime_death = pygame.image.load('slime_monsters/Green_Slime/Dead.png')

red_slime_idle = pygame.image.load('slime_monsters/Red_Slime/Idle.png')
red_slime_attack = pygame.image.load('slime_monsters/Red_Slime/Attack_3.png')
red_slime_death = pygame.image.load('slime_monsters/Red_Slime/Dead.png')

blue_slime_idle_sprites = []
blue_slime_attack_sprites = []
blue_slime_death_sprites = []

green_slime_idle_sprites = []
green_slime_attack_sprites = []       
green_slime_death_sprites = []
        
red_slime_idle_sprites = []
red_slime_attack_sprites = []
red_slime_death_sprites = []

cut_spritesheet(red_slime_death_sprites, red_slime_death, 128, 128, 0, 0)
cut_spritesheet(red_slime_attack_sprites, red_slime_attack, 128, 128, 0, 0)
cut_spritesheet(red_slime_idle_sprites, red_slime_idle, 128, 128, 0, 0)

cut_spritesheet(green_slime_death_sprites, green_slime_death, 128, 128, 0, 0)
cut_spritesheet(green_slime_attack_sprites, green_slime_attack, 128, 128, 0, 0)
cut_spritesheet(green_slime_idle_sprites, green_slime_idle, 128, 128, 0, 0)

cut_spritesheet(blue_slime_death_sprites, blue_slime_death, 128, 128, 0, 0)
cut_spritesheet(blue_slime_attack_sprites, blue_slime_attack, 128, 128, 0, 0)
cut_spritesheet(blue_slime_idle_sprites, blue_slime_idle, 128, 128, 0, 0)

class Slime:
    def __init__(self, x, y, color, offset_x, offset_y):
        self.x = x
        self.y = y
        self.height = 128
        self.width = 128
        self.move_x = 0
        self.move_y = 0
        self.x = offset_x + self.x + self.move_x
        self.y = offset_y + self.y + self.move_y
        self.rect = pygame.Rect(self.x + 5, self.y + self.height / 2 - 10, self.width - 16, self.height - 16)
        self.current_sprite = 0
        self.state = "idle"
        self.color = color
        self.alive = True
        self.speed = 10
        self.blue_animations = {
            "idle": blue_slime_idle_sprites[0:8],
            "attack": blue_slime_attack_sprites[0:5],
            "death": blue_slime_death_sprites[0:3]
        }
        self.green_animations = {
            "idle": green_slime_idle_sprites[0:8],
            "attack": green_slime_attack_sprites[0:5],
            "death": green_slime_death_sprites[0:3]
        }
        self.red_animations = {
            "idle": red_slime_idle_sprites[0:8],
            "attack": red_slime_attack_sprites[0:5],
            "death": red_slime_death_sprites[0:3]
        }
        
    def update(self):
        # Cycle through the sprites for animation
        if self.color == "blue":
            self.current_sprite = (self.current_sprite + 1) % len(self.blue_animations[self.state])
            
        if self.color == "green":
            self.current_sprite = (self.current_sprite + 1) % len(self.green_animations[self.state])
            
        if self.color == "red":
            self.current_sprite = (self.current_sprite + 1) % len(self.red_animations[self.state])
        
    def draw(self, screen):
        if self.alive:  # Only draw if the blue slime is alive
            if self.color == "blue":
                screen.blit(self.blue_animations[self.state][self.current_sprite], (self.x, self.y))
            if self.color == "green":
                screen.blit(self.green_animations[self.state][self.current_sprite], (self.x, self.y))
            if self.color == "red":
                screen.blit(self.red_animations[self.state][self.current_sprite], (self.x, self.y))
            
            # Drawing a red rectangle around the blue slime
            red = (252, 52, 38)
            rect_thickness = 2
            #if self.color == "blue":
                #pygame.draw.rect(screen, red, self.rect, rect_thickness)
            #if self.color == "green":
                #pygame.draw.rect(screen, red, self.rect, rect_thickness)
            #if self.color == "red":
                 #pygame.draw.rect(screen, red, self.rect, rect_thickness)
            
        
    def attack(self):
        self.state = "attack"
        
    def end_attack(self):
        self.state = "idle"
        
    def move(self, x, y):
        self.move_x += x
        self.move_y += y
        
    def die(self):
        self.state = "death"
        if self.current_sprite == 2:         
            self.alive = False
    
    def move_towards_hero(self, hero, hero_width, hero_height, offset_x, offset_y):
        # Calculate direction vector from slime to hero
        dir_x = hero.x - hero_width / 2 + offset_x - self.x
        dir_y = hero.y - hero_height / 2 + offset_y - self.y
        
        # avoid moving the slime if it is too far away
        if dir_x > 320 and dir_y > 320:
            return
        
        if dir_x < -320 and dir_y < -320:
            return 
        
        # Normalize the direction (get unit vector)
        magnitude = (dir_x**2 + dir_y**2)**0.5
        if magnitude == 0:  # Avoid division by zero
            return
        
        dir_x /= magnitude
        dir_y /= magnitude
        
        # Update the slime's position
        self.move_x += dir_x * self.speed
        self.move_y += dir_y * self.speed

# giant bat class
giant_bat_left_sprites = []
giant_bat_right_sprites = []
giant_bat_up_sprites = []
giant_bat_down_sprites = []

giant_bat_left_attack_sprites = []
giant_bat_right_attack_sprites = []
giant_bat_up_attack_sprites = []
giant_bat_down_attack_sprites = []

giant_bat_left_attack2_sprites = []
giant_bat_right_attack2_sprites = []
giant_bat_up_attack2_sprites = []
giant_bat_down_attack2_sprites = []

giant_bat_left_death_sprites = []
giant_bat_right_death_sprites = []
giant_bat_up_death_sprites = []
giant_bat_down_death_sprites = []

giant_bat_attack_box_sprites = []

giant_bat_down = pygame.image.load('Goblin_Riding_Giant_Bat/Down/Png/GoblinRiderIdle.png')
giant_bat_up = pygame.image.load('Goblin_Riding_Giant_Bat/Up/Png/GoblinRiderUpIdle.png')
giant_bat_left = pygame.image.load('Goblin_Riding_Giant_Bat/Left/Png/GoblinRiderLeftIdle.png')
giant_bat_right = pygame.image.load('Goblin_Riding_Giant_Bat/Right/Png/GoblinRiderRightIdle.png')

giant_bat_attack_down = pygame.image.load('Goblin_Riding_Giant_Bat/Down/Png/GoblinRiderAttack01.png')
giant_bat_attack_up = pygame.image.load('Goblin_Riding_Giant_Bat/Up/Png/GoblinRiderUpAttack01.png')
giant_bat_attack_left = pygame.image.load('Goblin_Riding_Giant_Bat/Left/Png/GoblinRiderLeftAttack01.png')
giant_bat_attack_right = pygame.image.load('Goblin_Riding_Giant_Bat/Right/Png/GoblinRiderRightAttack01.png')

giant_bat_death_down = pygame.image.load('Goblin_Riding_Giant_Bat/Down/Png/GoblinRiderDeath.png')
giant_bat_death_up = pygame.image.load('Goblin_Riding_Giant_Bat/Up/Png/GoblinRiderUpDeath.png')
giant_bat_death_left = pygame.image.load('Goblin_Riding_Giant_Bat/Left/Png/GoblinRiderLeftDeath.png')
giant_bat_death_right = pygame.image.load('Goblin_Riding_Giant_Bat/Right/Png/GoblinRiderRightDeath.png')

giant_bat_attack2_down = pygame.image.load('Goblin_Riding_Giant_Bat/Down/Png/GoblinRiderAttack03.png')
giant_bat_attack2_up = pygame.image.load('Goblin_Riding_Giant_Bat/Up/Png/GoblinRiderUpAttack03.png')
giant_bat_attack2_left = pygame.image.load('Goblin_Riding_Giant_Bat/Left/Png/GoblinRiderLeftAttack03.png')
giant_bat_attack2_right = pygame.image.load('Goblin_Riding_Giant_Bat/Right/Png/GoblinRiderRightAttack03.png')

giant_bat_attack_box = pygame.image.load('Goblin_Riding_Giant_Bat/giant_bat_attack_box.png')

big_meat1 = pygame.image.load('meat-and-skin-icons/PNG/shadow/1.png')
meat1 = pygame.transform.scale(big_meat1, (64, 64))
big_meat2 = pygame.image.load('meat-and-skin-icons/PNG/shadow/3.png')
meat2 = pygame.transform.scale(big_meat2, (64, 64))
big_meat3 = pygame.image.load('meat-and-skin-icons/PNG/shadow/5.png')
meat3 = pygame.transform.scale(big_meat3, (64, 64))
big_meat4 = pygame.image.load('meat-and-skin-icons/PNG/shadow/14.png')
meat4 = pygame.transform.scale(big_meat4, (64, 64))
big_meat5 = pygame.image.load('meat-and-skin-icons/PNG/shadow/42.png')
meat5 = pygame.transform.scale(big_meat5, (64, 64))
big_meat6 = pygame.image.load('meat-and-skin-icons/PNG/shadow/37.png')
meat6 = pygame.transform.scale(big_meat6, (64, 64))


cut_spritesheet(giant_bat_left_sprites, giant_bat_left, 80, 80, 0, 0)
cut_spritesheet(giant_bat_right_sprites, giant_bat_right, 80, 80, 0, 0)
cut_spritesheet(giant_bat_up_sprites, giant_bat_up, 80, 80, 0, 0)
cut_spritesheet(giant_bat_down_sprites, giant_bat_down, 80, 80, 0, 0)

cut_spritesheet(giant_bat_left_attack_sprites, giant_bat_attack_left, 80, 80, 0, 0)
cut_spritesheet(giant_bat_right_attack_sprites, giant_bat_attack_right, 80, 80, 0, 0)
cut_spritesheet(giant_bat_up_attack_sprites, giant_bat_attack_up, 80, 80, 0, 0)
cut_spritesheet(giant_bat_down_attack_sprites, giant_bat_attack_down, 80, 80, 0, 0)

cut_spritesheet(giant_bat_left_death_sprites, giant_bat_death_left, 80, 80, 0, 0)
cut_spritesheet(giant_bat_right_death_sprites, giant_bat_death_right, 80, 80, 0, 0)
cut_spritesheet(giant_bat_up_death_sprites, giant_bat_death_up, 80, 80, 0, 0)
cut_spritesheet(giant_bat_down_death_sprites, giant_bat_death_down, 80, 80, 0, 0)

cut_spritesheet(giant_bat_left_attack2_sprites, giant_bat_attack2_left, 80, 80, 0, 0)
cut_spritesheet(giant_bat_right_attack2_sprites, giant_bat_attack2_right, 80, 80, 0, 0)
cut_spritesheet(giant_bat_up_attack2_sprites, giant_bat_attack2_up, 80, 80, 0, 0)
cut_spritesheet(giant_bat_down_attack2_sprites, giant_bat_attack2_down, 80, 80, 0, 0)

cut_spritesheet(giant_bat_attack_box_sprites, giant_bat_attack_box, 80, 80, 0, 0)

class Giant_Bat:
    def __init__(self, x, y, offset_x, offset_y):
        self.width = 80
        self.height = 80
        self.speed = 24
        self.move_x = 0
        self.move_y = 0
        self.x = offset_x + x + self.move_x
        self.y = offset_y + y + self.move_y
        self.rect = pygame.Rect(self.x + 5, self.y + self.height / 2 - 10, self.width - 16, self.height - 16)
        self.direction = "down"
        self.attack2 = False
        self.state = "idle"
        self.current_sprite = 0
        self.alive = True
        self.meat_exists = False
        self.meat_num = None
        self.attack_box_sprite = 0
        
        self.down_animations = {
            "idle": giant_bat_down_sprites[0:5],
            "attack": giant_bat_down_attack_sprites[0:6],
            "death": giant_bat_down_death_sprites[0:10],
            "attack2": giant_bat_down_attack2_sprites[0:4]
        }
        self.up_animations = {
            "idle": giant_bat_up_sprites[0:5],
            "attack": giant_bat_up_attack_sprites[0:6],
            "death": giant_bat_up_death_sprites[0:10],
            "attack2": giant_bat_up_attack2_sprites[0:4]
        }
        self.left_animations = {
            "idle": giant_bat_left_sprites[0:5],
            "attack": giant_bat_left_attack_sprites[0:6],
            "death": giant_bat_left_death_sprites[0:10],
            "attack2": giant_bat_left_attack2_sprites[0:4]
        }
        self.right_animations = {
            "idle": giant_bat_right_sprites[0:5],
            "attack": giant_bat_right_attack_sprites[0:6],
            "death": giant_bat_right_death_sprites[0:10],
            "attack2": giant_bat_right_attack2_sprites[0:4]
        }
        self.meat = {
            "meat1": meat1,
            "meat2": meat2,
            "meat3": meat3,
            "meat4": meat4,
            "meat5": meat5,
            "meat6": meat6
        }
        
        self.attack_box = giant_bat_attack_box_sprites[0:4]
        
    def update(self, screen):
        if self.direction == "down":
            self.current_sprite = (self.current_sprite + 1) % len(self.down_animations[self.state])
            
        if self.direction == "up":
            self.current_sprite = (self.current_sprite + 1) % len(self.up_animations[self.state])
        
        if self.direction == "left":
            self.current_sprite = (self.current_sprite + 1) % len(self.left_animations[self.state])
    
        if self.direction == "right":
            self.current_sprite = (self.current_sprite + 1) % len(self.right_animations[self.state])
        
    def draw(self, screen):
        if self.alive == True:
            if self.direction == "down":
                screen.blit(self.down_animations[self.state][self.current_sprite], (self.x, self.y))
                
            if self.direction == "up":
                screen.blit(self.up_animations[self.state][self.current_sprite], (self.x, self.y))
                
            if self.direction == "left":
                screen.blit(self.left_animations[self.state][self.current_sprite], (self.x, self.y))
                
            if self.direction == "right":
                screen.blit(self.right_animations[self.state][self.current_sprite], (self.x, self.y))
            
            red = (252, 52, 38)
            rect_thickness = 2
            #pygame.draw.rect(screen, red, self.rect, rect_thickness)
            
    def attack(self, screen):
        if self.current_sprite <= 3:
            screen.blit(self.attack_box[self.current_sprite], (self.x, self.y))
        self.state = "attack"
        self.attack2 = False
    
    def range_attack(self, hero, hero_width, hero_height, offset_x, offset_y, hero_rect):
        # Calculate direction vector from slime to hero
        if self.direction == "right":
            direction_x = hero.x - hero_width / 2 + offset_x - (self.x+50)
            direction_y = hero.y - hero_height / 2 + offset_y - (self.y+25)
        elif self.direction == "left":
            direction_x = hero.x - hero_width / 2 + offset_x - (self.x+25)
            direction_y = hero.y - hero_height / 2 + offset_y - (self.y+25)
        elif self.direction == "up":
            direction_x = hero.x - hero_width / 2 + offset_x - (self.x+50)
            direction_y = hero.y - hero_height / 2 + offset_y - (self.y+25)
        elif self.direction == "down":
            direction_x = hero.x - hero_width / 2 + offset_x - (self.x+25)
            direction_y = hero.y - hero_height / 2 + offset_y - (self.y+25)
            
        self.attack2 = False
        if direction_x < 64 or direction_y < 64 or direction_x > 64 or direction_y > 64:
            # only attack if hero is a certain distance away 
            if direction_x > 32 and direction_y > 32: #and not direction_x > 384 and not direction_y > 384
                self.attack2 = True
                
            elif direction_x < -32 and direction_y < -32: # and not direction_x < -384 and not direction_y < -384
                self.attack2 = True
                
            elif direction_x > 32 and direction_y < -32: #and not direction_x > 384 and not direction_y < -384
                self.attack2 = True
                
            elif direction_x < -32 and direction_y > 32: # and not direction_x < -384 and not direction_y < -384
                self.attack2 = True
            
        if self.state == "attack2" and self.current_sprite == 3:
            if self.rect.colliderect(hero_rect):
                self.state = "attack"
            else:
                self.state = "idle"
        if self.attack2 == True:
            self.state = "attack2"
            if self.current_sprite > 3:
                self.current_sprite = 0    
        
    def end_attack(self):
        self.state = "idle"
        
    def die(self, screen):
        self.state = "death"
        if self.current_sprite == 9:
            self.alive = False
            screen.blit(self.meat["meat1"], (self.x, self.y))
            self.meat_exists = True
            self.meat_num = random.randint(1, 100)
            
    def show_meat(self, screen, hero_rect):
        if self.meat_exists == True:
            if self.meat_num <= 15:
                screen.blit(self.meat["meat1"], (self.x, self.y))
                if hero_rect.colliderect(self.rect):
                    self.meat_exists = False
                    return "meat1"
            elif self.meat_num > 15 and self.meat_num <= 32:
                screen.blit(self.meat["meat2"], (self.x, self.y))
                if hero_rect.colliderect(self.rect):
                    self.meat_exists = False
                    return "meat2"
            elif self.meat_num > 32 and self.meat_num <= 62:
                screen.blit(self.meat["meat3"], (self.x, self.y))
                if hero_rect.colliderect(self.rect):
                    self.meat_exists = False
                    return "meat3"
            elif self.meat_num > 32 and self.meat_num <= 62:
                screen.blit(self.meat["meat4"], (self.x, self.y))
                if hero_rect.colliderect(self.rect):
                    self.meat_exists = False
                    return "meat4"
            elif self.meat_num > 62 and self.meat_num <= 70:
                screen.blit(self.meat["meat5"], (self.x, self.y))
                if hero_rect.colliderect(self.rect):
                    self.meat_exists = False
                    return "meat5"
            elif self.meat_num > 70 and self.meat_num <= 100:
                screen.blit(self.meat["meat6"], (self.x, self.y))
                if hero_rect.colliderect(self.rect):
                    self.meat_exists = False
                    return "meat6"
                
    def change_direction(self, hero_x, hero_y):
        delta_x = hero_x - self.x
        delta_y = hero_y - self.y

        # Calculate the angle between the bat and the hero
        angle = math.atan2(delta_y, delta_x)
        angle_degrees = math.degrees(angle)

        # Determine the direction based on the angle
        if -45 <= angle_degrees <= 45:
            self.direction = "right"
        elif 45 < angle_degrees <= 135:
            self.direction = "down"
        elif -135 <= angle_degrees < -45:
            self.direction = "up"
        else:
            self.direction = "left"

    def move_towards_hero(self, hero, hero_width, hero_height, offset_x, offset_y):
        if self.alive == True:
            # Calculate direction vector from slime to hero
            dir_x = hero.x - hero_width / 2 + offset_x - self.x
            dir_y = hero.y - hero_height / 2 + offset_y - self.y
            
            # avoid moving the giant bat if it is too far away
            if dir_x > 320 and dir_y > 320:
                return
            
            if dir_x < -320 and dir_y < -320:
                return 
            
            # Normalize the direction (get unit vector)
            magnitude = (dir_x**2 + dir_y**2)**0.5
            if magnitude == 0:  # Avoid division by zero
                return
            
            dir_x /= magnitude
            dir_y /= magnitude
            
            # Update the slime's position
            self.move_x += dir_x * self.speed
            self.move_y += dir_y * self.speed

# goblin class
goblin_down_sprites = []
goblin_up_sprites = []
goblin_left_sprites = []
goblin_right_sprites = []

goblin_down_attack_sprites = []
goblin_up_attack_sprites = []
goblin_left_attack_sprites = []
goblin_right_attack_sprites = []

goblin_down_move_sprites = []
goblin_up_move_sprites = []
goblin_left_move_sprites = []
goblin_right_move_sprites = []

goblin_down_death_sprites = []
goblin_left_death_sprites = []
goblin_up_death_sprites = []
goblin_right_death_sprites = []

goblin_down = pygame.image.load('goblin/Down/Png/GoblinDownIdle.png')
goblin_up = pygame.image.load('goblin/Up/Png/GoblinUpIdle.png')
goblin_left = pygame.image.load('goblin/Left/Png/GoblinLeftIdle.png')
goblin_right = pygame.image.load('goblin/Right/Png/GoblinRightIdle.png')

goblin_attack_down = pygame.image.load('goblin/Down/Png/GoblinDownAttack01.png')
goblin_attack_up = pygame.image.load('goblin/Up/Png/GoblinUpAttack01.png')
goblin_attack_left = pygame.image.load('goblin/Left/Png/GoblinLeftAttack01.png')
goblin_attack_right = pygame.image.load('goblin/Right/Png/GoblinRightAttack01.png')

goblin_move_down = pygame.image.load('goblin/Down/Png/GoblinDownRun.png')
goblin_move_up = pygame.image.load('goblin/Up/Png/GoblinUpRun.png')
goblin_move_left = pygame.image.load('goblin/Left/Png/GoblinLeftRun.png')
goblin_move_right = pygame.image.load('goblin/Right/Png/GoblinRightRun.png')

goblin_death_down = pygame.image.load('goblin/Down/Png/GoblinDownDeath.png')
goblin_death_up = pygame.image.load('goblin/Up/Png/GoblinUpDeath.png')
goblin_death_left = pygame.image.load('goblin/Left/Png/GoblinLeftDeath.png')
goblin_death_right = pygame.image.load('goblin/Right/Png/GoblinRightDeath.png')

cut_spritesheet(goblin_left_sprites, goblin_left, 48, 48, 0, 0)
cut_spritesheet(goblin_right_sprites, goblin_right, 48, 48, 0, 0)
cut_spritesheet(goblin_up_sprites, goblin_up, 48, 48, 0, 0)
cut_spritesheet(goblin_down_sprites, goblin_down, 48, 48, 0, 0)

cut_spritesheet(goblin_left_attack_sprites, goblin_attack_left, 48, 48, 0, 0)
cut_spritesheet(goblin_right_attack_sprites, goblin_attack_right, 48, 48, 0, 0)
cut_spritesheet(goblin_up_attack_sprites, goblin_attack_up, 48, 48, 0, 0)
cut_spritesheet(goblin_down_attack_sprites, goblin_attack_down, 48, 48, 0, 0)


cut_spritesheet(goblin_left_move_sprites, goblin_move_left, 48, 48, 0, 0)
cut_spritesheet(goblin_right_move_sprites, goblin_move_right, 48, 48, 0, 0)
cut_spritesheet(goblin_up_move_sprites, goblin_move_up, 48, 48, 0, 0)
cut_spritesheet(goblin_down_move_sprites, goblin_move_down, 48, 48, 0, 0)

cut_spritesheet(goblin_left_death_sprites, goblin_death_left, 48, 48, 0, 0)
cut_spritesheet(goblin_right_death_sprites, goblin_death_right, 48, 48, 0, 0)
cut_spritesheet(goblin_up_death_sprites, goblin_death_up, 48, 48, 0, 0)
cut_spritesheet(goblin_down_death_sprites, goblin_death_down, 48, 48, 0, 0)

class Goblin:
    def __init__(self, x, y, offset_x, offset_y):
        self.width = 48
        self.height = 48
        self.speed = 16
        self.move_x = 0
        self.move_y = 0
        self.x = offset_x + x + self.move_x
        self.y = offset_y + y + self.move_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = "down"
        self.state = "idle"
        self.current_sprite = 0
        self.alive = True
        self.meat_exists = False
        self.meat_num = None
        
        self.down_animations = {
            "idle": goblin_down_sprites[0:6],
            "attack": goblin_down_attack_sprites[0:10],
            "move": goblin_down_move_sprites[0:6],
            "death": goblin_down_death_sprites[0:8]
        }
        self.up_animations = {
            "idle": goblin_up_sprites[0:6],
            "attack": goblin_up_attack_sprites[0:10],
            "move": goblin_up_move_sprites[0:6],
            "death": goblin_up_death_sprites[0:8]
        }
        self.left_animations = {
            "idle": goblin_left_sprites[0:6],
            "attack": goblin_left_attack_sprites[0:10],
            "move": goblin_left_sprites[0:6],
            "death": goblin_left_death_sprites[0:8]
        }
        self.right_animations = {
            "idle": goblin_right_sprites[0:6],
            "attack": goblin_right_attack_sprites[0:10],
            "move": goblin_right_move_sprites[0:6],
            "death": goblin_right_death_sprites[0:8]
        }
    def update(self, screen):
        if self.direction == "down":
            self.current_sprite = (self.current_sprite + 1) % len(self.down_animations[self.state])
            
        if self.direction == "up":
            self.current_sprite = (self.current_sprite + 1) % len(self.up_animations[self.state])
        
        if self.direction == "left":
            self.current_sprite = (self.current_sprite + 1) % len(self.left_animations[self.state])
    
        if self.direction == "right":
            self.current_sprite = (self.current_sprite + 1) % len(self.right_animations[self.state])
        
    def draw(self, screen):
        if self.alive == True:
            if self.direction == "down":
                screen.blit(self.down_animations[self.state][self.current_sprite], (self.x, self.y))
                
            if self.direction == "up":
                screen.blit(self.up_animations[self.state][self.current_sprite], (self.x, self.y))
                
            if self.direction == "left":
                screen.blit(self.left_animations[self.state][self.current_sprite], (self.x, self.y))
                
            if self.direction == "right":
                screen.blit(self.right_animations[self.state][self.current_sprite], (self.x, self.y))
            
            red = (252, 52, 38)
            rect_thickness = 2
            #pygame.draw.rect(screen, red, self.rect, rect_thickness)
    
    def change_direction(self, hero_x, hero_y):
        delta_x = hero_x - self.x
        delta_y = hero_y - self.y

        # Calculate the angle between the bat and the hero
        angle = math.atan2(delta_y, delta_x)
        angle_degrees = math.degrees(angle)

        # Determine the direction based on the angle
        if -45 <= angle_degrees <= 45:
            self.direction = "right"
        elif 45 < angle_degrees <= 135:
            self.direction = "down"
        elif -135 <= angle_degrees < -45:
            self.direction = "up"
        else:
            self.direction = "left"

    def move_towards_hero(self, hero, hero_width, hero_height, offset_x, offset_y):
        if self.alive == True:
            # Calculate direction vector from slime to hero
            dir_x = hero.x - hero_width / 2 + offset_x - self.x
            dir_y = hero.y - hero_height / 2 + offset_y - self.y
            
            # avoid moving the giant bat if it is too far away
            if dir_x > 320 and dir_y > 320:
                return
            
            if dir_x < -320 and dir_y < -320:
                return 
            
            # Normalize the direction (get unit vector)
            magnitude = (dir_x**2 + dir_y**2)**0.5
            if magnitude == 0:  # Avoid division by zero
                return
            
            dir_x /= magnitude
            dir_y /= magnitude
            
            # Update the slime's position
            self.move_x += dir_x * self.speed
            self.move_y += dir_y * self.speed
    
    def attack(self):
        self.state = "attack"

    def end_attack(self):
        self.state = "idle"

    def die(self, screen):
        self.state = "death"
        if self.current_sprite == 7:
            self.alive = False

# goblin beast class
goblin_beast_down_sprites = []
goblin_beast_up_sprites = []
goblin_beast_left_sprites = []
goblin_beast_right_sprites = []

goblin_beast_down_attack_sprites = []
goblin_beast_up_attack_sprites = []
goblin_beast_left_attack_sprites = []
goblin_beast_right_attack_sprites = []

goblin_beast_down_move_sprites = []
goblin_beast_up_move_sprites = []
goblin_beast_left_move_sprites = []
goblin_beast_right_move_sprites = []

goblin_beast_down_death_sprites = []
goblin_beast_left_death_sprites = []
goblin_beast_up_death_sprites = []
goblin_beast_right_death_sprites = []

goblin_beast_down = pygame.image.load('goblin_beast/Down/Png/GoblinBeastDownIdle.png')
goblin_beast_up = pygame.image.load('goblin_beast/Up/Png/GoblinBeastUpIdle.png')
goblin_beast_left = pygame.image.load('goblin_beast/Left/Png/GoblinBeastLeftIdle.png')
goblin_beast_right = pygame.image.load('goblin_beast/Right/Png/GoblinBeastRightIdle.png')

goblin_beast_attack_down = pygame.image.load('goblin_beast/Down/Png/GoblinBeastDownAttack01.png')
goblin_beast_attack_up = pygame.image.load('goblin_beast/Up/Png/GoblinBeastUpAttack01.png')
goblin_beast_attack_left = pygame.image.load('goblin_beast/Left/Png/GoblinBeastLeftAttack01.png')
goblin_beast_attack_right = pygame.image.load('goblin_beast/Right/Png/GoblinBeastRightAttack01.png')

goblin_beast_move_down = pygame.image.load('goblin_beast/Down/Png/GoblinBeastDownWalk.png')
goblin_beast_move_up = pygame.image.load('goblin_beast/Up/Png/GoblinBeastUpWalk.png')
goblin_beast_move_left = pygame.image.load('goblin_beast/Left/Png/GoblinBeastLeftWalk.png')
goblin_beast_move_right = pygame.image.load('goblin_beast/Right/Png/GoblinBeastRightWalk.png')

goblin_beast_death_down = pygame.image.load('goblin_beast/Down/Png/GoblinBeastDownDeath.png')
goblin_beast_death_up = pygame.image.load('goblin_beast/Up/Png/GoblinBeastUpDeath.png')
goblin_beast_death_left = pygame.image.load('goblin_beast/Left/Png/GoblinBeastLeftDeath.png')
goblin_beast_death_right = pygame.image.load('goblin_beast/Right/Png/GoblinBeastRightDeath.png')

cut_spritesheet(goblin_beast_left_sprites, goblin_beast_left, 48, 48, 0, 0)
cut_spritesheet(goblin_beast_right_sprites, goblin_beast_right, 48, 48, 0, 0)
cut_spritesheet(goblin_beast_up_sprites, goblin_beast_up, 48, 48, 0, 0)
cut_spritesheet(goblin_beast_down_sprites, goblin_beast_down, 48, 48, 0, 0)

cut_spritesheet(goblin_beast_left_attack_sprites, goblin_beast_attack_left, 64, 64, 0, 0)
cut_spritesheet(goblin_beast_right_attack_sprites, goblin_beast_attack_right, 64, 64, 0, 0)
cut_spritesheet(goblin_beast_up_attack_sprites, goblin_beast_attack_up, 64, 64, 0, 0)
cut_spritesheet(goblin_beast_down_attack_sprites, goblin_beast_attack_down, 64, 64, 0, 0)

cut_spritesheet(goblin_beast_left_move_sprites, goblin_beast_move_left, 48, 48, 0, 0)
cut_spritesheet(goblin_beast_right_move_sprites, goblin_beast_move_right, 48, 48, 0, 0)
cut_spritesheet(goblin_beast_up_move_sprites, goblin_beast_move_up, 48, 48, 0, 0)
cut_spritesheet(goblin_beast_down_move_sprites, goblin_beast_move_down, 48, 48, 0, 0)

cut_spritesheet(goblin_beast_left_death_sprites, goblin_beast_death_left, 48, 48, 0, 0)
cut_spritesheet(goblin_beast_right_death_sprites, goblin_beast_death_right, 48, 48, 0, 0)
cut_spritesheet(goblin_beast_up_death_sprites, goblin_beast_death_up, 48, 48, 0, 0)
cut_spritesheet(goblin_beast_down_death_sprites, goblin_beast_death_down, 48, 48, 0, 0)

class Goblin_Beast:
    def __init__(self, x, y, offset_x, offset_y):
        self.width = 48
        self.height = 48
        self.speed = 16
        self.move_x = 0
        self.move_y = 0
        self.x = offset_x + x + self.move_x
        self.y = offset_y + y + self.move_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = "down"
        self.state = "idle"
        self.current_sprite = 0
        self.alive = True
        self.meat_exists = False
        self.meat_num = None
        
        self.down_animations = {
            "idle": goblin_beast_down_sprites[0:6],
            "attack": goblin_beast_down_attack_sprites[0:8],
            "move": goblin_beast_down_move_sprites[0:6],
            "death": goblin_beast_down_death_sprites[0:8]
        }
        self.up_animations = {
            "idle": goblin_beast_up_sprites[0:6],
            "attack": goblin_beast_up_attack_sprites[0:8],
            "move": goblin_beast_up_move_sprites[0:6],
            "death": goblin_beast_up_death_sprites[0:8]
        }
        self.left_animations = {
            "idle": goblin_beast_left_sprites[0:6],
            "attack": goblin_beast_left_attack_sprites[0:8],
            "move": goblin_beast_left_sprites[0:6],
            "death": goblin_beast_left_death_sprites[0:8]
        }
        self.right_animations = {
            "idle": goblin_beast_right_sprites[0:6],
            "attack": goblin_beast_right_attack_sprites[0:8],
            "move": goblin_beast_right_move_sprites[0:6],
            "death": goblin_beast_right_death_sprites[0:8]
        }

    def update(self, screen):
        if self.direction == "down":
            self.current_sprite = (self.current_sprite + 1) % len(self.down_animations[self.state])
            
        if self.direction == "up":
            self.current_sprite = (self.current_sprite + 1) % len(self.up_animations[self.state])
        
        if self.direction == "left":
            self.current_sprite = (self.current_sprite + 1) % len(self.left_animations[self.state])
    
        if self.direction == "right":
            self.current_sprite = (self.current_sprite + 1) % len(self.right_animations[self.state])
        
    def draw(self, screen):
        if self.alive == True:
            if self.direction == "down":
                screen.blit(self.down_animations[self.state][self.current_sprite], (self.x, self.y))
                
            if self.direction == "up":
                screen.blit(self.up_animations[self.state][self.current_sprite], (self.x, self.y))
                
            if self.direction == "left":
                screen.blit(self.left_animations[self.state][self.current_sprite], (self.x, self.y))
                
            if self.direction == "right":
                screen.blit(self.right_animations[self.state][self.current_sprite], (self.x, self.y))
            
            red = (252, 52, 38)
            rect_thickness = 2
            #pygame.draw.rect(screen, red, self.rect, rect_thickness)

    def change_direction(self, hero_x, hero_y):
        delta_x = hero_x - self.x
        delta_y = hero_y - self.y

        # Calculate the angle between the bat and the hero
        angle = math.atan2(delta_y, delta_x)
        angle_degrees = math.degrees(angle)

        # Determine the direction based on the angle
        if -45 <= angle_degrees <= 45:
            self.direction = "right"
        elif 45 < angle_degrees <= 135:
            self.direction = "down"
        elif -135 <= angle_degrees < -45:
            self.direction = "up"
        else:
            self.direction = "left"

    def move_towards_hero(self, hero, hero_width, hero_height, offset_x, offset_y):
        if self.alive == True:
            # Calculate direction vector from slime to hero
            dir_x = hero.x - hero_width / 2 + offset_x - self.x
            dir_y = hero.y - hero_height / 2 + offset_y - self.y
            
            # avoid moving the giant bat if it is too far away
            if dir_x > 320 and dir_y > 320:
                return
            
            if dir_x < -320 and dir_y < -320:
                return 
            
            # Normalize the direction (get unit vector)
            magnitude = (dir_x**2 + dir_y**2)**0.5
            if magnitude == 0:  # Avoid division by zero
                return
            
            dir_x /= magnitude
            dir_y /= magnitude
            
            # Update the slime's position
            self.move_x += dir_x * self.speed
            self.move_y += dir_y * self.speed

    def attack(self):
        self.state = "attack"

    def end_attack(self):
        self.state = "idle"

    def die(self, screen):
        self.state = "death"
        if self.current_sprite == 7:
            self.alive = False
            
# button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        if self.is_over(pygame.mouse.get_pos()):
            if self.color != None:
                pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height), 0)
        elif self.color != None:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        font = pygame.font.SysFont('Press Start 2P', 30)
        text = font.render(self.text, 1, self.text_color)
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        if self.is_over(pygame.mouse.get_pos()) and self.color == None: # if there is no background color and mouse if over button, draw the text as the hover color
            screen.blit(font.render(self.text, 1, self.hover_color), (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        # Returns True if mouse position is over the button
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False
    
    def change_text(self, new_text):
        self.text = new_text

# stamina bar class
class Stamina_Bar:
    def __init__(self, x, y, width, height, max_stamina, is_in_water, stamina_display, oxygen_display, arrow_display):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_stamina = max_stamina
        self.current_stamina = max_stamina
        self.is_in_water = False
        self.arrow_is_shooting = False
        self.arrow_display = arrow_display
        self.oxygen_display = oxygen_display
        self.stamina_display = stamina_display
        self.text_display = None
        
    def reduce_stamina(self, amount):
        self.current_stamina -= amount
        if self.current_stamina < 0:
            self.current_stamina = 0

    def increase_stamina(self, amount):
        self.current_stamina += amount
        if self.current_stamina > self.max_stamina:
            self.current_stamina = self.max_stamina
    
    def _calculate_color(self, is_in_water, is_shooting_arrows):
        if is_shooting_arrows == True:
            self.text_display = self.arrow_display
            return 'orange'
        if is_in_water == True:
            self.text_display = self.oxygen_display
            return 'blue'
        else:
            self.text_display = self.stamina_display
            return 'green'
    
    def draw(self, screen):
        #pygame.draw.rect(screen, (255, 0, 0), (50, 50, 50, 50))
        # Draw the background
        pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.width, self.height))
        
        # Calculate the current width of the bar based on the stamina percentage
        current_width = (self.current_stamina / self.max_stamina) * self.width
        
        color = (0, 255, 0)
        color_result = self._calculate_color(self.is_in_water, self.arrow_is_shooting)
        if color_result == 'blue':
            color = (49, 111, 224)
        elif color_result == 'green':
            color = (0, 255, 0)
        elif color_result == 'orange':
            color = (252, 143, 78)
        
        # Draw the current stamina
        pygame.draw.rect(screen, color, (self.x, self.y, current_width, self.height))
        screen.blit(self.text_display, (self.x, self.y - 3))

# health bar class
class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.low_health = max_health / 8
        self.visible = True

    def _calculate_color(self):
        if self.current_health == self.max_health:
            return (0, 255, 0)
        if self.low_health < self.current_health < self.max_health:
            return (255, 0, 0)
        if self.current_health <= self.low_health:
            return (0, 0, 0)

    def reduce_health(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def increase_health(self, amount):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def draw(self, screen):
        if self.visible == True:
            # Draw the background
            pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.width, self.height))
            
            # Calculate the current width of the health bar based on the health percentage
            current_width = (self.current_health / self.max_health) * self.width
            
            # Get the color
            color = self._calculate_color()
            
            # Draw the current health with the calculated color
            pygame.draw.rect(screen, color, (self.x, self.y, current_width, self.height))
    
    def dissapear(self):
        self.visible = False

# arrow class
arrow_sprites = []
arrow = pygame.image.load('arrow.png')
cut_spritesheet(arrow_sprites, arrow, 32, 32, 0, 0)

spear_sprites = []
spear = pygame.image.load('spear.png')
cut_spritesheet(spear_sprites, spear, 22, 22, 0, 0)

class Arrow:
    def __init__(self, x, y, offset_x, offset_y, direction, state):
        self.speed = 24
        self.move_x = 0
        self.move_y = 0
        self.state = state
        if self.state == "normal":
            self.width = 32
            self.height = 32
        elif self.state == "spear":
            self.width = 22
            self.height = 22
        self.x = x + self.move_x
        self.y = y + self.move_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = direction
        self.exists = False
        self.down_images = {
            "normal": arrow_sprites[3],
            "spear": spear_sprites[1]
            }
        self.up_images = {
            "normal": arrow_sprites[2],
            "spear": spear_sprites[0]
            }
        self.left_images = {
            "normal": arrow_sprites[1],
            "spear": spear_sprites[3]
            }
        self.right_images = {
            "normal": arrow_sprites[0],
            "spear": spear_sprites[2]
            }
        
    def draw(self, screen, direction):
        if self.exists == True:
            if direction == "down":
                screen.blit(self.down_images[self.state], (self.x, self.y))
            if direction == "up":
                screen.blit(self.up_images[self.state], (self.x, self.y))
            if direction == "left":
                screen.blit(self.left_images[self.state], (self.x, self.y))
            if direction == "right":
               screen.blit(self.right_images[self.state], (self.x, self.y))
            #pygame.draw.rect(screen, (252, 143, 78), self.rect, 1)
            
    def update(self, direction):
        if self.exists == True:
            if self.direction == "down":
                self.move_y += self.speed
            elif self.direction == "up":
                self.move_y -= self.speed
            elif self.direction == "left":
                self.move_x -= self.speed
            elif self.direction == "right":
                self.move_x += self.speed
                
            self.x += self.move_x
            self.y += self.move_y
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            
    def check_collision(self, blue_slime_rect, green_slime_rect, red_slime_rect, giant_bat_rect, hero_rect):
        if self.rect.colliderect(blue_slime_rect):
            return "blue_slime"
        if self.rect.colliderect(red_slime_rect):
            return "red_slime"
        if self.rect.colliderect(green_slime_rect):
            return "green_slime"
        if self.rect.colliderect(giant_bat_rect):
            return "giant_bat"
        if self.rect.colliderect(hero_rect):
            return "hero"
# item class
class item:
    def __init__(type):
        self.type = type
        if self.type == "shell":
            self.value = 8
            self.use = ["blow", "sell", "drop"]
        if self.type == "pearl":
            self.value = 5
            self.use = ["drow", "sell"]
        if self.type == "crown":
            self.value = 15
            self.use = ["wear", "take_off", "drop", "sell"]
        if self.type == "helmet":
            self.value = 22
            self.use = ["wear", "take_off", "drop", "sell"]
        if self.type == "sword":
            self.value = 18
            self.use = ["drop", "sell"]
        if self.type == "necklace":
            self.value = 5
            self.use = ["wear", "take_off", "drop", "sell"]
        if self.type == "ring":
            self.value = 3
            self.use = ["wear", "take_off", "drop", "sell"]
        if self.type == "potion":
            self.value = 6
            self.use = ["drink", "drop", "sell"]
        if self.type == "arrow":
            self.value = 1
            self.use = ["drop", "sell"]
        