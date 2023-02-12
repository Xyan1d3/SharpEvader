bold = "\033[1m"
teal = "\033[38;5;50m"
green = "\033[38;5;47m"
lgreen = "\033[38;5;119m"
white = "\033[37m"
purple = "\033[95m"
red = "\033[91m"
blue = "\033[34m"
orange = "\033[33m"
yellow = "\033[38;5;214m"
end = "\033[0m"


def print_success(text,level=40) :
    if level != 10:
        print(f"{bold}{lgreen}[+] {end}{text}")
def print_info(text,level=40) :
    if level != 10:
        print(f"{bold}{purple}[*] {end}{text}")
def print_error(text,level=40) : 
    if level != 10:
        print(f"{bold}{red}[-] {end}{text}")
def print_data(text,level=40) :
    if level != 10:
        print(text)

print(f"SharpEvader {bold}{orange}v2.0{end} - Made by {bold}{teal}Xyan1d3{end}\n")
