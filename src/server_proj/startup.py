import subprocess
import time
import datetime
from server_proj.wol import wake_server

import os








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
