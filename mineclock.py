class ClockSettings(object):
    DEBUG = False


print('Initializing')

import mcpi.minecraft as minecraft
import mcpi.block as block
import time, math, random

game_linked = False

while not game_linked:
    try:
        mc = minecraft.Minecraft.create()
        player_id = mc.getPlayerEntityIds()[0]
        game_linked = True
    except Exception:
        print('Waiting for minecraft-pi...')
        time.sleep(0.1)
        game_linked = False

def chat(message=''):
    print('<chat> ' + str(message))
    mc.postToChat(message)


def get_x(x):
    return top_left[0] - x
    
    
def get_y(y):
    return top_left[1] - y


def wait_for_kb_and_mouse():
    #original_pos = mc.player.getPos()
    """p_head = [20, 41, -3]
    blocks_to_break = [[p_head[0] + 1, p_head[1], p_head[2]],
                       [p_head[0], p_head[1], p_head[2] + 1],
                       [p_head[0] - 1, p_head[1], p_head[2]], 
                       [p_head[0], p_head[1], p_head[2] - 1]]
    
    mc.setBlock(p_head[0], p_head[1] - 2, p_head[2], block.GLASS.id)
    
    mc.camera.setNormal(player_id)
    #chat(mc.player.getPos())
    mc.player.setPos(20.7, 40.0, -2.47485)

    for test_block in blocks_to_break:
        mc.setBlock(test_block[0], test_block[1], test_block[2], block.GLASS.id)
        
    block_broken = False
    
    while not block_broken:
        device.emit(uinput.BTN_LEFT, 1)
        time.sleep(1)
        device.emit(uinput.BTN_LEFT, 0)
        
        for test_block in blocks_to_break:
            if mc.getBlock(test_block[0], test_block[1], test_block[2]) == 0:
                block_broken = True"""
    
    draw_hidden_block()
    
    block_broken = False
    
    while not block_broken:
        device.emit(uinput.BTN_LEFT, 1)
        time.sleep(1)
        device.emit(uinput.BTN_LEFT, 0)

        if mc.getBlock(get_x(12), camera_height - 5, get_y(7)) == block.AIR.id:
            block_broken = True
    
    
    first_pos = mc.player.getPos()
    second_pos = mc.player.getPos()
    
    while first_pos == second_pos:
        device.emit(uinput.KEY_W, 1)
        time.sleep(0.1)
        device.emit(uinput.KEY_W, 0)
        second_pos = mc.player.getPos()
    
    stop_player()
    
    #mc.player.setTilePos(original_pos)


def reset_camera():
    #mc.camera.setNormal(player_id)
    #return
    if ClockSettings.DEBUG and False: 
        mc.camera.setFollow(player_id)
    else:
        mc.camera.setFixed()
        mc.camera.setPos([get_x(12.04), camera_height, get_y(7.04)])
        #mc.camera.setPos([get_x(18.04), 6, get_y(7.04)])
    #mc.camera.setPos([-12.04, 20, -7.04])
    

def prepare_hotbar():
    item_list = [[3, 6],
                 [4, 6],
                 [5, 0]]
                 
    item_list.reverse()

    for it in range(len(item_list)):
        device.emit_click(uinput.KEY_E)
        time.sleep(0.1)
        
        for move in range(7):
            time.sleep(0.05)
            device.emit_click(uinput.KEY_W)
        for move in range(12):
            time.sleep(0.05)
            device.emit_click(uinput.KEY_A)
        
        for move in range(item_list[it][0]):
            time.sleep(0.05)
            device.emit_click(uinput.KEY_S)        
        for move in range(item_list[it][1]):
            time.sleep(0.05)
            device.emit_click(uinput.KEY_D)
        
        device.emit_click(uinput.KEY_ENTER)
        time.sleep(0.1)
    
    

def get_orientation(stay_visible=False):
    global current_orientation
    
    original_pos = mc.player.getPos()
    
    if not stay_visible:
        mc.player.setTilePos([test_loc[0], 1, test_loc[1]])

    first_pos = mc.player.getPos()
    x1, y1 = first_pos.x, first_pos.z
    distance_traveled = 0
    
    device.emit(uinput.KEY_W, 1)
    
    while distance_traveled < 0.1:
    
        time.sleep(0.1)
        
        second_pos = mc.player.getPos()
        x2, y2 = second_pos.x, second_pos.z
        
        angle_rad = math.atan2(y2 - y1, x2 - x1)
        angle_deg = math.degrees(angle_rad) + 180
        
        distance_traveled = round(math.sqrt((first_pos.x - second_pos.x) ** 2.0 + (first_pos.z - second_pos.z) ** 2.0), 1)
        #chat(str(distance_traveled) + '  ' + str(angle_deg))
        
        #if first_pos == second_pos and ClockSettings.DEBUG:
            #chat('ERROR - get_orientation: Player didn\'t move!')
            #angle_deg = get_orientation()
    
    device.emit(uinput.KEY_W, 0)
    
    current_orientation = angle_deg
    
    mc.player.setTilePos(original_pos)
    
    return angle_deg


def set_orientation(h_view, v_view=-1):
    if v_view != -1:
        # TODO: Look completely up (0) and move until approximate angle
        pass
    
    original_pos = mc.player.getPos()
    mc.player.setTilePos([test_loc[0], 1, test_loc[1]])
    
    stop_player()
    current_h_view = get_orientation(stay_visible=False)
    movement = int(h_view) - int(current_h_view)
    
    while movement != 0:
        if abs(movement) > 180:
            if movement < 0:
                movement = 360 - abs(movement)
            else:
                movement = movement - 360
        
        if -5 < movement < 5:
            movement = -10 if movement < 0 else 10
        else:
            movement = movement * 2
        
        device.emit(uinput.REL_X, movement)
        current_h_view = get_orientation(stay_visible=False)
        movement = int(h_view) - int(current_h_view)
        
    mc.player.setTilePos(original_pos)
        #if ClockSettings.DEBUG:
        #    chat(current_h_view)
    

def walk(distance, backwards=False):
    if ClockSettings.DEBUG and False:
        chat('walk - dist: ' + str(round(distance, 2)))
        
    if distance <= 0:
        return

    original_pos = mc.player.getPos()
    distance_traveled = 0
    key = uinput.KEY_S if backwards else uinput.KEY_W
    
    device.emit(key, 1)
             
    while distance_traveled < distance:
        before_pos = mc.player.getPos()
        current_pos = before_pos
        
        wait_start = time.time()
        
        while before_pos == current_pos:
            current_pos = mc.player.getPos()
            
            if time.time() - wait_start > 0.5:
                device.emit(key, 0)
                time.sleep(0.2)
                device.emit(key, 1)
                wait_start = time.time()
            
        last_dist = distance_traveled
        distance_traveled = math.sqrt((original_pos.x - current_pos.x) ** 2.0 + (original_pos.z - current_pos.z) ** 2.0)
        
        
        if before_pos.x == current_pos.x or before_pos.z == current_pos.z:
            if int(current_pos.x * 10) == current_pos.x * 10 or int(current_pos.z * 10) == current_pos.z * 10:
                if abs(int(current_pos.x * 10)) % 10 == 3 or abs(int(current_pos.x * 10)) % 10 == 7 or abs(int(current_pos.z * 10)) % 10 == 3 or abs(int(current_pos.z * 10)) % 10 == 7:
                    device.emit(key, 0)
                    time.sleep(0.2)
                    device.emit(key, 1)
                    time.sleep(0.1)
                    device.emit(uinput.KEY_SPACE, 1)
                    
                    wait_start = time.time()
                    
                    while before_pos.y + 1 > current_pos.y:
                        current_pos = mc.player.getPos()
                        
                        if current_pos.y < before_pos.y:
                            # Rare edge cases caused by leftover blocks and water when lagging heavily, essentially causing a softlock
                            before_pos = current_pos
                            # mc.setBlock(get_x(12), 0, get_y(5), block.LAPIS_LAZULI_BLOCK.id)
                        
                        if abs(current_pos.x) == 127.7 or abs(current_pos.z) == 127.7:
                            # mc.setBlock(get_x(12), 0, get_y(7), block.BEDROCK.id)
                            device.emit(key, 0)
                            # chat('Softlock prevention triggered :/')
                            return
                        
                        if time.time() - wait_start > 5:
                            # chat('Resetting space...')
                            device.emit(uinput.KEY_SPACE, 0)
                            time.sleep(0.2)
                            device.emit(uinput.KEY_SPACE, 1)
                            wait_start = time.time()
                        
                    device.emit(uinput.KEY_SPACE, 0)
                    
                    time.sleep(0.2)
                    last_dist = distance_traveled
                    distance_traveled = math.sqrt((original_pos.x - current_pos.x) ** 2.0 + (original_pos.z - current_pos.z) ** 2.0)

    device.emit(key, 0)
    
    """
    device.emit(key, 1)
    
    while distance_traveled < distance:
    
        last_distance = distance_traveled
    
        #device.emit(key, 1)
        time.sleep(0.1)
        #device.emit(key, 0)
    
        moved_pos = mc.player.getPos()
        distance_traveled = round(math.sqrt((original_pos.x - moved_pos.x) ** 2.0 + (original_pos.z - moved_pos.z) ** 2.0), 1)

        if distance_traveled == last_distance and distance_traveled > 0:
            if stuck:
                if ClockSettings.DEBUG:
                    chat('Player got stuck while walking, abandonning...')
                break
            else:
                # We're stuck, let's jump
                device.emit(uinput.KEY_SPACE, 1)
                time.sleep(0.1)
                device.emit(uinput.KEY_SPACE, 0)
                stuck = True
        else:
            stuck = False

    device.emit(key, 0)
    """


def walk_to(dest_x, dest_y):
    if ClockSettings.DEBUG and False:
        chat('walk_to - x: ' + str(dest_x) + ' y: ' + str(dest_y))

    current_pos = mc.player.getPos()
    
    dist = math.sqrt((current_pos.x - dest_x - 0.5) ** 2.0 + (current_pos.z - dest_y - 0.5) ** 2.0)
    last_dist = dist

    keys = [uinput.KEY_W, uinput.KEY_A, uinput.KEY_S, uinput.KEY_D]

    while dist > 1:
        for key in keys:
            device.emit(key, 1)
             
            while last_dist >= dist:
                before_pos = mc.player.getPos()
                current_pos = before_pos
                
                wait_start = time.time()
                
                while before_pos == current_pos:
                    current_pos = mc.player.getPos()
                    
                    if time.time() - wait_start > 1:
                        # mc.setBlock(get_x(12), 0, get_y(9), block.GOLD_BLOCK.id)
                        break
                        """device.emit(key, 0)
                        time.sleep(0.2)
                        device.emit(key, 1)
                        wait_start = time.time()"""
                    
                    
                last_dist = dist
                dist = math.sqrt((current_pos.x - dest_x - 0.5) ** 2.0 + (current_pos.z - dest_y - 0.5) ** 2.0)
                
                if dist <= 1:
                    break
                
                if before_pos.x == current_pos.x or before_pos.z == current_pos.z:
                    if int(current_pos.x * 10) == current_pos.x * 10 or int(current_pos.z * 10) == current_pos.z * 10:
                        if abs(int(current_pos.x * 10)) % 10 == 3 or abs(int(current_pos.x * 10)) % 10 == 7 or abs(int(current_pos.z * 10)) % 10 == 3 or abs(int(current_pos.z * 10)) % 10 == 7:
                            device.emit(key, 0)
                            time.sleep(0.2)
                            device.emit(key, 1)
                            time.sleep(0.1)
                            device.emit(uinput.KEY_SPACE, 1)
                            
                            wait_start = time.time()
                            
                            while before_pos.y + 1 > current_pos.y:
                                current_pos = mc.player.getPos()
                                
                                if current_pos.y < before_pos.y:
                                    # Rare edge cases caused by leftover blocks and water when lagging heavily, essentially causing a softlock
                                    before_pos = current_pos
                                    # mc.setBlock(get_x(12), 0, get_y(5), block.LAPIS_LAZULI_BLOCK.id)
                                
                                if abs(current_pos.x) == 127.7 or abs(current_pos.z) == 127.7:
                                    # mc.setBlock(get_x(12), 0, get_y(7), block.BEDROCK.id)
                                    device.emit(key, 0)
                                    # chat('Softlock prevention triggered :/')
                                    return
                                    
                                if time.time() - wait_start > 5:
                                    # chat('Resetting space...')
                                    device.emit(uinput.KEY_SPACE, 0)
                                    time.sleep(0.2)
                                    device.emit(uinput.KEY_SPACE, 1)
                                    wait_start = time.time()
                                
                            device.emit(uinput.KEY_SPACE, 0)
                            
                            time.sleep(0.2)
                            current_pos = mc.player.getPos()
                            last_dist = dist
                            dist = math.sqrt((current_pos.x - dest_x - 0.5) ** 2.0 + (current_pos.z - dest_y - 0.5) ** 2.0)

            device.emit(key, 0)

            if dist <= 1:
                break
                
            current_position = mc.player.getPos()
            time.sleep(0.1)
            while current_position != mc.player.getPos():
                time.sleep(0.1)
                current_position = mc.player.getPos()
            
            current_pos = mc.player.getPos()
            dist = math.sqrt((current_pos.x - dest_x - 0.5) ** 2.0 + (current_pos.z - dest_y - 0.5) ** 2.0)
            last_dist = dist
            

    #mc.player.setTilePos(dest_x, 1, dest_y)


def stop_player():
    original_pos = mc.player.getPos()
    mc.setBlocks(test_loc[0] - get_x(1), 1, test_loc[1] - get_y(1),test_loc[0] + get_x(1), 3, test_loc[1] + get_y(1), block.WOOL.id, 0)
    mc.setBlocks(test_loc[0], 1, test_loc[1],test_loc[0], 3, test_loc[1], block.AIR.id)
    mc.player.setTilePos(test_loc[0], 1, test_loc[1])
    
    current_position = mc.player.getPos()
    time.sleep(0.1)
    while current_position != mc.player.getPos():
        time.sleep(0.1)
        current_position = mc.player.getPos()
    
    mc.player.setTilePos(original_pos)
    mc.setBlocks(test_loc[0] - get_x(1), 1, test_loc[1] - get_y(1),test_loc[0] + get_x(1), 3, test_loc[1] + get_y(1), block.AIR.id)


def toggle_flying(flying=None):
    trigger_flight = False
    original_height = mc.player.getPos().y
    
    #while original_height != mc.player.getPos().y:
    #    original_height = mc.player.getPos().y

    if flying is None:
        trigger_flight = True
    else:
        device.emit(uinput.KEY_SPACE, 1)
        time.sleep(0.1)
        device.emit(uinput.KEY_SPACE, 0)
        
        time.sleep(0.75)
        
        if original_height == mc.player.getPos().y:
            trigger_flight = flying
        else:
            trigger_flight = not flying
        

    if trigger_flight:
        device.emit(uinput.KEY_SPACE, 1)
        time.sleep(0.1)
        device.emit(uinput.KEY_SPACE, 0)
        time.sleep(0.1)
        device.emit(uinput.KEY_SPACE, 1)
        time.sleep(0.1)
        device.emit(uinput.KEY_SPACE, 0)


def get_good_block():
    if ClockSettings.DEBUG:
        return good_blocks['wool_purple']
    else:
        return random.choice(list(good_blocks.values()))


def clear_clock():
    mc.setBlocks(top_left[0] + 5, -64, top_left[1] + 5, get_x(30), 64, get_y(20), block.AIR.id)
    mc.setBlocks(test_loc[0] + 10, 0, test_loc[1] + 10, test_loc[0] - 10, 5, test_loc[1] - 10, block.AIR.id)
    mc.setBlocks(top_left[0] + 5, 0, top_left[1] + 5, get_x(30), 0, get_y(20), block.GLASS.id)
    mc.setBlocks(test_loc[0] + 10, 0, test_loc[1] + 10, test_loc[0] - 10, 0, test_loc[1] - 10, block.GLASS.id)
    # Uncomment to make lag lol
    # mc.setBlocks(top_left[0] + 5, -1, top_left[1] + 5, get_x(30), -1, get_y(20), block.WATER.id, 1)
    

def toggle_column():
    global column_visible
    
    if column_visible:
        mc.setBlock(get_x(12), 1, get_y(6), block.WOOL.id, 7)
        mc.setBlock(get_x(12), 1, get_y(8), block.WOOL.id, 7)
    else:
        mc.setBlock(get_x(12), 1, get_y(6), block.WOOL.id, 8)
        mc.setBlock(get_x(12), 1, get_y(8), block.WOOL.id, 8)
        
    column_visible = not column_visible


def draw_number(number, position):
    transition = active_numbers[position]['transition']
    transitions = {'draw': ['lava', 'draw_gravity', 'player_place'], 'clear': ['player_break', 'trapdoor', 'snow_plow']}
    
    number_width = len(number_dict[0][0])
    number_height = len(number_dict[0])
    corner = [number_width * position + position + 4, 5]

    
    if position > 1:
        corner[0] += 2

    
    # --------------------------------------------------------------- Clear transitions ---------------------------------------------------------------
    
    if transition is None:
        mc.setBlocks(get_x(corner[0]), 1, get_y(corner[1]), get_x(corner[0] + number_width - 1), 1, get_y(corner[1] + number_height - 1), block.AIR.id)
        
        for it_y in range(number_height):
            for it_x in range(number_width):
                if number_dict[number][it_y][it_x] == '#':
                    mc.setBlock(get_x(it_x + corner[0]), 1, get_y(corner[1] + it_y), active_numbers[position]['block'], active_numbers[position]['block_data'])
                        
    elif transition == 'instant_clear':
        mc.setBlocks(get_x(corner[0]), 1, get_y(corner[1]), get_x(corner[0] + number_width - 1), 1, get_y(corner[1] + number_height - 1), block.AIR.id)
        transition = None 
                 
    elif transition == 'player_break':
        mc.player.setTilePos([test_loc[0], 1, test_loc[1]])
        set_orientation(270)
        mc.player.setTilePos(get_x(corner[0] + math.floor(number_width/2)), 1, get_y(15))
        
        draw_hidden_block()
        
        walk(get_y(corner[1] + number_height + 1) - mc.player.getPos().z)
        #walk_to(get_x(corner[0] + math.floor(number_width/2)), get_y(corner[1] + number_height + 1))
        
        for it_y in range(number_height):
            for it_x in range(number_width):
                if number_dict[active_numbers[position]['number']][number_height - it_y - 1][it_x] == '#':
                    device.emit(uinput.BTN_LEFT, 1)
                    time.sleep(0.1)
                    device.emit(uinput.BTN_LEFT, 0)
                    draw_hidden_block()
                    mc.setBlock(get_x(it_x + corner[0]), 1, get_y(corner[1] + number_height - it_y - 1), block.AIR.id)
            
            if 3 < math.sqrt((get_x(corner[0] + math.floor(number_width/2)) - mc.player.getPos().x) ** 2.0 + (get_y(corner[1] + number_height - it_y) - mc.player.getPos().z) ** 2.0):
                # We're too far from where we should be going to
                set_orientation(270)
                walk_to(get_x(corner[0] + math.floor(number_width/2)), get_y(corner[1] + number_height - it_y))
            else:
                walk(get_y(corner[1] + number_height - it_y) - mc.player.getPos().z)
        
        #walk_to(get_x(corner[0] + math.floor(number_width/2)), get_y(-2))
        walk(get_y(-2) - mc.player.getPos().z)

        transition = None    
        
    elif transition == 'clear_gravity':
        for it_y in range(number_height):
            for it_x in range(number_width):
                if number_dict[active_numbers[position]['number']][it_y][it_x] == '#':
                    time.sleep(0.1)
                mc.setBlock(get_x(it_x + corner[0]), 0, get_y(corner[1] + it_y), block.AIR.id)
                    
        time.sleep(1)
        
        mc.setBlocks(get_x(corner[0]), 1, get_y(corner[1]), get_x(corner[0] + number_width - 1), 1, get_y(corner[1] + number_height - 1), block.AIR.id)
        
        for it_y in range(number_height + 2):
            for it_x in range(number_width + 2):
                mc.setBlock(get_x(corner[0] + it_x - 1), 0, get_y(corner[1] + it_y - 1), block.GLASS.id)
                
        transition = None
        
    elif transition == 'snow_melt':
        if slow_water_mode:
            slow_down_water()
            
        for it_y in range(number_height):
            for it_x in range(number_width):
                if number_dict[active_numbers[position]['number']][it_y][it_x] == '#':
                    mc.setBlock(get_x(it_x + corner[0]), 2, get_y(corner[1] + it_y), block.WATER.id, 4)
                    time.sleep(0.05)
        
        time.sleep(0.2)
        
        for it_y in range(number_height):
            for it_x in range(number_width):
                if number_dict[active_numbers[position]['number']][it_y][it_x] == '#':
                    mc.setBlock(get_x(it_x + corner[0]), 1, get_y(corner[1] + it_y), block.WATER.id, 5)
                    time.sleep(0.1)
        
        transition = None
        
    elif transition == 'snow_plow':
        mc.player.setTilePos([test_loc[0], 1, test_loc[1]])
        set_orientation(270)
        
        for it in range(-screen_height, models['snow_plow']['depth'] + 1):
            start_time = time.time()
            for plow_piece in models['snow_plow']['block_list']:
                skip_draw = [plow_piece[0], plow_piece[1], plow_piece[2] - 1, plow_piece[3], plow_piece[4]] in models['snow_plow']['block_list']
                
                if not skip_draw:
                    mc.setBlock(get_x(corner[0] + number_width - plow_piece[0] - 1), plow_piece[1] + 1, get_y(plow_piece[2] - it), plow_piece[3], plow_piece[4])
                    
                if plow_piece[3] == block.STONE_SLAB.id and plow_piece[4] == 9:
                    # Tp player to seat
                    #chat('seat')
                    mc.player.setTilePos(get_x(corner[0] + number_width - plow_piece[0] - 1), plow_piece[1] + 2, get_y(plow_piece[2] - it))
                        
            for plow_piece in models['snow_plow']['air_list']:
                skip_draw = [plow_piece[0], plow_piece[1], plow_piece[2] - 1, plow_piece[3], plow_piece[4]] in models['snow_plow']['air_list']
                
                if not skip_draw:
                    mc.setBlock(get_x(corner[0] + number_width - plow_piece[0] - 1), plow_piece[1] + 1, get_y(plow_piece[2] - it), plow_piece[3], plow_piece[4])
                        
            mc.setBlocks(get_x(corner[0]), 1, get_y(-it + models['snow_plow']['depth']), get_x(corner[0] + models['snow_plow']['width'] - 1), models['snow_plow']['height'], get_y(-it + models['snow_plow']['depth']), block.AIR.id)
            
            if -it - 1 < screen_height/2 and it < 0:
                mc.setBlocks(get_x(corner[0]), 1, get_y(-it - 2), get_x(corner[0] + models['snow_plow']['width'] - 1), 1, get_y(-it - 2), active_numbers[position]['block'], active_numbers[position]['block_data'])
        
            sleep_compensate(start_time, 0.11)
        

        mc.setBlocks(get_x(corner[0]), 1, get_y(0), get_x(corner[0] + models['snow_plow']['width'] - 1), models['snow_plow']['height'], get_y(-models['snow_plow']['depth']), block.AIR.id)
    
        transition = None
        
    elif transition == 'trapdoor':
        mc.player.setTilePos(get_x(-1), 1, get_y(corner[1]))
        pos = mc.player.getTilePos()
        mc.player.setTilePos([test_loc[0], 1, test_loc[1]])
        
        trapdoor = minecraftstuff.MinecraftShape(mc, pos)
        trapdoor.rotate(0, 180, 0)
        trapdoor.moveBy(0, -1, 0)
        
        trapdoor.setBlocks(-corner[0] - 1,1,0,-corner[0] - number_width,1,number_height - 1, block.GLASS.id)

        mc.setBlocks(get_x(corner[0]), 0, get_y(corner[1] - 1), get_x(corner[0] + number_width - 1), 0, get_y(corner[1] + number_height - 1), block.AIR.id)
        
        
        for it_y in range(number_height):
            for it_x in range(number_width):
                    if number_dict[active_numbers[position]['number']][it_y][it_x] == '#':
                        trapdoor.setBlock(-corner[0] - 1 - it_x, 0, it_y, active_numbers[position]['block'], active_numbers[position]['block_data'])
        
        mc.setBlocks(get_x(corner[0]), 1, get_y(corner[1] - 1), get_x(corner[0] + number_width - 1), 1, get_y(corner[1] + number_height - 1), block.AIR.id)
        
        for it in range(0, 8):
            rotation_start = time.time()
            
            blocks_to_clear = []
            
            for blockToClear in trapdoor.shapeBlocks:
                blocks_to_clear.append([blockToClear.actualPos.x, blockToClear.actualPos.y, blockToClear.actualPos.z, blockToClear.blockType, blockToClear.blockData])
            
            trapdoor.visible = False
            trapdoor.rotate(0, 180 - it * 13, 0)
            
            for it_r in range(len(trapdoor.shapeBlocks)):
                blockToClear = blocks_to_clear[it_r]
                blockToDraw = trapdoor.shapeBlocks[it_r]
                if blockToDraw.actualPos.x != blockToClear[0] or blockToDraw.actualPos.y != blockToClear[1] or blockToDraw.actualPos.z != blockToClear[2] or blockToDraw.blockType != blockToClear[3] or blockToDraw.blockData != blockToClear[4]:
                    trapdoor.mc.setBlock(blockToClear[0], blockToClear[1], blockToClear[2], block.AIR.id)
                trapdoor.mc.setBlock(blockToDraw.actualPos.x, blockToDraw.actualPos.y, blockToDraw.actualPos.z, blockToDraw.blockType, blockToDraw.blockData)     

            sleep_compensate(rotation_start, 0.075)
                

        fall_distance = 50
        
        for it_fall in range(0, fall_distance):
            start_time = time.time()
            
            for it_y in range(number_height):
                for it_x in range(number_width):
                    if it_fall == fall_distance - 1:
                        mc.setBlock(get_x(corner[0] + it_x), - it_y - it_fall, get_y(corner[1]), block.AIR.id)
                    else:
                        if it_y == number_height - 1:
                            if number_dict[active_numbers[position]['number']][it_y][it_x] == '#':
                                mc.setBlock(get_x(corner[0] + it_x), -1 - it_y - it_fall, get_y(corner[1]), active_numbers[position]['block'], active_numbers[position]['block_data'])
                        else:
                            if it_y == 0 and number_dict[active_numbers[position]['number']][it_y][it_x] == '#':
                                mc.setBlock(get_x(corner[0] + it_x),-it_y - it_fall, get_y(corner[1]), block.AIR.id)
                            if number_dict[active_numbers[position]['number']][it_y][it_x] == '#' and number_dict[active_numbers[position]['number']][it_y + 1][it_x] == '0':
                                mc.setBlock(get_x(corner[0] + it_x), -1 - it_y - it_fall, get_y(corner[1]), active_numbers[position]['block'], active_numbers[position]['block_data'])
                            elif number_dict[active_numbers[position]['number']][it_y][it_x] == '0' and number_dict[active_numbers[position]['number']][it_y + 1][it_x] == '#':
                                mc.setBlock(get_x(corner[0] + it_x), -1 - it_y - it_fall, get_y(corner[1]), block.AIR.id)
            
            # time.sleep without compensation prevents big skips when lagging hard and not sleeping
            time.sleep(0.001)
            sleep_compensate(start_time, 0.15 / (it_fall + 1))
        

        trapdoor.setBlocks(-corner[0] - 1,1,0,-corner[0] - number_width,1,number_height - 1, block.GLASS.id)
        trapdoor.setBlocks(-corner[0] - 1,0,0,-corner[0] - number_width,0,number_height - 1, block.AIR.id)
        
        mc.setBlocks(get_x(corner[0]), -1, get_y(corner[1] - 1), get_x(corner[0] + number_width - 1), -number_height, get_y(corner[1] + number_height - 1), block.AIR.id)
        
        
        # trapdoor closing animation
        for it in range(0, 8):
            rotation_start = time.time()
            
            if it == 4:
                trapdoor.moveBy(0, 1, 0)
            
            blocks_to_clear = []
            
            for blockToClear in trapdoor.shapeBlocks:
                blocks_to_clear.append([blockToClear.actualPos.x, blockToClear.actualPos.y, blockToClear.actualPos.z, blockToClear.blockType, blockToClear.blockData])

            trapdoor.visible = False
            trapdoor.rotate(0, 90 + it * 13, 0)
            
            for it_r in range(len(trapdoor.shapeBlocks)):
                blockToClear = blocks_to_clear[it_r]
                blockToDraw = trapdoor.shapeBlocks[it_r]
                if blockToDraw.actualPos.x != blockToClear[0] or blockToDraw.actualPos.y != blockToClear[1] or blockToDraw.actualPos.z != blockToClear[2] or blockToDraw.blockType != blockToClear[3] or blockToDraw.blockData != blockToClear[4]:
                    trapdoor.mc.setBlock(blockToClear[0], blockToClear[1], blockToClear[2], block.AIR.id)
                trapdoor.mc.setBlock(blockToDraw.actualPos.x, blockToDraw.actualPos.y, blockToDraw.actualPos.z, blockToDraw.blockType, blockToDraw.blockData)            
            
            
            sleep_compensate(rotation_start, 0.075)
            

        mc.setBlocks(get_x(corner[0] - 1), 0, get_y(corner[1] - 1), get_x(corner[0] + number_width), 0, get_y(corner[1] + number_height), block.GLASS.id)
        mc.setBlocks(get_x(corner[0] - 1), -1, get_y(corner[1] - 1), get_x(corner[0] + number_width), -number_height, get_y(corner[1] + number_height), block.AIR.id)
                
        transition = None
    
    toggle_column()
    
    # --------------------------------------------------------------- Draw transitions ---------------------------------------------------------------
    
    if transition is None:
        transition = transitions['draw'][random.randint(0, len(transitions['draw']) - 1)] if not ClockSettings.DEBUG else 'lava'
    
    if active_numbers[position]['transition'] is None:
        transition = None
    else:
        if transition == 'lava':
            mc.player.setTilePos([test_loc[0], 1, test_loc[1]])
            set_orientation(270)
            mc.player.setTilePos(get_x(corner[0] + math.floor(number_width/2)), 1, get_y(-2))
            device.emit_click(uinput.KEY_2)
            mc.setBlock(get_x(12), camera_height - 5, get_y(7), block.AIR.id)
            
            walk(mc.player.getPos().z - get_y(corner[1] - 1), backwards=True)
            #walk_to(get_x(corner[0] + math.floor(number_width/2)), get_y(corner[1] - 1))
        
            device.emit(uinput.BTN_LEFT, 1)
            for it_y in range(number_height + 2):
                if 3 < math.sqrt((get_x(corner[0] + math.floor(number_width/2)) - mc.player.getPos().x) ** 2.0 + (get_y(corner[1] + it_y) - mc.player.getPos().z) ** 2.0):
                    # We're too far from where we should be going to
                    set_orientation(270)
                    walk_to(get_x(corner[0] + math.floor(number_width/2)), get_y(corner[1] + it_y))
                else:
                    walk(mc.player.getPos().z - get_y(corner[1] + it_y), backwards=True)
                    
                draw_hidden_block()
                for it_x in range(number_width + 2):
                    time.sleep(0.05)
                    if 0 < it_y <= number_height and 0 < it_x <= number_width:
                        if number_dict[number][it_y - 1][it_x - 1] == '#':
                            mc.setBlock(get_x(it_x + corner[0] - 1), 1, get_y(corner[1] + it_y - 1), block.LAVA.id)
                        else:
                            mc.setBlock(get_x(it_x + corner[0] - 1), 1, get_y(corner[1] + it_y - 1), block.COBBLESTONE.id)
                    else:
                        mc.setBlock(get_x(corner[0] + it_x - 1), 1, get_y(corner[1] + it_y - 1), block.COBBLESTONE.id)
            
            device.emit(uinput.BTN_LEFT, 0)
            walk_to(get_x(corner[0] + math.floor(number_width/2)), get_y(corner[1] + number_height + 2))
            
            device.emit_click(uinput.KEY_1)
            
            if slow_water_mode:
                slow_down_water()
            
            mc.setBlocks(get_x(corner[0]), 3, get_y(corner[1]), get_x(corner[0] + number_width - 1), 3, get_y(corner[1] + number_height - 1), block.WATER.id, 1)
            time.sleep(0.5)
            mc.setBlocks(get_x(corner[0] - 1), 1, get_y(corner[1] - 1), get_x(corner[0] + number_width), 1, get_y(corner[1] + number_height), block.WATER.id, 1)

            for it_y in range(number_height):
                for it_x in range(number_width):
                    if number_dict[number][it_y][it_x] == '#':
                        mc.setBlock(get_x(it_x + corner[0]), 1, get_y(corner[1] + it_y), block.OBSIDIAN.id)
            
            walk(mc.player.getPos().z - get_y(15), backwards=True)
                        
            active_numbers[position]['block'] = block.OBSIDIAN.id
            transition = None
            
        elif transition == 'draw_gravity':
            block_id = block.SAND.id if random.randint(0, 1) else block.GRAVEL.id
        
            for it_y in range(number_height):
                for it_x in range(number_width):
                    if number_dict[number][it_y][it_x] == '#':
                        mc.setBlock(get_x(it_x + corner[0]), 12, get_y(corner[1] + it_y), block_id)
                        time.sleep(0.1)
            
            active_numbers[position]['block'] = block_id
            transition = 'clear_gravity'   
            
        elif transition == 'player_place':
            mc.player.setTilePos(get_x(corner[0] + math.floor(number_width/2)), 1, get_y(-2))
            set_orientation(270)
            chosen_block = get_good_block()
            
            draw_hidden_block()
            
            walk(mc.player.getPos().z - get_y(corner[1] - 2), backwards=True)
            #walk_to(get_x(corner[0] + math.floor(number_width/2)), get_y(corner[1] - 2))
        
            for it_y in range(number_height):
                if 3 < math.sqrt((get_x(corner[0] + math.floor(number_width/2)) - mc.player.getPos().x) ** 2.0 + (get_y(corner[1] + it_y) - mc.player.getPos().z) ** 2.0):
                    # We're too far from where we should be going to
                    set_orientation(270)
                    walk_to(get_x(corner[0] + math.floor(number_width/2)), get_y(corner[1] + it_y))
                else:
                    walk(mc.player.getPos().z - get_y(corner[1] + it_y), backwards=True)
                    
                    
                for it_x in range(number_width):
                    if number_dict[number][it_y][it_x] == '#':
                        device.emit(uinput.BTN_LEFT, 1)
                        time.sleep(0.1)
                        device.emit(uinput.BTN_LEFT, 0)
                        draw_hidden_block()
                        mc.setBlock(get_x(it_x + corner[0]), 1, get_y(corner[1] + it_y), chosen_block['id'], chosen_block['data'])
                        if chosen_block['id'] == block.ICE.id:
                            mc.setBlock(get_x(it_x + corner[0]), 2, get_y(corner[1] + it_y), block.SNOW.id)

            
            walk(mc.player.getPos().z - get_y(15), backwards=True)
                        
            active_numbers[position]['block'] = chosen_block['id']
            active_numbers[position]['block_data'] = chosen_block['data']
            
            if chosen_block['id'] == block.ICE.id:
                transition = 'snow_melt'
            else:
                transition = None
    
    # Almost invisible wheat crop as exit button
    draw_hidden_block()
    
    if transition is None:
        transition = transitions['clear'][random.randint(0, len(transitions['clear']) - 1)]

    active_numbers[position]['number'] = number
    active_numbers[position]['transition'] = transition


def draw_hidden_block():
    mc.setBlock(get_x(12), camera_height - 5, get_y(7), 59, 0)


def load_models():
    #if ClockSettings.DEBUG:
        #chat('Loading models...')

    for model in models.values():
        height = 1
        width = 1
        depth = 1
        increments = 1
        
        # Getting model dimensions
        # Height
        current_block = mc.getBlockWithData(model['pos'][0], model['pos'][1] + height, model['pos'][2])
        while current_block.id == block.WOOL.id and current_block.data == 8:
            height += increments
            current_block = mc.getBlockWithData(model['pos'][0], model['pos'][1] + height, model['pos'][2])
          
        height -= increments
            
        # Width
        current_block = mc.getBlockWithData(model['pos'][0] + width, model['pos'][1], model['pos'][2])
        if current_block.id != block.WOOL.id or current_block.data != 8:
            increments = -1
            width = -1
            current_block = mc.getBlockWithData(model['pos'][0] + width, model['pos'][1], model['pos'][2])

        while current_block.id == block.WOOL.id and current_block.data == 8:
            width += increments
            current_block = mc.getBlockWithData(model['pos'][0] + width, model['pos'][1], model['pos'][2]) 
            
        width -= increments
        increments = 1
        # Depth
        current_block = mc.getBlockWithData(model['pos'][0], model['pos'][1], model['pos'][2] + depth)
        if current_block.id != block.WOOL.id or current_block.data != 8:
            increments = -1
            depth = -1
            current_block = mc.getBlockWithData(model['pos'][0], model['pos'][1], model['pos'][2] + depth)

        while current_block.id == block.WOOL.id and current_block.data == 8:
            depth += increments
            current_block = mc.getBlockWithData(model['pos'][0], model['pos'][1], model['pos'][2] + depth)
            
        depth -= increments
        
        # Storing model from dimensions
        for it_h in range(height):
            for it_w in range(abs(width)):
                for it_d in range(abs(depth)):
                    current_block = mc.getBlockWithData(model['pos'][0] + (it_w + 1 if width > 0 else -it_w - 1), model['pos'][1] + it_h + 1, model['pos'][2] + (it_d + 1 if depth > 0 else -it_d - 1))
                    if current_block.id != block.AIR.id:
                        model['block_list'].append([it_w, it_h, it_d, current_block.id, current_block.data])
                    else:
                        model['air_list'].append([it_w, it_h, it_d, current_block.id, current_block.data])

        model['width'] = abs(width)
        model['height'] = height
        model['depth'] = abs(depth)

# This method takes lag into consideration when sleeping so we don't sleep if we're already late
def sleep_compensate(start_time, sleep_time):
    time_passed = time.time() - start_time
    
    if time_passed < sleep_time:
        time.sleep(sleep_time - time_passed)


def check_for_exit():
    if ClockSettings.DEBUG:
        time.sleep(1)
        
    if mc.getBlock(get_x(12), camera_height - 5, get_y(7)) == block.AIR.id:
        chat(' Exiting...')
        #os.system('pkill -9 minecraft-pi')
        exit()


def slow_down_water():
    mc.setBlocks(test_loc[0] - 4, water_container_height + 5, test_loc[1] - 4, test_loc[0] + 4, water_container_height + 5, test_loc[1] + 4, block.WATER.id, 1)
    

if ClockSettings.DEBUG:
    chat('Debug mode')

screen_width = 25
screen_height = 15
camera_height = 10
#camera_height = 30

top_left = [0, 0]
test_loc = [get_x(-5), get_y(-5)]

number_dict = {1: ['##0',
                   '0#0',
                   '0#0',
                   '0#0',
                   '###'],
               2: ['###',
                   '00#',
                   '###',
                   '#00',
                   '###'],
               3: ['###',
                   '00#',
                   '0##',
                   '00#',
                   '###'],
               4: ['#0#',
                   '#0#',
                   '###',
                   '00#',
                   '00#'],
               5: ['###',
                   '#00',
                   '###',
                   '00#',
                   '###'],
               6: ['###',
                   '#00',
                   '###',
                   '#0#',
                   '###'],
               7: ['###',
                   '00#',
                   '0#0',
                   '0#0',
                   '0#0'],
               8: ['###',
                   '#0#',
                   '###',
                   '#0#',
                   '###'],
               9: ['###',
                   '#0#',
                   '###',
                   '00#',
                   '###'],
               0: ['###',
                   '#0#',
                   '#0#',
                   '#0#',
                   '###']}


active_numbers = {0 : {'number' : -1, 'block' : block.WOOL.id, 'block_data' : 10, 'transition' : None},
                  1 : {'number' : -1, 'block' : block.OBSIDIAN.id, 'block_data' : 0, 'transition' : None},
                  2 : {'number' : -1, 'block' : block.WOOL.id, 'block_data' : 10, 'transition' : None},
                  3 : {'number' : -1, 'block' : block.OBSIDIAN.id, 'block_data' : 0, 'transition' : None}}

good_blocks = {'gold_block': {'id': block.GOLD_BLOCK.id, 'data': 0, 'hotbar': [3, 4]},
               'wool_magenta': {'id': block.WOOL.id, 'data': 2, 'hotbar': [4, 6]},
               'wool_pink': {'id': block.WOOL.id, 'data': 6, 'hotbar': [4, 2]},
               'wool_purple': {'id': block.WOOL.id, 'data': 10, 'hotbar': [5, 0]},
               'wool_orange': {'id': block.WOOL.id, 'data': 1, 'hotbar': [4, 7]},
               'ice': {'id': block.ICE.id, 'data': 0, 'hotbar': [0, 0]},
               'grass': {'id': block.GRASS.id, 'data': 0, 'hotbar': [0, 9]}}

models = {'snow_plow': {'pos': [38.5, 0, -31.5], 'width': 0, 'height': 0, 'depth': 0, 'block_list': [], 'air_list': []}}

column_blink_delay = 1
column_visible = True

mc.player.setting('autojump', False)
silly_lag_mode = 0
#silly_lag_mode = 6
slow_water_mode = False
water_container_height = 10

clear_clock()

# ":" in the middle
toggle_column()

hours = time.strftime("%H")
minutes = time.strftime("%M")
#seconds = time.strftime("%S")

draw_number(int(hours[0]), 0)
draw_number(int(hours[1]), 1)
draw_number(int(minutes[0]), 2)
draw_number(int(minutes[1]), 3)

reset_camera()
            
mc.player.setTilePos([test_loc[0], 1, test_loc[1]])

if slow_water_mode:
    mc.setBlocks(test_loc[0] - 5, water_container_height, test_loc[1] - 5, test_loc[0] + 5, water_container_height, test_loc[1] + 5, block.GLASS.id)
    mc.setBlocks(test_loc[0] - 5, water_container_height + 1, test_loc[1] - 5, test_loc[0] - 5, water_container_height + 5, test_loc[1] + 5, block.GLASS.id)
    mc.setBlocks(test_loc[0] - 5, water_container_height + 1, test_loc[1] - 5, test_loc[0] + 5, water_container_height + 5, test_loc[1] - 5, block.GLASS.id)
    mc.setBlocks(test_loc[0] + 5, water_container_height + 1, test_loc[1] - 5, test_loc[0] + 5, water_container_height + 5, test_loc[1] + 5, block.GLASS.id)
    mc.setBlocks(test_loc[0] - 5, water_container_height + 1, test_loc[1] + 5, test_loc[0] + 5, water_container_height + 5, test_loc[1] + 5, block.GLASS.id)
    
    

import os
os.system('modprobe uinput')
import uinput

device = uinput.Device([
        uinput.BTN_LEFT,
        uinput.BTN_RIGHT,
        uinput.REL_X,
        uinput.REL_Y,
        uinput.KEY_1,
        uinput.KEY_2,
        uinput.KEY_3,
        uinput.KEY_4,
        uinput.KEY_5,
        uinput.KEY_6,
        uinput.KEY_7,
        uinput.KEY_8,
        uinput.KEY_W,
        uinput.KEY_A,
        uinput.KEY_S,
        uinput.KEY_D,
        uinput.KEY_E,
        uinput.KEY_ENTER,
        uinput.KEY_SPACE,
        ])

import minecraftstuff

wait_for_kb_and_mouse()
    
#prepare_hotbar()

device.emit(uinput.KEY_W, 0)
device.emit(uinput.KEY_S, 0)
device.emit(uinput.KEY_A, 0)
device.emit(uinput.KEY_D, 0)
device.emit(uinput.KEY_SPACE, 0)
device.emit(uinput.BTN_LEFT, 0)
device.emit(uinput.BTN_RIGHT, 0)

# Exit "button"
draw_hidden_block()

set_orientation(270)
current_orientation = get_orientation()

if silly_lag_mode:
    chat('Lag mode enabled, you\'re welcome I guess...')
    for it in range(0, screen_width, silly_lag_mode):
        mc.setBlocks(get_x(it), -1, get_y(0), get_x(it), -64, get_x(screen_height - 1), block.WATER.id, 1)

load_models()

loop_duration = 0
time_since_blink = column_blink_delay

while True:
    loop_start_time = time.time()
    hours = time.strftime("%H")
    minutes = time.strftime("%M")

    time_since_blink += loop_duration
    
    if time_since_blink >= column_blink_delay:
        time_since_blink = 0
        toggle_column()
        
    check_for_exit()
    
    if hours[0] != str(active_numbers[0]['number']):
        draw_number(int(hours[0]), 0)
        mc.player.setTilePos([test_loc[0], 1, test_loc[1]])
        toggle_column()
        hours = time.strftime("%H")
        minutes = time.strftime("%M")
        
    if hours[1] != str(active_numbers[1]['number']):
        draw_number(int(hours[1]), 1)
        mc.player.setTilePos([test_loc[0], 1, test_loc[1]])
        toggle_column()
        hours = time.strftime("%H")
        minutes = time.strftime("%M")
        
    if minutes[0] != str(active_numbers[2]['number']):
        draw_number(int(minutes[0]), 2)
        mc.player.setTilePos([test_loc[0], 1, test_loc[1]])
        toggle_column()
        hours = time.strftime("%H")
        minutes = time.strftime("%M")

    if minutes[1] != str(active_numbers[3]['number']) or ClockSettings.DEBUG:
        if ClockSettings.DEBUG: 
            active_numbers[3]['transition'] = 'trapdoor'
            
        draw_number(int(minutes[1]), 3)
        mc.player.setTilePos([test_loc[0], 1, test_loc[1]])
        
        if silly_lag_mode:
            for it in range(0, screen_width, silly_lag_mode):
                mc.setBlocks(get_x(it), -1, get_y(0), get_x(it), -1, get_x(screen_height - 1), block.WATER.id, 1)

    
    
    loop_duration = time.time() - loop_start_time
    
    if loop_duration < 0.1:
        time.sleep(0.1 - loop_duration)
        loop_duration = time.time() - loop_start_time
