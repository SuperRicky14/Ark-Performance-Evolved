from rich.console import Console
from rich.rule import Rule
import shutil
import json
import os

console = Console()

license_text = (
    "MIT License",
    "",
    "Copyright (c) 2023 SuperRicky14",
    "",
    "Permission is hereby granted, free of charge, to any person obtaining a copy",
    "of this software and associated documentation files (the 'Software'), to deal",
    "in the Software without restriction, including without limitation the rights",
    "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell",
    "copies of the Software, and to permit persons to whom the Software is",
    "furnished to do so, subject to the following conditions:",
    "",
    "The above copyright notice and this permission notice shall be included in all",
    "copies or substantial portions of the Software.",
    "",
    "THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR",
    "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,",
    "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE",
    "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER",
    "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,",
    "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE",
    "SOFTWARE."
)

console.print(Rule("[bold green]Beginning of LICENSE agreement[/bold green]"))
for line in license_text:
    print(line)
console.print(Rule("[bold green]End of LICENSE agreement[/bold green]"))

if not os.path.exists("LICENSE"):
    with open("LICENSE", "w") as license:
        for line in license_text:
            license.write(line + "\n")

user_input = console.input("[bold magenta]Do you agree to the terms?[/bold magenta] [bold yellow][y/n][/bold yellow]: ")
if not (user_input.lower() == "y"):
    console.print(Rule("[red]You did not agree to the terms. Exiting...[/red]"))
    os.system("PAUSE")
    exit()
else:
    console.print(Rule("[cyan]You agree to the terms and conditions.[/cyan]"))

# check if the patches are installed
if not os.path.exists("BaseScalability.ini") or not os.path.exists("Engine.ini"):
    console.print(Rule("[red]The program's installation is corrupted and / or unreadable[/red]"))
    os.system("PAUSE")
    exit()

global configuration; configuration = {
    "_ark_installation_path": {
        "path": "<path>",
        "_comment": {
            "example_path": "E:/SteamLibrary/steamapps/common/ARK",
            "how_to_find_it": "Go to steam, then right click \"Ark: Survival Evolved\" then click \"Browse Local Files\" and copy the path!"
        }
    },
    "_patches": 
    {
        "basescalability_patch": {
            "enabled": False,
            "file_affected": "/Engine/Config/BaseScalability.ini",
            "description": "This is a total overhaul of the scalability groups used in ARK:SE with a focus on increasing visual quality at the high end, and performance at the low end. The Epic settings in this rework are built to push circa-2020 GPUs much harder than the defaults, while the Medium and Low settings should open up more performance to lower-end hardware than is possible with the defaults.",
            "link": "https://steamcommunity.com/sharedfiles/filedetails/?id=1914356037",
            "author": "lordbean (https://steamcommunity.com/id/lordbean)",
        },

        "engine_patch": {
            "enabled": False,
            "file_affected": "/ShooterGame/Saved/Config/WindowsNoEditor/Engine.ini",
            "description": "This is a total overhaul of the scalability groups used in ARK:SE with a focus on increasing visual quality at the high end, and performance at the low end. The Epic settings in this rework are built to push circa-2020 GPUs much harder than the defaults, while the Medium and Low settings should open up more performance to lower-end hardware than is possible with the defaults.",
            "link": "https://steamcommunity.com/sharedfiles/filedetails/?id=2356992556",
            "author": "Few (https://steamcommunity.com/id/AndreikaRPM)"
        },

        "disable_mouse_acceleration": {
            "enabled": False,
            "file_affected": "/Engine/Config/BaseInput.ini",
            "description": "Forcefully disables mouse acceleration and smoothing in ARK:SE which causes it to feel weird / different compared to other games and application",
            "link": "https://eliteownage.com/arksurvivalevolvedmousefixes.html",
            "author": "Unknown"
        }
    }
}

def load_configuration():
    global configuration
    with open("config.json", "r") as cfg:
        configuration = json.load(cfg)

def generate_configuration():
    if os.path.exists("config.json"):
        console.print(Rule("[cyan]Detected existing configuration![/cyan]"))
        try:
            load_configuration()
        except json.JSONDecodeError:
            console.print(Rule("[red]Failed to load existing configuration! Malformed JSON[/red]"))
            console.print_exception()
            os.system("PAUSE")
            exit()
        console.print()
        if not os.path.exists(configuration["_ark_installation_path"]["path"]):
            console.print(Rule("[red]ARK installation path not found![/red]"))
            os.system("PAUSE")
            exit()
        # check for /Engine/Config and 
        if not os.path.exists(f"{configuration["_ark_installation_path"]["path"]}/Engine/Config") or not os.path.exists(f"{configuration["_ark_installation_path"]["path"]}/ShooterGame/Saved/Config/WindowsNoEditor/"):
            console.print(Rule("[red]ARK installation is corrupted and / or unreadable[/red]"))
            os.system("PAUSE")
            exit()
    else:
        console.print(Rule("[green]Generating new configuration...[/green]"))
        with open("config.json", "w") as cfg:
            json.dump(configuration, cfg, indent=4)
        console.print(Rule("[green]...Complete![/green]"))

generate_configuration()

console.print(Rule("[bold magenta]Beginning of configuration[/bold magenta]"))
console.print_json(json.dumps(configuration, indent=4))
console.print(Rule("[bold magenta]End of configuration[/bold magenta]"))

engine_config_path = f"{configuration["_ark_installation_path"]["path"]}/Engine/Config"
windowsnoeditor_config_path = f"{configuration["_ark_installation_path"]["path"]}/ShooterGame/Saved/Config/WindowsNoEditor/"
mouse_smoothing_config_path = f"{configuration['_ark_installation_path']['path']}/Engine/Config/BaseInput.ini"

# seperate it to make it easier to look at
print("")

# if basescalability is enabled, apply the patch
if (configuration["_patches"]["basescalability_patch"]["enabled"]):
    shutil.copy("BaseScalability.ini", f"{engine_config_path}")
    console.print(Rule("Applied patch: [bold magenta]basescalability[/bold magenta]"))
# if engine patch is enabled, apply the patch
if (configuration["_patches"]["engine_patch"]["enabled"]):
    shutil.copy("Engine.ini", f"{windowsnoeditor_config_path}")
    console.print(Rule("Applied patch: [bold magenta]engine[/bold magenta]"))
# if disable_mouse_acceleration is enabled, apply the patch
if (configuration["_patches"]["disable_mouse_acceleration"]["enabled"]):
    # Check if "[/Script/Engine.InputSettings]" exists, and if not, insert it to the top of BaseInput.ini
    if not os.path.exists(mouse_smoothing_config_path):
        console.print(Rule("[red]BaseInput.ini not found![/red]"))
        console.print(Rule("[red]The program's installation is corrupted and / or unreadable[/red]"))
        os.system("PAUSE")
        exit()

    with open(mouse_smoothing_config_path, 'r') as base_input_file:
        base_input_lines = base_input_file.readlines()

    found_bEnableMouseSmoothing = False
found_script_input_settings = False
bEnableMouseSmoothing_index = 0
input_settings_index = 0

for index, line in enumerate(base_input_lines):
    if "[/Script/Engine.InputSettings]" in line:
        found_script_input_settings = True
        input_settings_index = index

    if "bEnableMouseSmoothing" in line:
        if "true" in line:
            # Check if "bEnableMouseSmoothing" is in BaseInput.ini
            found_bEnableMouseSmoothing = True
            bEnableMouseSmoothing_index = index
            line = line.replace("true", "false")
            base_input_lines[index] = line
        if "false" in line:
            found_bEnableMouseSmoothing = True
            bEnableMouseSmoothing_index = index

if not found_script_input_settings:
    if found_bEnableMouseSmoothing:
        base_input_lines.insert(bEnableMouseSmoothing_index - 1, "[/Script/Engine.InputSettings]\n\n")
    else:
        input_settings_index = 0
        base_input_lines.insert(0, "[/Script/Engine.InputSettings]\n\n")

if not found_bEnableMouseSmoothing:
    base_input_lines.insert(input_settings_index + 1, "\nbEnableMouseSmoothing=false")


with open(mouse_smoothing_config_path, 'w') as base_input_file:
    base_input_file.writelines(base_input_lines)

    console.print(Rule("Applied patch: [bold magenta]disable_mouse_acceleration[/bold magenta]"))

print("")
console.print(Rule("[bold dark_orange3]Patching Complete![/bold dark_orange3] Automatic Launch Arguments optimization coming soon!"))
console.print(Rule("Expect a [yellow]decent performance improvement![/yellow]"))
os.system("PAUSE")