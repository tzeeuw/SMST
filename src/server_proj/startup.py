import subprocess
import os
import sys
import time
from server_proj.wol import wake_server

# open process
cmd = [sys.executable, os.getcwd() + "/tests/continous.py"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=False)


# early implementation to avoid turning on computer when people are sleeping
if not 1 < time.hour < 9:
    wake_server("3C-58-C2-4C-C8-EF", port=9)
else:
    print('Too late sorry mate')



def get_players():
    return 0

# test code to see if everything works
while True:

    # read line, remove termchars and convert to str from bits
    line = proc.stdout.readline()
    line = bytes.decode(line.strip(), "utf-8")


    print(line)

    # placeholder code
    if "left" in line:
        print('test players')
        if get_players() == 0:
            current_time = time.time()

    # some early code
    if time.time() - current_time > 5 and get_players() == 0:
        print("THIS DOES WORK")
        proc.terminate()
        break



