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


def print_success(text) :
    print(f"{bold}{lgreen}[+] {end}{text}")
def ainfo(text) :
    print(f"{bold}{purple}[*] {end}{text}")
def aerr(text) : 
    print(f"{bold}{red}[-] {end}{text}")

print(f"SharpEvader {bold}{orange}v2.0{end} - Made by {bold}{teal}Xyan1d3{end}")
