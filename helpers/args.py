import argparse
from helpers.colorize import *

main_args = {
    "-p" : {
    "help" : "The msfvenom payload",
    "metavar" : "windows/x64/meterpreter/reverse_https"
    },
    "-lh" :{
    "help" : "The Listening Address / IP",
    "metavar" : "127.0.0.1"
    },
    "-lp" : {
    "help" : "The Listening Port",
    "metavar" : "443"
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
    args = parser.parse_args()
    return args