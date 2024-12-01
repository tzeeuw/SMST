import subprocess
import os
import sys
import time
import datetime
from server_proj.wol import wake_server

# open process
directory = "C:\\Users\\Thijs\\Minecraft_server"
cmd = "start.bat"
proc = subprocess.Popen(cmd, cwd=directory, stdin=subprocess.PIPE, shell=True, text=True)



time.sleep(20)
proc.stdin.write("stop\n")
proc.communicate()
proc.stdin.write("f\n")
proc.communicate()

def get_players():
    proc.stdin.write("/list")
    line = proc.stdout.readline()
    players = next(filter(line.isdigit))
    return players


def init_shutdown():
    proc.stdin.write("exit")


# put entire code in class? when server is down -> create new class instance to activate
# current_time = 0
# shutdown = False
# # test code to see if everything works
# while True:

#     # read line, remove termchars and convert to str from bits
#     line = proc.stdout.readline()
#     line = bytes.decode(line.strip(), "utf-8")

#     print(line)

#     # placeholder code
#     if "left" in line:
#         print('test')
#         if get_players() == 0:
#             proc.stdin.write("test")
#             current_time = time.time()
#             shutdown = True

#     elif "joined" in line:
#         shutdown = False

#     # some early code
#     if time.time() - current_time > 10 and shutdown:
#         if get_players == 0:
#             init_shutdown()
#             break
#         else:
#             shutdown = False


#     if  not 1 < datetime.datetime.now().hour < 9:
#         init_shutdown()
#         break

