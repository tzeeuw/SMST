import subprocess

cmd = "test_cmd.bat"
cmd_dir = "C:\\Users\\thijs\\Python\\server_proj\\tests"
proc = subprocess.Popen(
    cmd,
    cwd=cmd_dir,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True,
    text=True,
)

while True:
    print("wat")
    print(proc.stdout.readline())

