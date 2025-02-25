import subprocess

cmd = "test_cmd.bat"
cmd_dir = "C:\\Users\\thijs\\SMST\\tests"
proc = subprocess.Popen(
    cmd,
    cwd=cmd_dir,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True,
    text=True,
    bufsize=1
)

def readline():
    return proc.stdout.readline()

for line in iter(readline, ''):
    print(line.strip())

