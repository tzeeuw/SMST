import subprocess
import os

# open process
print(os.getcwd() + "tests/continous.py")
proc = subprocess.Popen(['python', os.getcwd() + "/tests/continous.py"], stdout=subprocess.PIPE)


# test code to see if everything works
while True:
    line = proc.stdout.readline()
    if not line:
        break
    else:
        print(line)
