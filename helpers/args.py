import argparse
from helpers.colorize import *

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
    "help" : "Shellcode Injection Technique\nHello world\nHello world\nHello world",
    #"choices" : [1,2,3,4],
    "required" : False
    },
    "-bb" : {
    "help" : "Behaviour Bypass Technique",
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
    
    evasion_group = parser.add_argument_group("Evasion Options", "Evasion Payload modification")
    for param in evasion_args.keys():
        evasion_group.add_argument(param,**evasion_args[param])
    testing = parser.add_argument_group("Debugging", "For Debugging Purposes")
    for param in testing_args.keys():
        testing.add_argument(param,**testing_args[param])
    args = parser.parse_args()
    return args