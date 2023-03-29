import obspython as OBS
import os.path as path

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

# Other variables
randomizer_path = ''
seed_file_name = 'randomizer.dat'
is_active = False
seed_display = []

# Description displayed in the Scripts dialog window
def script_description():
    return """Ori Rando Seed Variables
            Parses the randomizer.dat and adds the headers you'd like to see into a text source."""

def script_properties():
    props = OBS.obs_properties_create()
    #Allows user to select the Ori DE application path
    OBS.obs_properties_add_path(props, "randomizer_path", 'Ori DE Directory Path', OBS.OBS_PATH_DIRECTORY, '', 'C:/Program Files (x86)/Steam/steamapps/common/Ori DE')
    return props

def script_load(settings):
    global randomizer_path

    randomizer_path = OBS.obs_data_get_string(settings, "randomizer_path")
    OBS.script_log(OBS.LOG_INFO, '2023-03-28_20:11')

    # set hotkey
    global hotkey_id
    hotkey_id = OBS.obs_hotkey_register_frontend()


with open(randomizer_path, 'r', encoding='utf-8') as f:
    headers = f.readline()

# stripping newline from end of header line (if existing) and splits the data into a list
headers = headers.split("|", 1)
headers[-1] = headers[-1].strip()
headers0 = headers[0].split(",")
headers1 = headers[1]
headers = headers0
headers.append(headers1)


if display_logic_mode:
    for item in headers:
        if item in logic_modes:
            seed_display.append('LogicMode=' + item)

if display_key_mode:
    for item in headers:
        if item in key_modes:
            seed_display.append('KeyMode=' + item)

if display_goal_mode:
    for item in headers:
        if item in goal_modes:
            seed_display.append('GoalMode=' + item)

if display_selected_variations:
    for item in headers:
        if item in variations:
            seed_display.append('vars=' + item)

if display_item_pool:
    if bool(set(headers) & set(item_pool)):
        for item in headers:
            if item in item_pool:
                seed_display.append(item)
    else:
        seed_display.append('item_pool=Normal')

if display_path_difficulty:
    if bool(set(headers) & set(path_difficulty)):
        for item in headers:
            if item in path_difficulty:
                seed_display.append(item)
    else:
        seed_display.append('prefer_path_difficulty=Normal')
            
if display_file_algorithm:
    if bool(set(headers) & set(file_algorithm)):
        for item in headers:
            if item in file_algorithm:
                seed_display.append('file_algorithm=' + item)
    else:
        seed_display.append('file_algorithm=Classic')

if display_seed_name:
    seed_display.append('seed name =' + headers[-1])

print(seed_display)