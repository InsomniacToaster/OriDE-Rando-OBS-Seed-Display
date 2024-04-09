# Overview
This addon is forked from [JHobz's](https://github.com/jhobz/ori-obs-scripts) original Lua script, and has been updated for compatibility with the current Ori DE Randomizer DLL. The intent of this script is to allow you to display the Ori DE Randomizer seed name and/or parameters in OBS without having to manually update the text each time. 

This has been tested to work on Windows, and may not be compatible with other Operating Systems.

# Installation
Ensure you have the latest version of [Python](https://www.python.org/) supported by OBS (At the time of writing, OBS 30.1.0 supports Python 3.11.x, which can be downloaded [here](https://www.python.org/downloads/windows/).)

Ensure OBS is pointing to your Python 3.11.x directory (In OBS Studio go to Tools -> Scripts -> Python Settings, and ensure the path is pointed to your Python311 installation directory)

![image](https://github.com/InsomniacToaster/OriDE-Rando-OBS-Seed-Display/assets/89503619/86156c81-2b14-475b-87ce-2147aaf758c8)

Download the latest `ori_rando_seed_name.py` file from [releases](https://github.com/InsomniacToaster/OriDE-Rando-OBS-Seed-Display/releases)

In OBS Studio, go to Tools -> Scripts -> + and find the file you downloaded.

# Usage
In the script properties:

* Set the text source you want to be populated.
* Set the path to the directory where your randomizer.dat file is located (usually the Ori DE folder in steamapps\common).
* Customize the seed parameters to your liking.

![image](https://github.com/InsomniacToaster/OriDE-Rando-OBS-Seed-Display/assets/89503619/37e8f777-7db4-4ca3-b652-e6a2f4396fbd)


In OBS properties:

* Go to Hotkeys and add a hotkey for "Ori Rando Seed Headers" (recommended: Alt+L as this will coincide with the default "Load Seed" command in the Ori randomizer).

Now anytime you press the registered hotkey, your text source will populate with whichever parameters you have selected.

# Credits
Special thanks again to [JHobz](https://github.com/jhobz) for the original work and giving me the "ok" to fork/update it.
