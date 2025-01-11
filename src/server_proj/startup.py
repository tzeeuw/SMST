import subprocess
import time
import datetime
from server_proj.wol import wake_server

import os
import re




directory = "D:\\Minecraft\\Minecraft_server"
cmd = "start.bat"

# opens a .bat file from a specified working directory (cwd), links input/output/errors to PIPE to be able to read and write, bufsize=1 will mean that every write ended with a "\n" termination character
# will be flushed to the PIPE (thus being excecuted), shell is required to open the process and text=true removes the need of decoding the input and output strings.
proc = subprocess.Popen(cmd, cwd=directory, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, bufsize=1)





def get_player_count():
    proc.stdin.write("/list\n")
    # proc.stdin.flush()
    line = proc.stdout.readline().strip()
    print(line)
    player_count = re.search(r'\d+', line).group()

    return player_count


while True:
    line = proc.stdout.readline().strip()
    print(line)

    if "joined" in line:
        print("test")
        time.sleep(5)
        proc.stdin.write("say hello\n")
        # proc.stdin.flush()
        print("test2")
        time.sleep(1)
        print(get_player_count())

# STARTING FROM SCRATCH

# os.system("cd D:\\Minecraft\\Minecraft_server & java -Xms1G -Xmx2G -Djava.net.preferIPv4Stack=true server.jar --no-gui")

# try:
#     # open process
#     cmd = ["java", "-Xms1G", "-Xmx2G", "-Djava.net.preferIPv4Stack=true", "server.jar", "--no-gui"]
#     proc = subprocess.Popen("D:\\Minecraft\\Minecraft_server\\start.bat", stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, text=False)

#     def get_players():
#         proc.stdin.write("list players")
#         line = proc.stdout.readline()
#         players = len(line)
#         return players


#     def init_shutdown():
#         proc.stdin.write(str.encode("exit"))


#     # put entire code in class? when server is down -> create new class instance to activate

#     # test code to see if everything works
#     while True:

#         # read line, remove termchars and convert to str from bits
#         line = proc.stdout.readline()
#         line = bytes.decode(line.strip(), "utf-8")

#         if not line:
#             print(line)

#         # placeholder code
#         if "left" in line:
#             print('test players')
#             if get_players() == 0:
#                 shutdown_time = time.time()
#                 shutdown = True

#         elif "joined" in line:
#             shutdown = False

#         else:
#             shutdown_time = time.time()

#         # some early code
#         if time.time() - shutdown_time > 10 and shutdown:
#             if get_players == 0:
#                 init_shutdown()
#                 break
#             else:
#                 shutdown = False


#         if 1 < datetime.datetime.now().hour < 9:
#             init_shutdown()
#             break

# except KeyboardInterrupt:
#     print("Interrupted")
