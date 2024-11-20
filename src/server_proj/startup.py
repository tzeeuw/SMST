import subprocess
import time
import datetime
from server_proj.wol import wake_server

# open process
cmd = ["java", "Xms1G", "Xmx2G", "server.jar", "--no-gui"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=False)


def get_players():
    proc.stdin.write("list players")
    line = proc.stdout.readline()
    players = len(line)
    return players


def init_shutdown():
    proc.stdin.write("exit")


# put entire code in class? when server is down -> create new class instance to activate

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
            shutdown = True

    elif "joined" in line:
        shutdown = False

    # some early code
    if time.time() - current_time > 10 and shutdown:
        if get_players == 0:
            init_shutdown()
            break
        else:
            shutdown = False


    if  not 1 < datetime.datetime.now().hour < 9:
        init_shutdown()
        break

