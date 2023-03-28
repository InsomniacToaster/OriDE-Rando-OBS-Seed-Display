# Most of the applicable randomizer headers
logic_modes = ['Casual', 'Standard', 'Expert', 'Master', 'Glitched', 'Custom']
key_modes = ['Shards', 'Clues', 'Limitkeys', 'Free', 'Default']
goal_modes = ['ForceTrees', 'WorldTour', 'ForceMaps', 'WarmthFrags']
# variations = ['NonProgressMapStones', 'Entrance', 'Hard', 'StompTriggers', 'NoExtraExp', 'Bingo', 'Race', 'KeysOnlyForDoors', 'WarpsInsteadOfTPs', 'WarpCount', 'StartingHealth', 'StartingEnergy', 'StartingSkills', 'NoTPs']
variations = ['Starved', 'OHKO', '0XP', 'ClosedDungeons', 'OpenWorld', 'DoubleSkills', 'StrictMapstones', 'TPStarved', 'GoalModeFinish', 'WallStarved', 'GrenadeStarved', 'InLogicWarps']
item_pool = ['pool=Competitive', 'pool=BonusLite', 'pool=BonusPickups']
path_difficulty = ['prefer_path_difficulty=Easy', 'prefer_path_difficulty=Hard'] # Normal if blank
file_algorithm = ['balanced'] # Classic if blank

# user-selectable(eventually) booleans to determine what is displayed in OBS at the end
display_logic_mode = True
display_key_mode = True
display_goal_mode = True
display_selected_variations = True
display_item_pool = True
display_path_difficulty = True
display_file_algorithm = True
display_seed_name = True

seed_display = []

# loading up the randomizer.dat file
randomizer_path = r'D:\games\steam\steamapps\common\Ori DE\randomizer.dat'

with open(randomizer_path, 'r', encoding='utf-8') as f:
    dat_headers = f.readline()

# stripping newline from end of header line (if existing) and splits the data into a list
headers = headers.split("|", 1)
headers[-1] = headers[-1].strip()
headers0 = headers[0].split(",")
headers1 = headers[1]
headers = headers0
headers.append(headers1)


if display_logic_mode:
    for item in dat_headers:
        if item in logic_modes:
            seed_display.append('LogicMode=' + item)

if display_key_mode:
    for item in dat_headers:
        if item in key_modes:
            seed_display.append('KeyMode=' + item)

if display_goal_mode:
    for item in dat_headers:
        if item in goal_modes:
            seed_display.append('GoalMode=' + item)

if display_selected_variations:
    for item in dat_headers:
        if item in variations:
            seed_display.append('vars=' + item)

if display_item_pool:
    if bool(set(dat_headers) & set(item_pool)):
        for item in dat_headers:
            if item in item_pool:
                seed_display.append(item)
    else:
        seed_display.append('item_pool=Normal')

if display_path_difficulty:
    if bool(set(dat_headers) & set(path_difficulty)):
        for item in dat_headers:
            if item in path_difficulty:
                seed_display.append(item)
    else:
        seed_display.append('prefer_path_difficulty=Normal')
            
if display_file_algorithm:
    if bool(set(dat_headers) & set(file_algorithm)):
        for item in dat_headers:
            if item in file_algorithm:
                seed_display.append('file_algorithm=' + item)
    else:
        seed_display.append('file_algorithm=Classic')

if display_seed_name:
    seed_display.append('seed name =' + dat_headers[-1])

print(seed_display)