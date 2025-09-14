import pygame
import pytmx
import random
from playsound import playsound
from threading import Thread
from game_classes_and_functions import *

pygame.init()
pygame.mixer.init()
pygame.font.init()

screen_width, screen_height = 1008, 640
camera = pygame.Rect(0, 0, screen_width, screen_height)

offset_x = 0
offset_y = 0
hero_rect = hero_img.get_rect()
hero_width = 48
hero_height = 64     
hero_speed = 16

blue_slime_x = random.randint(48, 1936)
blue_slime_y = random.randint(48, 1200)

green_slime_x = random.randint(48, 1936)
green_slime_y = random.randint(48, 1200)

red_slime_x = random.randint(48, 1936)
red_slime_y = random.randint(48, 1200)

giant_bat_x = random.randint(48, 1936)
giant_bat_y = random.randint(48, 1200)

goblin_x = random.randint(48, 1200)
goblin_y = goblin_x

goblin_beast_x = random.randint(48, 1936)
goblin_beast_y = goblin_beast_x

gems = 0
max_stamina = 100
mute = False
music_is_playing = True

turquoise = (2, 250, 205)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
light_blue = (2, 238, 250)

font = pygame.font.SysFont('Press Start 2P', 30)
small_font = pygame.font.SysFont('Lexend', 20)

music = pygame.mixer.Sound('forest_music.mp3')

################### ## ######## ##### ## ###################
#########⬇️######## -> FUNCTION STUFF <- #########⬇️########

current_map = "map-new.tmx"

#hero = Player(880, 1600, 300)
hero = Player(58*32, 46*32, 300)

blue_slime_width = 128
blue_slime_height = 128
green_slime_width = 128
green_slime_height = 128
red_slime_width = 128
red_slime_height = 128

giant_bat_width = 80
giant_bat_height = 80

direction = "down"
shift_key_down = False
space_key_down = False
stamina_depleted = False
attacking = False
def handle_input():
    global direction
    global hero_speed
    global shift_key_down
    global space_key_down
    global stamina_depleted
    global attacking
    map_width = tm.width * (tm.tilewidth * 2)
    map_height = tm.height * (tm.tileheight * 2)
    #if current_map == "map-new.tmx":
        #map_width = 2528
        #map_height = 1760
    #elif current_map == "shop.tmx":
        #map_width = 960
        #map_height = 608
    keys = pygame.key.get_pressed()
    moving_left = False
    moving_right = False
    moving_forwards = False
    moving_down = False
    attacking = False
    moving = False
    shift_key_down = False
    x_move = y_move = 0
    if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
        shift_key_down = True
    if keys[pygame.K_LEFT]:
        x_move = - hero_speed
        moving_left = True
        moving = True
    if keys[pygame.K_RIGHT]:
        x_move = hero_speed
        moving_right = True
        moving = True
    if keys[pygame.K_UP]:
        y_move = - hero_speed
        moving_forwards = True
        moving = True
    if keys[pygame.K_DOWN]:
        y_move = hero_speed
        moving_down = True
        moving = True
    if keys[pygame.K_SPACE] and moving == False and shift_key_down == False:
        attacking = True
        Thread(target = lambda: play_sound('attack_woosh.mp3', mute, music, music_is_playing)).start()
    if keys[pygame.K_SPACE]:
        space_key_down = True
    else:
        space_key_down = False
    if not keys[pygame.K_LEFT] or not keys[pygame.K_RIGHT] or not keys[pygame.K_UP] or not keys[pygame.K_DOWN]:
        moving = False
    
    # Predict the next position of the hero
    predicted_x = hero.x + x_move
    predicted_y = hero.y + y_move
    
    # Check if predicted positions are within the map boundary
    if predicted_x < 0 or predicted_x > map_width - hero_width:
        x_move = 0

    if predicted_y < 0 or predicted_y > map_height - hero_height:
        y_move = 0

    next_rect = pygame.Rect(predicted_x, predicted_y, hero_width, hero_height)
    # Check if there will be a collision in the next position
    # Refactored collision check
    if not will_collide(next_rect, tm, "wall"):
        hero.x += x_move
        hero.y += y_move
        
    if moving_left and not will_collide(next_rect, tm, "wall"):
        hero.state = "moving_left"
        direction = "left"
        if shift_key_down and stamina_depleted == False:
            hero_speed = 24
    elif moving_right and not will_collide(next_rect, tm, "wall"):
        hero.state = "moving_right"
        direction = "right"
        if shift_key_down and stamina_depleted == False:
            hero_speed = 24
    elif moving_forwards and not will_collide(next_rect, tm, "wall"):
        hero.state = "moving_up"
        direction = "up"
        if shift_key_down and stamina_depleted == False:
            hero_speed = 24
    elif moving_down and not will_collide(next_rect, tm, "wall"):
        hero.state = "moving_down"
        direction = "down"
        if shift_key_down and stamina_depleted == False:
            hero_speed = 24
    
    elif attacking and direction == "down":
        hero.state = "attacking_down"
    elif attacking and direction == "left":
        hero.state = "attacking_left"
    elif attacking and direction == "right":
        hero.state = "attacking_right"
    elif attacking and direction == "up":
        hero.state = "attacking_up"
        
    elif direction == "up":
        hero.state = "idle_up"
    elif direction == "left":
        hero.state = "idle_left"
    elif direction == "right":
        hero.state = "idle_right"
    elif direction == "down":
        hero.state = "idle_down"
        
    if shift_key_down == False or stamina_depleted == True:
        hero_speed = 16

def will_collide(next_rect, tilemap, wall_or_water):
    if current_map == "map-new.tmx":
        layer = tilemap.layers[2]
        for x, y, gid in layer:
            tile_properties = tilemap.get_tile_properties_by_gid(gid)
            tile_rect = pygame.Rect(x * tilemap.tilewidth * 2, y * tilemap.tileheight * 2, tilemap.tilewidth, tilemap.tileheight)
            
            if next_rect.colliderect(tile_rect) and tile_properties:
                if tile_properties.get('is_wall') and wall_or_water == "wall":
                    return True
                if tile_properties.get('is_water') and wall_or_water == "water":
                    return True
        return False

open_treasure_chests = set()
removed_collectables = set()
collision_tiles = []
collision_direction = None
on_counter = False
def check_collision(hero_rect, hero_bottom_rect, tilemap):
    global collision_tiles
    global collision_direction
    tw = 32
    th = 32
    if current_map == "map-new.tmx":
        layer = tilemap.layers[2]
        collision_tiles = []
        for x, y, gid in layer:
            tile_properties = tilemap.get_tile_properties_by_gid(gid)
            tile_rect = pygame.Rect(x * tw + offset_x, y * th + offset_y, tw, th)
            if hero_rect.colliderect(tile_rect): # Only check collision with the tiles colliding with the hero
                if tile_properties and hero_rect.colliderect(tile_rect):
                    if tile_properties.get('is_treasure_chest') and (x, y) not in open_treasure_chests:
                        open_treasure_chests.add((x, y))
                        collision_tiles.append("treasure_chest")
                    
                    elif tile_properties.get('is_blue_gem') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("blue_gem")
                        
                    elif tile_properties.get('is_red_gems') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("red_gems")
                        
                    elif tile_properties.get('is_bag_of_coins') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("bag_of_coins")
                        
                    elif tile_properties.get('is_ring') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("ring")
                        
                    elif tile_properties.get('is_three_pearls') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("three_pearls")
                        
                    elif tile_properties.get('is_single_pearl') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("single_pearl")
                        
                    elif tile_properties.get('is_necklace') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("necklace")
                        
                    elif tile_properties.get('is_crown') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("crown")
                        
                    elif tile_properties.get('is_arrow') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("arrow")
                        
                    elif tile_properties.get('is_shell') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("shell")
                    
                    elif tile_properties.get('is_potion') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("potion")
                        
                    elif tile_properties.get('is_helmet') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("helmet")
                        
                    elif tile_properties.get('is_map') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("map")
                        
                    elif tile_properties.get('is_sword') and tile_properties.get('is_collectable') and (x, y) not in removed_collectables:
                        removed_collectables.add((x, y))
                        collision_tiles.append("sword")
                    
                    # shop collision
                    elif tile_properties.get('is_dirt'):
                        collision_tiles.append('shop')
                    
                    elif hero_bottom_rect.colliderect(tile_rect):     
                        if tile_properties.get('is_water'):
                            collision_tiles.append("water")
                    
                    
                if tile_properties and green_slime.rect.colliderect(tile_rect):
                    if tile_properties.get('is_water'):
                        collision_direction = None

                        # Check which side of the green_slime_rect the tile_rect is touching:
                        if tile_rect.top < green_slime.rect.top and tile_rect.bottom > green_slime.rect.top:
                            collision_direction = "top"
                        elif tile_rect.bottom > green_slime.rect.bottom and tile_rect.top < green_slime.rect.bottom:
                            collision_direction = "bottom"
                        elif tile_rect.left < green_slime.rect.left and tile_rect.right > green_slime.rect.left:
                            collision_direction = "left"
                        elif tile_rect.right > green_slime.rect.right and tile_rect.left < green_slime.rect.right:
                            collision_direction = "right"
                            
                        if collision_direction:
                            collision_tiles.append(f"green_slime-water-{collision_direction}")
                        else:
                            collision_tiles.append("green_slime-water")
                
                    if tile_properties.get('is_wall'):
                        collision_direction = None
                        # Check which side of the green_slime_rect the tile_rect is touching:
                        if tile_rect.top < green_slime.rect.top and tile_rect.bottom > green_slime.rect.top:
                            collision_direction = "top"
                        elif tile_rect.bottom > green_slime.rect.bottom and tile_rect.top < green_slime.rect.bottom:
                            collision_direction = "bottom"
                        elif tile_rect.left < green_slime.rect.left and tile_rect.right > green_slime.rect.left:
                            collision_direction = "left"
                        elif tile_rect.right > green_slime.rect.right and tile_rect.left < green_slime.rect.right:
                            collision_direction = "right"
                            
                        if collision_direction:
                            collision_tiles.append(f"green_slime-wall-{collision_direction}")
                        else:
                            collision_tiles.append("green_slime-wall")  
                else:
                    collision_tiles.append("green_slime-nothing")
                
                if tile_properties and red_slime.rect.colliderect(tile_rect):
                    if tile_properties.get('is_water'):
                        collision_direction = None

                        # Check which side of the red_slime.rect the tile_rect is touching:
                        if tile_rect.top < red_slime.rect.top and tile_rect.bottom > red_slime.rect.top:
                            collision_direction = "top"
                        elif tile_rect.bottom > red_slime.rect.bottom and tile_rect.top < red_slime.rect.bottom:
                            collision_direction = "bottom"
                        elif tile_rect.left < red_slime.rect.left and tile_rect.right > red_slime.rect.left:
                            collision_direction = "left"
                        elif tile_rect.right > red_slime.rect.right and tile_rect.left < red_slime.rect.right:
                            collision_direction = "right"
                            
                        if collision_direction:
                            collision_tiles.append(f"red_slime-water-{collision_direction}")
                        else:
                            collision_tiles.append("red_slime-water")
                            
                    if tile_properties.get('is_wall'):
                        collision_direction = None
                        
                        # Check which side of the red_slime.rect the tile_rect is touching:
                        if tile_rect.top < red_slime.rect.top and tile_rect.bottom > red_slime.rect.top:
                            collision_direction = "top"
                        elif tile_rect.bottom > red_slime.rect.bottom and tile_rect.top < red_slime.rect.bottom:
                            collision_direction = "bottom"
                        elif tile_rect.left < red_slime.rect.left and tile_rect.right > red_slime.rect.left:
                            collision_direction = "left"
                        elif tile_rect.right > red_slime.rect.right and tile_rect.left < red_slime.rect.right:
                            collision_direction = "right"
                            
                        if collision_direction:
                            collision_tiles.append(f"red_slime-wall-{collision_direction}")
                        else:
                            collision_tiles.append("red_slime-wall")      
                else:
                    collision_tiles.append("red_slime-nothing")

                if tile_properties and blue_slime.rect.colliderect(tile_rect):
                    if tile_properties.get('is_water'):
                        collision_tiles.append("blue_slime-water")

                if hero_rect.colliderect(blue_slime.rect):
                    collision_tiles.append("blue_slime")
                if hero_rect.colliderect(green_slime.rect):
                    collision_tiles.append("green_slime")
                if hero_rect.colliderect(red_slime.rect):
                    collision_tiles.append("red_slime")
                if hero_rect.colliderect(giant_bat.rect):
                    collision_tiles.append("giant_bat")
                if hero_rect.colliderect(goblin.rect):
                    collision_tiles.append("goblin")
                if hero_rect.colliderect(goblin_beast.rect):
                    collision_tiles.append("goblin_beast")
      
    if current_map == "shop.tmx":
        layer2 = tilemap.layers[1]
        for x, y, gid in layer2:
            tile_properties = tilemap.get_tile_properties_by_gid(gid)
            tile_rect = pygame.Rect(x * tw + offset_x, y * th + offset_y, tw, th)
            if tile_properties and hero_rect.colliderect(tile_rect):
                if tile_properties.get('is_white_tile'):
                    collision_tiles.append("shop_exit")
                if tile_properties.get('is_wood'):
                    collision_tiles.append("shop_counter")
                if tile_properties.get('is_buyable'):
                    removed_collectables.add((x, y))
                    if tile_properties.get('is_arrow'):
                        collision_tiles.append("buyable_arrow")
                    if tile_properties.get('is_helmet'):
                        collision_tiles.append("buyable_helmet")
                    if tile_properties.get('is_potion'):
                        collision_tiles.append("buyable_potion")
                    if tile_properties.get('is_sword'):
                        collision_tiles.append("buyable_sword")
                    if tile_properties.get('is_map'):
                        collision_tiles.append("buyable_map")
                    if tile_properties.get('is_shell'):
                        collision_tiles.append("buyable_shell")
    
    return collision_tiles

def draw_objects(screen, tm):
    tw = 32
    th = 32
    if current_map == "map-new.tmx":
        layer2 = tm.layers[1]
        layer3 = tm.layers[0]
    for layer in tm.layers:
        if isinstance(layer, pytmx.TiledObjectGroup):
            for obj in layer:
                if obj.image:
                    obj_image = pygame.transform.scale(obj.image, (int(obj.width * 2), int(obj.height * 2)))
                    screen.blit(obj_image, (obj.x * 2 + offset_x, obj.y * 2 + offset_y))
                else:
                    pygame.draw.rect(surface, (255, 0, 0), (obj.x + offset_x, obj.y + offset_y, obj.width, obj.height), 2)

def draw_tiles(screen, tm):
    tw = 32
    th = 32
    if current_map == "map-new.tmx":
        layer2 = tm.layers[1]
        layer3 = tm.layers[0]
    for layer in tm.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                if layer.name == "collision tiles" and (x, y) in open_treasure_chests:
                    gid = layer2.data[21][5]
                    tile_image = tm.get_tile_image_by_gid(gid)
                    big_tile_image = pygame.transform.scale(tile_image, (32, 32))
                    blit_position = (x * tw + offset_x, y * th + offset_y)
                    screen.blit(big_tile_image, blit_position)
                elif layer.name == "collision tiles" and (x, y) in removed_collectables and current_map == "map-new.tmx":
                    gid = layer3.data[2][2]
                    tile_image = tm.get_tile_image_by_gid(gid)
                    big_tile_image = pygame.transform.scale(tile_image, (32, 32))
                    blit_position = (x * tw + offset_x, y * th + offset_y)
                    screen.blit(big_tile_image, blit_position)
                else:
                    tile = tm.get_tile_image_by_gid(gid)
                    if tile:
                        tile_rect = pygame.Rect(x * tw + offset_x, y * th + offset_y, tw, th)
                        if camera.colliderect(tile_rect): # Only draw if the tile is within the camera's view
                            big_tile = pygame.transform.scale(tile, (32, 32))
                            screen.blit(big_tile, (x * tw + offset_x, y * th + offset_y))

def draw_special_tiles(screen, tm, tile_property):
    tw = 32
    th = 32
    for layer in tm.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tm.get_tile_image_by_gid(gid)
                if tile:
                    tile_properties = tm.get_tile_properties_by_gid(gid)
                    if tile_properties and tile_properties.get(tile_property):
                        tile_rect = pygame.Rect(x * tw + offset_x, y * th + offset_y, tw, th)
                        if camera.colliderect(tile_rect): # Only draw if the tile is within the camera's view
                            big_tile = pygame.transform.scale(tile, (32, 32))
                            screen.blit(big_tile, (x * tw + offset_x, y * th + offset_y))

def change_map(new_map):
    global current_map
    # Load the shop map
    current_map = new_map

def draw_inventory(screen, inventory, font, start_x, start_y, line_height):
    keys = list(inventory.keys())
    for i, key in enumerate(keys):
        text = f'• {key}: {inventory[key]}'
        inventory_surf = font.render(text, True, (0, 0, 255))
        button = Button(start_x, start_y + i * line_height, 100, 40, text, None, turquoise, (0, 0, 255))
        button.draw(screen)
        

first_time_changing_map_to_shop = True
first_time_changing_map_back = True
             
######\/###### ## #### #### #### ##### ## ######\/######                      
######⬇️###### -> MAIN GAME LOOP STUFF <- ######⬇️######

screen = load_pygame(mute, music, music_is_playing)
tm = load_map(current_map)

# Create instances of Classess
offset_x = screen.get_width() // 2 - hero.x
offset_y = screen.get_height() // 2 - hero.y
blue_slime = Slime(blue_slime_x, blue_slime_y, "blue", offset_x, offset_y)
green_slime = Slime(green_slime_x, green_slime_y, "green", offset_x, offset_y)
red_slime = Slime(red_slime_x, red_slime_y, "red", offset_x, offset_y)
giant_bat = Giant_Bat(giant_bat_x, giant_bat_y, offset_x, offset_y)
goblin = Goblin(goblin_x, goblin_y, offset_x, offset_y)
goblin_beast = Goblin_Beast(goblin_beast_x, goblin_beast_y, offset_x, offset_y)

stamina_bar = Stamina_Bar(screen.get_width() // 2, screen.get_height() // 2 - 10, 48, 8, max_stamina, False, small_font.render('stamina', True, (0, 0, 0)), small_font.render('oxygen', True, (0, 0, 0)), small_font.render(f'arrows: {hero.arrows}', True, (0, 0, 0)))

health_bar = HealthBar(310, 600, 300, 20, 300)# x, y, width, height, max_health
blue_slime_health_bar = HealthBar(blue_slime.x + 26, blue_slime.y + 75, 75, 8, 120)
green_slime_health_bar = HealthBar(green_slime.x + 26, green_slime.y + 75, 75, 8, 100)
red_slime_health_bar = HealthBar(red_slime.x + 26, red_slime.y + 75, 75, 8, 100)
giant_bat_health_bar = HealthBar(giant_bat.x + 3, giant_bat.y, 75, 8, 200)
goblin_health_bar = HealthBar(goblin.x, goblin.y, 50, 8, 80)
goblin_beast_health_bar = HealthBar(goblin_beast.x, goblin_beast.y, 50, 8, 180)

# Button for showing inventory
inventory_button = Button(190, 588, 100, 40, 'Inventory', light_blue, turquoise, (0, 0, 0))
# State variable for the inventory screen
show_inventory = False

music_mute_button = Button(860, 595, 140, 36, "mute music", light_blue, turquoise, (0, 0, 0))
sound_effects_mute_button = Button(628, 595, 222, 36, "mute sound effects", light_blue, turquoise, (0, 0, 0))

arrows = []
spears = []

villager1_x = 800
villager1_y = 1450

villager2_x = 640
villager2_y = 1600

villager3_x = 400
villager3_y = 1500

villager4_x = 1600
villager4_y = 1550

villager5_x = 900
villager5_y = 1200

villager6_x = 2000
villager6_y = 1100

shopkeeper_x = 448
shopkeeper_y = 64

NPC_speech = ["hi", "   hello", "...", "      welcome", "10% off!"] # last two are for shopkeeper

NPCs = []
NPCs.append(NPC(villager1_x, villager1_y, "bearded_villager", "left", offset_x, offset_y, NPC_speech[random.randint(0, 2)], False))
NPCs.append(NPC(villager2_x, villager2_y, "herbalist", "down", offset_x, offset_y, NPC_speech[random.randint(0, 2)], False))
NPCs.append(NPC(villager3_x, villager3_y, "astrologer", "left", offset_x, offset_y, NPC_speech[random.randint(0, 2)], False))
NPCs.append(NPC(villager4_x, villager4_y, "artist", "up", offset_x, offset_y, NPC_speech[random.randint(0, 2)], False))
NPCs.append(NPC(villager5_x, villager5_y, "hunter", "down", offset_x, offset_y, NPC_speech[random.randint(0, 2)], False))
NPCs.append(NPC(villager6_x, villager6_y, "jeweler", "down", offset_x, offset_y, NPC_speech[random.randint(0, 2)], False))
NPCs.append(NPC(shopkeeper_x, shopkeeper_y, "warlord", "down", offset_x, offset_y, NPC_speech[random.randint(0, 3)], True))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if inventory_button.is_over(pygame.mouse.get_pos()):
                show_inventory = not show_inventory  # Toggle the inventory display
                
            if music_mute_button.is_over(pygame.mouse.get_pos()):
                if stop_or_play_music(music, music_is_playing, False) == False:
                    music_is_playing = True
                    music_mute_button.change_text("unmute music")
                    Thread(target = lambda: play_sound("mute_button.mp3", mute, music, music_is_playing)).start()
                elif stop_or_play_music(music, music_is_playing, False) == True:
                    music_is_playing = False
                    music_mute_button.change_text("mute_music")
                    Thread(target = lambda: play_sound("mute_button.mp3", mute, music, music_is_playing)).start()
                stop_or_play_music(music, music_is_playing, True)
                
            if sound_effects_mute_button.is_over(pygame.mouse.get_pos()):
                Thread(target = lambda: play_sound("mute_button.mp3", mute, music, music_is_playing)).start()
                if mute == False:
                    mute = True
                    sound_effects_mute_button.change_text("unmute_sound_effects")
                elif mute == True:
                    mute = False
                    sound_effects_mute_button.change_text("mute_sound_effects")
        
    if shift_key_down == True and stamina_depleted == False and stamina_bar.is_in_water == False:
        Thread(target = lambda: play_sound("running_in_grass.mp3", mute, music, music_is_playing)).start()
        if stamina_bar.current_stamina <= 6:
            stamina_bar.reduce_stamina(stamina_bar.current_stamina)
            stamina_depleted == True
            hero_speed = 16
        else:
            stamina_bar.reduce_stamina(6)
            
    elif stamina_bar.current_stamina < 100:
        stamina_depleted == False
        stamina_bar.increase_stamina(4)
        
    # update all of the monster, NPC, or hero rects
    offset_x = screen.get_width() // 2 - hero.x
    offset_y = screen.get_height() // 2 - hero.y
    
    blue_slime.x = offset_x + blue_slime_x + blue_slime.move_x
    blue_slime.y = offset_y + blue_slime_y + blue_slime.move_y
    blue_slime_health_bar.x = offset_x + blue_slime_x + 26 + blue_slime.move_x
    blue_slime_health_bar.y = offset_y + blue_slime_y + 75 + blue_slime.move_y
    blue_slime.rect = pygame.Rect(blue_slime.x + 5, blue_slime.y + blue_slime_height / 2 - 10, blue_slime_width - 16, blue_slime_height - 16)
        
    green_slime.x = offset_x + green_slime_x + green_slime.move_x
    green_slime.y = offset_y + green_slime_y + green_slime.move_y
    green_slime_health_bar.x = offset_x + green_slime_x + 26 + green_slime.move_x
    green_slime_health_bar.y = offset_y + green_slime_y + 75 + green_slime.move_y
    green_slime.rect = pygame.Rect(green_slime.x + 5, green_slime.y + green_slime_height / 2 - 10, green_slime_width - 16, green_slime_height - 16)
    
    red_slime.x = offset_x + red_slime_x + red_slime.move_x
    red_slime.y = offset_y + red_slime_y + red_slime.move_y
    red_slime_health_bar.x = offset_x + red_slime_x + 26 + red_slime.move_x
    red_slime_health_bar.y = offset_y + red_slime_y + 75 + red_slime.move_y
    red_slime.rect = pygame.Rect(red_slime.x + 5, red_slime.y + red_slime_height / 2 - 10, red_slime_width - 16, red_slime_height - 16)
    
    giant_bat.x = offset_x + giant_bat_x + giant_bat.move_x
    giant_bat.y = offset_y + giant_bat_y + giant_bat.move_y
    giant_bat_health_bar.x = offset_x + giant_bat_x + 4 + giant_bat.move_x
    giant_bat_health_bar.y = offset_y + giant_bat_y + giant_bat.move_y
    giant_bat.rect = pygame.Rect(giant_bat.x, giant_bat.y, giant_bat_width, giant_bat_height)
    
    goblin.x = offset_x + goblin_x + goblin.move_x
    goblin.y = offset_y + goblin_y + goblin.move_y
    goblin_health_bar.x = offset_x + goblin_x + goblin.move_x
    goblin_health_bar.y = offset_y + goblin_x + goblin.move_y
    goblin.rect = pygame.Rect(goblin.x, goblin.y, goblin.width, goblin.height)
    
    goblin_beast.x = offset_x + goblin_beast_x + goblin_beast.move_x
    goblin_beast.y = offset_y + goblin_beast_y + goblin_beast.move_y
    goblin_beast_health_bar.x = offset_x + goblin_beast_x + goblin_beast.move_x
    goblin_beast_health_bar.y = offset_y + goblin_beast_x + goblin_beast.move_y
    goblin_beast.rect = pygame.Rect(goblin_beast.x, goblin_beast.y, goblin_beast.width, goblin_beast.height)
    
    hero_bottom_rect = pygame.Rect(screen.get_width() // 2, screen.get_height() // 2 + hero_height / 2, hero_width, hero_height / 2)
    hero_rect = pygame.Rect(screen.get_width() // 2, screen.get_height() // 2, hero_width, hero_height)
    
    collision_result = check_collision(hero_rect, hero_bottom_rect, tm)
    # shop collision
    if "shop" in collision_result:
        change_map("shop.tmx")
        tm = load_map(current_map)
        if first_time_changing_map_to_shop == True:
            hero.x = 14 * 32
            hero.y = 17 * 32
            first_time_changing_map_to_shop = False
            first_time_changing_map_back = True
        
    if "shop_exit" in collision_result:
        change_map("map-new.tmx")
        tm = load_map(current_map)
        if first_time_changing_map_back == True:
            hero.x = 58 * 32
            hero.y = 45 * 32
            first_time_changing_map_back = False
            first_time_changing_map_to_shop = True
    
    # item collision
    if "shell" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.shells += 1
        hero.inventory["shell"] = hero.shells
    if "three_pearls" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.pearls += 3
        hero.inventory["pearl"] = hero.pearls
    if "single_pearl" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.pearls += 1
        hero.inventory["pearl"] = hero.pearls
    if "crown" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.crowns += 1
        hero.inventory["crown"] = hero.crowns
    if "necklace" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.necklaces += 1
        hero.inventory["necklace"] = hero.necklaces
    if "ring" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.rings += 1
        hero.inventory["ring"] = hero.rings
    if "sword" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.inventory["sword"] += 1
    if "map" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.maps += 1
        hero.inventory["map"] = hero.maps
    if "potion" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.potions += 1
        hero.inventory["potion"] = hero.potions
    if "helmet" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.helmets += 1
        hero.inventory["helmet"] = hero.helmets
    if "arrow" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        hero.arrows += 1
        hero.inventory["arrows"] = hero.arrows

    if "treasure_chest" in collision_result:
        Thread(target = lambda: play_sound("coin.mp3", mute, music, music_is_playing)).start()
        gems += random.randint(3, 10)
    if "blue_gem" in collision_result:
        Thread(target = lambda: play_sound("coin.mp3", mute, music, music_is_playing)).start()
        gems += 1
    if "red_gems" in collision_result:
        Thread(target = lambda: play_sound("coin.mp3", mute, music, music_is_playing)).start()
        gems += 5
    if "bag_of_coins" in collision_result:
        Thread(target = lambda: play_sound("item-pickup.mp3", mute, music, music_is_playing)).start()
        gems += random.randint(6, 12)
    hero.inventory["gems"] = gems
        
    # water collision
    if "water" in collision_result:
        hero_speed = 6
        stamina_bar.is_in_water = True
        if hero.state == "moving" or hero.state == "attacking":
            stamina_or__bar.reduce_stamina(7.5)
        else:
            stamina_bar.reduce_stamina(5.615)
        if stamina_bar.current_stamina <= 0:
            print("hero drowned!")
            running = False
            
    # monster collision  
    if "blue_slime" in collision_result:
        if blue_slime.alive == True:
            if blue_slime.current_sprite == 4:
                Thread(target = lambda: play_sound("slime_attack.mp3", mute, music, music_is_playing)).start()
                blue_slime.attack()
                hero.health -= 8
                health_bar.reduce_health(8)
            if attacking == True:
                blue_slime_health_bar.reduce_health(8)
                if blue_slime_health_bar.current_health <= 0:
                    Thread(target = lambda: play_sound("slime_death.mp3", mute, music, music_is_playing)).start()
                    blue_slime.die()
                    blue_slime_health_bar.dissapear()
                    
    if "green_slime" in collision_result:
        if green_slime.alive == True:
            green_slime.attack()  
            if green_slime.current_sprite == 4:
                Thread(target = lambda: play_sound("slime_attack.mp3", mute, music, music_is_playing)).start()
                hero.health -= 8
                health_bar.reduce_health(8)
            if attacking == True:
                green_slime_health_bar.reduce_health(8)
                if green_slime_health_bar.current_health <= 0:
                    Thread(target = lambda: play_sound("slime_death.mp3", mute, music, music_is_playing)).start()
                    green_slime.die()
                    green_slime_health_bar.dissapear()
                    
    if "red_slime" in collision_result:
        if red_slime.alive == True:
            red_slime.attack()
            if red_slime.current_sprite == 4:
                Thread(target = lambda: play_sound("slime_attack.mp3", mute, music, music_is_playing)).start()
                hero.health -= 8
                health_bar.reduce_health(8)
                if health_bar.current_health <= 0:
                    play_sound("game_over.mp3", mute, music, music_is_playing)
                    running = False
                    ("hero died!")
            if attacking == True:
                red_slime_health_bar.reduce_health(8)
                if red_slime_health_bar.current_health <= 0:
                    Thread(target = lambda: play_sound("slime_death.mp3", mute, music, music_is_playing)).start()
                    red_slime.die()
                    red_slime_health_bar.dissapear()
    
    if "giant_bat" in collision_result:
        if giant_bat.alive == True:
            giant_bat.attack(screen)
            if giant_bat.current_sprite == 5:
                Thread(target = lambda: play_sound("attack_swoosh.mp3", mute, music, music_is_playing)).start()
                hero.health -= 11
                health_bar.reduce_health(11)
                if health_bar.current_health <= 0:
                    play_sound("game_over.mp3", mute, music, music_is_playing)
                    running = False
                    ("hero died!")
            if attacking == True:
                giant_bat_health_bar.reduce_health(12)
                if giant_bat_health_bar.current_health <= 0:
                    giant_bat.die(screen)
                    giant_bat_health_bar.dissapear()
                    
    if "goblin" in collision_result:
        if goblin.alive == True:
            goblin.attack()
            if goblin.current_sprite == 5:
                Thread(target = lambda: play_sound("attack_swoosh.mp3", mute, music, music_is_playing)).start()
                hero.health -= 14
                health_bar.reduce_health(15)
                if health_bar.current_health <= 0:
                    play_sound("game_over.mp3", mute, music, music_is_playing)
                    running = False
                    ("hero died!")
            if attacking == True:
                goblin_health_bar.reduce_health(11)
                if goblin_health_bar.current_health <= 0:
                    goblin.die(screen)
                    goblin_health_bar.dissapear()
                
    if "goblin_beast" in collision_result:
        if goblin_beast.alive == True:
            goblin_beast.attack()
            if goblin.current_sprite == 5:
                Thread(target = lambda: play_sound("attack_swoosh.mp3", mute, music, music_is_playing)).start()
                hero.health -= 16
                health_bar.reduce_health(15)
                if health_bar.current_health <= 0:
                    play_sound("game_over.mp3", mute, music, music_is_playing)
                    running = False
                    ("hero died!")
            if attacking == True:
                goblin_beast_health_bar.reduce_health(8)
                if goblin_beast_health_bar.current_health <= 0:
                    goblin_beast.die(screen)
                    goblin_beast_health_bar.dissapear()
                    
    if "blue_slime-water" in collision_result:
        blue_slime.speed = 24
        
    if "blue_slime-water" not in collision_result:
        if blue_slime.speed == 24:
            blue_slime.speed = 16
    
    if "water" not in collision_result:
        stamina_bar.is_in_water = False
        if stamina_bar.current_stamina < 97:
            stamina_bar.current_stamina += 3
        elif stamina_bar.current_stamina > 97 and stamina_bar.current_stamina < 100:
            stamina_bar.current_stamina = 100
        if hero_speed == 6:
            hero_speed = 16
    
    handle_input()
    
    gem_display = font.render(f'gems: {gems}', True, (0, 0, 255))
    tile_coordinates = font.render(f'{hero.x/32 + hero_width/64}, {hero.y/32 + hero_height/64}', True, (82, 82, 82))
    screen.fill((0, 0, 0))
    if current_map == "map-new.tmx":
        draw_tiles(screen, tm)
        draw_objects(screen, tm)
    elif current_map == "shop.tmx":
        draw_tiles(screen, tm)
        draw_objects(screen, tm)
        draw_special_tiles(screen, tm, "is_buyable")
    screen.blit(gem_display, (200, 600))
    screen.blit(tile_coordinates, (32, 600))
    
    stamina_bar.draw(screen)
    music_mute_button.draw(screen)
    sound_effects_mute_button.draw(screen)
    inventory_button.draw(screen)
    health_bar.draw(screen)
    if current_map == "map-new.tmx":
        blue_slime_health_bar.draw(screen)
        green_slime_health_bar.draw(screen)
        red_slime_health_bar.draw(screen)
        giant_bat_health_bar.draw(screen)
        goblin_health_bar.draw(screen)
        goblin_beast_health_bar.draw(screen)
    
    # check is green slime is touching water
    if "green_slime-water-left" in collision_result:
        green_slime.move(16, 0)
        
    if "green_slime-water-right" in collision_result:
        green_slime.move(-16, 0)
        
    if "green_slime-water-top" in collision_result:
        green_slime.move(0, 16)
        
    if "green_slime-water-bottom" in collision_result:
        green_slime.move(0, -16)
        
    # check if green slime is touching a wall
    if "green_slime-wall-left" in collision_result:
        green_slime.move(16, 0)
        
    if "green_slime-wall-right" in collision_result:
        green_slime.move(-16, 0)
        
    if "green_slime-wall-top" in collision_result:
        green_slime.move(0, 16)
        
    if "green_slime-wall-bottom" in collision_result:
        green_slime.move(0, -16)
    
    # move the green slime if there is nothing in the way
    if "green_slime-nothing" in collision_result:
        green_slime.move_towards_hero(hero, hero_width, hero_height, offset_x, offset_y)
    
    # check is the red slime is touching a wall
    if "red_slime-wall-left" in collision_result:
        red_slime.move(16, 0)
        
    if "red_slime-wall-right" in collision_result:
        red_slime.move(-16, 0)
        
    if "red_slime-wall-top" in collision_result:
        red_slime.move(0, 16)
        
    if "red_slime-wall-bottom" in collision_result:
        red_slime.move(0, -16)
        
    # check is the red slime is touching water
    if "red_slime-water-left" in collision_result:
        red_slime.move(16, 0)
        
    if "red_slime-water-right" in collision_result:
        red_slime.move(-16, 0)
        
    if "red_slime-water-top" in collision_result:
        red_slime.move(0, 16)
        
    if "red_slime-water-bottom" in collision_result:
        red_slime.move(0, -16)
    
    # move the red slime if there is nothing in the way
    if "red_slime-nothing" in collision_result:
        red_slime.move_towards_hero(hero, hero_width, hero_height, offset_x, offset_y)
    
    giant_bat.range_attack(hero, hero_width, hero_height, offset_x, offset_y, hero_rect)
    if giant_bat.attack2 == True and giant_bat.alive == True:
        if giant_bat.current_sprite == 3:
            if giant_bat.direction == "left":
                new_spear = Arrow(giant_bat.x + 20, giant_bat.y + 20, offset_x, offset_y, "left", "spear")
            elif giant_bat.direction == "right":
                 new_spear = Arrow(giant_bat.x + 20, giant_bat.y + 20, offset_x, offset_y, "right", "spear")
            elif giant_bat.direction == "up":
                new_spear = Arrow(giant_bat.x + 20, giant_bat.y + 20, offset_x, offset_y, "up", "spear")
            elif giant_bat.direction == "down":
                new_spear = Arrow(giant_bat.x + 20, giant_bat.y + 20, offset_x, offset_y, "down", "spear")

            new_spear.exists = True
            spears.append(new_spear)
    
    giant_bat.x = offset_x + giant_bat_x + giant_bat.move_x
    giant_bat.y = offset_y + giant_bat_y + giant_bat.move_y
    
    if current_map == "map-new.tmx":
        for spear in spears:
            spear.speed = random.randint(24, 40)
            spear.update(spear.direction)
            spear.draw(screen, spear.direction)
            if spear.check_collision(blue_slime.rect, green_slime.rect, red_slime.rect, giant_bat.rect, hero_rect) == "hero":
                hero.health -= 12
                health_bar.reduce_health(12)
                if health_bar.current_health <= 0:
                    running = False
                    print("hero died!")   

    blue_slime.move_towards_hero(hero, hero_width, hero_height, offset_x, offset_y)
    giant_bat.move_towards_hero(hero, hero_width, hero_height, offset_x, offset_y)
    goblin.move_towards_hero(hero, hero_width, hero_height, offset_x, offset_y)
    goblin_beast.move_towards_hero(hero, hero_width, hero_height, offset_x, offset_y)
    giant_bat.change_direction(hero.x + hero_width / 2, hero.y + hero_height / 2)
    goblin.change_direction(hero.x + hero_width / 2, hero.y + hero_height / 2)
    goblin_beast.change_direction(hero.x + hero_width / 2, hero.y + hero_height / 2)
    
    hero.update()
    hero.draw(screen)
    if current_map == "map-new.tmx":
        goblin_beast.update(screen)
        blue_slime.update()
        green_slime.update()
        red_slime.update()
        giant_bat.update(screen)
        goblin.update(screen)
        blue_slime.draw(screen)
        green_slime.draw(screen)
        red_slime.draw(screen)
        giant_bat.draw(screen)
        goblin.draw(screen)
        goblin_beast.draw(screen)
    
    for npc in NPCs:
        npc.x = offset_x + npc.start_x + npc.move_x
        npc.y = offset_y + npc.start_y + npc.move_y
        npc.rect = pygame.Rect(npc.x, npc.y, npc.width, npc.height)
        npc.speech_condition = npc.is_close(hero)  # Assuming 'player' is your player object
        if npc.is_shopkeeper == True and current_map == "shop.tmx":
            npc.draw(screen)
            if npc.speech_condition == True:
                npc.talk(screen, npc.speech, small_font)
        elif npc.is_shopkeeper == False and current_map == "map-new.tmx":
            npc.draw(screen)
            if npc.speech_condition == True:
                npc.talk(screen, npc.speech, small_font)
        if npc.mouse_is_over(pygame.mouse.get_pos()):
            if npc.is_shopkeeper == False:
                npc.interact(screen, npc.speech, "", font)
            else:
                if npc.shopkeeper_speech_num == 0:
                    npc.interact(screen, "               drop items on", "                counter to sell", font)
                else:
                    npc.interact(screen, "                  walk to an item", "                     on display to buy", font)
        else:
            npc.shopkeeper_speech_num = random.randint(0, 1)
        
    if giant_bat.alive == False:
        if giant_bat.show_meat(screen, hero_rect) == "meat1":
            health_bar.increase_health(random.randint(30, 44))
        elif giant_bat.show_meat(screen, hero_rect) == "meat2":
            health_bar.increase_health(random.randint(20, 30))
        elif giant_bat.show_meat(screen, hero_rect) == "meat3":
            health_bar.increase_health(random.randint(24, 34))
        elif giant_bat.show_meat(screen, hero_rect) == "meat4":
            health_bar.increase_health(randomt.randint(18, 26))
        elif giant_bat.show_meat(screen, hero_rect) == "meat5":
            health_bar.increase_health(random.randint(32, 40))
        elif giant_bat.show_meat(screen, hero_rect) == "meat6":
            health_bar.increase_health(random.randint(40, 56))
    
    # If the game state is to show the inventory
    if show_inventory:
        # This function will pause the game and display the inventory
        draw_inventory(screen, hero.inventory, font, 50, 50, 30) 
    
    # arrow logic
    if space_key_down == True and shift_key_down == True and stamina_bar.current_stamina > 6 and hero.arrows > 0:
        stamina_bar.arrow_is_shooting = True
        Thread(target = lambda: play_sound("bow_release.mp3", mute, music, music_is_playing)).start() 
        if direction == "left":
            #new_arrow = Arrow(448, 342, offset_x, offset_y, "left", "normal")
            new_arrow = Arrow(screen.get_width() // 2, screen.get_height() // 2 + 10, offset_x, offset_y, "left", "normal")
        elif direction == "right":
             #new_arrow = Arrow(540, 342, offset_x, offset_y, "right", "normal")
             new_arrow = Arrow(screen.get_width() // 2 + 16, screen.get_height() // 2 + 10, offset_x, offset_y, "right", "normal")
        elif direction == "up":
             #new_arrow = Arrow(510, 290, offset_x, offset_y, "up", "normal")
            new_arrow = Arrow(screen.get_width() // 2 + 8, screen.get_height() // 2, offset_x, offset_y, "up", "normal")
        elif direction == "down":
             #new_arrow = Arrow(514, 356, offset_x, offset_y, "down", "normal")
            new_arrow = Arrow(screen.get_width() // 2 + 8, screen.get_height() // 2, offset_x, offset_y, "down", "normal")
             
        new_arrow.exists = True
        arrows.append(new_arrow)
        hero.arrows -= 1
        hero.inventory["arrow"] = hero.arrows
        stamina_bar.arrow_display = small_font.render(f'arrows: {hero.arrows}', True, (0, 0, 0))
    else:
        stamina_bar.arrow_is_shooting = False
    
    for arrow in arrows:
        arrow.speed = random.randint(24, 40)
        arrow.update(arrow.direction)
        arrow.draw(screen, arrow.direction)
        if arrow.check_collision(blue_slime.rect, green_slime.rect, red_slime.rect, giant_bat.rect, hero_rect) == "blue_slime":
            blue_slime_health_bar.reduce_health(3)
            if blue_slime_health_bar.current_health <= 0:
                blue_slime.die()
                blue_slime_health_bar.dissapear()
        if arrow.check_collision(blue_slime.rect, green_slime.rect, red_slime.rect, giant_bat.rect, hero_rect) == "green_slime":
            green_slime_health_bar.reduce_health(3)
            if green_slime_health_bar.current_health <= 0:
                green_slime.die()
                green_slime_health_bar.dissapear()
        if arrow.check_collision(blue_slime.rect, green_slime.rect, red_slime.rect, giant_bat.rect, hero_rect) == "red_slime":
            red_slime_health_bar.reduce_health(3)
            if red_slime_health_bar.current_health <= 0:
                red_slime.die()
                red_slime_health_bar.dissapear()
        if arrow.check_collision(blue_slime.rect, green_slime.rect, red_slime.rect, giant_bat.rect, hero_rect) == "giant_bat":
            giant_bat_health_bar.reduce_health(3)
            if giant_bat_health_bar.current_health <= 0:
                giant_bat.die(screen)
                giant_bat_health_bar.dissapear()
              
    if blue_slime.state == "attack" and blue_slime.current_sprite == 4:
        blue_slime.end_attack()
        
    if green_slime.state == "attack" and green_slime.current_sprite == 4:
        green_slime.end_attack()
        
    if red_slime.state == "attack" and red_slime.current_sprite == 4:
        red_slime.end_attack()
        
    if giant_bat.state == "attack" and giant_bat.current_sprite == 5:
        giant_bat.end_attack()
        
    if goblin.state == "attack" and goblin.current_sprite == 9:
        goblin.end_attack()
        
    if goblin_beast.state == "attack" and goblin_beast.current_sprite == 7:
        goblin_beast.end_attack() 

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()