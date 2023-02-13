import os
import yaml
import argparse
from helpers.colorize import *


script_path = os.path.dirname(os.path.abspath(__file__))
with open(f"{script_path}/../payloads/injection_templates/injection_list.yaml","r") as f:
    evasion_style = yaml.load(f, Loader=yaml.SafeLoader)
with open(f"{script_path}/../payloads/behaviour_bypass/behaviour_bypass.yaml","r") as f:
    behaviour_bypass = yaml.load(f, Loader=yaml.SafeLoader)

# Creating a list of the available shellcode injection templates
available_evasion_csharp_templates = list(evasion_style["payload_types"].keys())
available_behaviour_bypass_templates = list(behaviour_bypass["behaviour_detection_bypass"].keys())

help_evasion_csharp_templates = ""
help_behaviour_bypass_templates = ""

for each in available_evasion_csharp_templates:
    help_evasion_csharp_templates += f"{lgreen}{bold}{each}{end} : {evasion_style['payload_types'][each]['process_name']}\n"

for each in available_behaviour_bypass_templates:
    help_behaviour_bypass_templates += f"{lgreen}{bold}{each}{end} : {behaviour_bypass['behaviour_detection_bypass'][each]['title']}\n"


main_args = {
    "-p" : {
    "help" : "The msfvenom payload",
    "metavar" : "windows/x64/meterpreter/reverse_https",
    "required" : True
    },
    "-lh" :{
    "help" : "The Listening Address / IP",
    "metavar" : "127.0.0.1",
    "required" : True
    },
    "-lp" : {
    "help" : "The Listening Port",
    "metavar" : "443",
    "required" : True
    }
}

optional_args = {
    "-nobin" : {
    "help" : "Disables generation of exe/dll payloads(Generates only reflection ps1) [Default : False]",
    "action" : "store_true",
    "required" : False
    },
    "-dll" : {
    "help" : "Generates dll payload instead of exe [Default : False]",
    "action" : "store_true",
    "required" : False
    },
    "-nops1" : {
    "help" : "Disables generation of powershell reflection payload [Default : False]",
    "action" : "store_true",
    "required" : False
    }
}

testing_args = {
    "-v" : {
    "help" : "Enables verbose logging",
    "action" : "store_true",
    "required" : False
    }
}

evasion_args = {
    "-sit" : {
    "help" : f"Shellcode Injection Technique\n{help_evasion_csharp_templates}",
    "choices" : available_evasion_csharp_templates,
    "required" : False
    },
    "-bb" : {
    "help" : f"Behaviour Bypass Technique\n{help_behaviour_bypass_templates}",
    "choices" : available_behaviour_bypass_templates,
    "required" : False
    }
}

def generate_cli_args():
    global parser 
    parser= argparse.ArgumentParser(description=f"""{bold}{orange} ____  _                      _____                _ 
/ ___|| |__   __ _ _ __ _ __ | ____|_   ____ _  __| | ___ _ __
{bold}{lgreen}\___ \| '_ \ / _` | '__| '_ \|  _| \ \ / / _` |/ _` |/ _ \ '__|
{bold}{yellow} ___) | | | | (_| | |  | |_) | |___ \ V / (_| | (_| |  __/ |
{bold}{teal}|____/|_| |_|\__,_|_|  | .__/|_____| \_/ \__,_|\__,_|\___|_|
{bold}{red}                       |_|                                     
{end}""",formatter_class=argparse.RawTextHelpFormatter)
    for param in main_args.keys():
        parser.add_argument(param,**main_args[param])
    
    optional = parser.add_argument_group("Payload Formats", "Options for modifying payload formats")
    for param in optional_args.keys():
        optional.add_argument(param,**optional_args[param])
    evasion_group = parser.add_argument_group("Evasion Options", "Evasion Payload Arguments")
    for param in evasion_args.keys():
        evasion_group.add_argument(param,**evasion_args[param])
    testing = parser.add_argument_group("Debugging", "For Debugging Purposes")
    for param in testing_args.keys():
        testing.add_argument(param,**testing_args[param])
    args = parser.parse_args()
    return args