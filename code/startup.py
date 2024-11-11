import subprocess
import os
import time

# open process
print(os.getcwd() + "tests/continous.py")
proc = subprocess.Popen(['python', os.getcwd() + "/tests/continous.py"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)


def getplayers():
    return 0

# test code to see if everything works
while True:
    print('WTF')
    line = proc.stdout.readline()
    if not line:
        break
    else:
        line = bytes.decode(line)

        if str(9) not in line:
            print(line)
        if "left" in line:
            print('test players')
            if getplayers() == 0:
                current_time = time.time()

        if time.time() - current_time > 5 and getplayers() == 0:
            print("THIS DOES NOT WORK")
            proc.communicate(input=bytes('^Z\n', encoding="utf-8"))
            proc.terminate()
            


