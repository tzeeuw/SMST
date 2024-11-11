import subprocess
import os
import sys
import time

# open process
cmd = [sys.executable, os.getcwd() + "/tests/continous.py"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=False)


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



