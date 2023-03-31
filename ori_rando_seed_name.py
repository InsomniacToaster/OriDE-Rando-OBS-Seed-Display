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

# user-selectable booleans to determine what is displayed in OBS at the end
display_logic_mode = False
display_key_mode = False
display_goal_mode = False
display_selected_variations = False
display_item_pool = False
display_path_difficulty = False
display_file_algorithm = False
display_seed_name = False

# Other variables
hotkey_id = OBS.OBS_INVALID_HOTKEY_ID
randomizer_path = ''
source_name = ''
seed_file_name = 'randomizer.dat'
is_active = False
seed_display = []

# Description displayed in the Scripts dialog window
def script_description():
    return """Ori Rando Seed Headers
            Parses the randomizer.dat and adds the headers you'd like to see into a text source."""

def script_properties():
    props = OBS.obs_properties_create()
    # Allows user to select the Ori DE application path
    OBS.obs_properties_add_path(props, "randomizer_path", 'Ori DE Directory Path', OBS.OBS_PATH_DIRECTORY, '', 'C:/Program Files (x86)/Steam/steamapps/common/Ori DE')

    # Allows user to select source
    list_property = OBS.obs_properties_add_list(props, "source_name", 'Source: ', OBS.OBS_COMBO_TYPE_LIST, OBS.OBS_COMBO_FORMAT_STRING)
    
    # Button to refresh the drop-down list
    OBS.obs_properties_add_button(props, "button", "Refresh list of sources: ",
                                  lambda props,prop: True if populate_list_property_with_source_names(list_property) else True)
    populate_list_property_with_source_names(list_property)   
    # Specific variables for which headers the user wants to show
    OBS.obs_properties_add_bool(props, "display_logic_mode", 'Display logic mode: ')
    OBS.obs_properties_add_bool(props, "display_key_mode", 'Display key mode: ')
    OBS.obs_properties_add_bool(props, "display_goal_mode", 'Display goal mode: ')
    OBS.obs_properties_add_bool(props, "display_selected_variations", 'Display selected variations: ')
    OBS.obs_properties_add_bool(props, "display_item_pool", 'Display item pool: ')
    OBS.obs_properties_add_bool(props, "display_path_difficulty", 'Display path difficulty: ')
    OBS.obs_properties_add_bool(props, "display_file_algorithm", 'Display file algorithm: ')
    OBS.obs_properties_add_bool(props, "display_seed_name", 'Display seed name: ')
    
    return props

def script_update(settings):
    global display_logic_mode, display_key_mode, display_goal_mode, display_selected_variations, display_item_pool, display_path_difficulty, display_file_algorithm, display_seed_name, source_name
    display_logic_mode = OBS.obs_data_get_bool(settings, "display_logic_mode")
    display_key_mode = OBS.obs_data_get_bool(settings, "display_key_mode")
    display_goal_mode = OBS.obs_data_get_bool(settings, "display_goal_mode")
    display_selected_variations = OBS.obs_data_get_bool(settings, "display_selected_variations")
    display_item_pool = OBS.obs_data_get_bool(settings, "display_item_pool")
    display_path_difficulty = OBS.obs_data_get_bool(settings, "display_path_difficulty")
    display_file_algorithm = OBS.obs_data_get_bool(settings, "display_file_algorithm")
    display_seed_name = OBS.obs_data_get_bool(settings, "display_seed_name")
    source_name = OBS.obs_data_get_string(settings, 'source_name')

def script_load(settings):
    global display_logic_mode
    global display_key_mode
    global display_goal_mode
    global display_selected_variations
    global display_item_pool
    global display_path_difficulty
    global display_file_algorithm
    global display_seed_name
    global seed_display
    global randomizer_path
    global source_name

    randomizer_path = OBS.obs_data_get_string(settings, "randomizer_path")

    # set hotkey
    global hotkey_id
    hotkey_id = OBS.obs_hotkey_register_frontend(script_path(), 'Ori Rando Seed Headers', ori_seed_headers_hotkey)
    hotkey_save_array = OBS.obs_data_get_array(settings, "oriseedheaders_hotkey")
    OBS.obs_hotkey_load(hotkey_id, hotkey_save_array)
    OBS.obs_data_array_release(hotkey_save_array)

def script_save(settings):
    # Hotkey save
    hotkey_save_array = OBS.obs_hotkey_save(hotkey_id)
    OBS.obs_data_set_array(settings, "oriseedheaders_hotkey", hotkey_save_array)
    OBS.obs_data_array_release(hotkey_save_array)

# Fills the given list property object with the names of all sources plus an empty one
def populate_list_property_with_source_names(list_property):
    sources = OBS.obs_enum_sources()
    OBS.obs_property_list_clear(list_property)
    OBS.obs_property_list_add_string(list_property, "", "")
    for source in sources:
        source_id = OBS.obs_source_get_id(source)
        if source_id == 'text_gdiplus_v2':
            name = OBS.obs_source_get_name(source)
            OBS.obs_property_list_add_string(list_property, name, name)
    OBS.source_list_release(sources)

def populate_headers(rpath, filename):
    global display_logic_mode
    global display_key_mode
    global display_goal_mode
    global display_selected_variations
    global display_item_pool
    global display_path_difficulty
    global display_file_algorithm
    global display_seed_name
    global seed_display
    global source_name

    if path.exists(rpath + '\\' + filename):
        with open((rpath + '\\' + filename), 'r', encoding='utf-8') as f:
            headers = f.readline()

        # stripping newline from end of header line (if existing) and splits the data into a list
        headers = headers.split("|", 1)
        headers[-1] = headers[-1].strip()
        headers0 = headers[0].split(",")
        headers1 = headers[1]
        headers = headers0
        headers.append(headers1)
        seed_display = []

        if display_logic_mode:
            for item in headers:
                if item in logic_modes:
                    seed_display.append('LogicMode=' + item + '|')

        if display_key_mode:
            for item in headers:
                if item in key_modes:
                    seed_display.append('KeyMode=' + item + '|')

        if display_goal_mode:
            for item in headers:
                if item in goal_modes:
                    seed_display.append('GoalMode=' + item + '|')

        if display_selected_variations:
            for item in headers:
                if item in variations:
                    seed_display.append('vars=' + item + '|')

        if display_item_pool:
            if bool(set(headers) & set(item_pool)):
                for item in headers:
                    if item in item_pool:
                        seed_display.append(item + '|')
            else:
                seed_display.append('pool=Normal' + '|')

        if display_path_difficulty:
            if bool(set(headers) & set(path_difficulty)):
                for item in headers:
                    if item in path_difficulty:
                        seed_display.append('path difficulty =' + item + '|')
            else:
                seed_display.append('path difficulty=Normal' + '|')
                    
        if display_file_algorithm:
            if bool(set(headers) & set(file_algorithm)):
                for item in headers:
                    if item in file_algorithm:
                        seed_display.append('file_algorithm=' + item + '|')
            else:
                seed_display.append('file_algorithm=Classic' + '|')

        if display_seed_name:
            seed_display.append('seed name =' + headers[-1])

        temp_seed_display = ''
        for item in seed_display:
            temp_seed_display += item
        seed_display = temp_seed_display

        update_source_text()
    else:
        OBS.script_log(OBS.LOG_INFO, 'File does not exist!')

def update_source_text():
    global source_name, seed_display
    src = OBS.obs_get_source_by_name(source_name)
    textset = OBS.obs_data_create()
    OBS.obs_data_set_string(textset, 'text', seed_display)
    OBS.obs_source_update(src, textset)
    OBS.obs_data_release(textset)
    OBS.obs_source_release(src)

#Callback for the hotkey
def ori_seed_headers_hotkey(pressed):
    if pressed:
        populate_headers(randomizer_path, seed_file_name)