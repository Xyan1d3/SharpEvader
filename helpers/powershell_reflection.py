import subprocess

# powershell_reflection_generate(f"{cwd}/rev.{mode}",os.getcwd(),mode)
def powershell_reflection_generate(filepath,scriptpath,outpath):
    op = subprocess.run(f"pwsh {scriptpath}/reflection_generate.ps1 -File {filepath} -OutputFile {outpath}/rev.ps1".split(), stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return 0