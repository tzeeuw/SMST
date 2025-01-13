import subprocess
import time
import datetime
from server_proj.wol import wake_server

import os
import re


class mc_server():
    def __init__(self):
        self.idle_loop()

    def server_start(self):
        directory = "D:\\Minecraft\\Minecraft_server"
        cmd = "start.bat"

        # opens a .bat file from a specified working directory (cwd), links input/output/errors to PIPE to be able to read and write, bufsize=1 will mean that every write ended with a "\n" termination character
        # will be flushed to the PIPE (thus being excecuted), shell is required to open the process and text=true removes the need of decoding the input and output strings.
        self.proc = subprocess.Popen(cmd, cwd=directory, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, bufsize=1)

    def server_stop(self):
        self.proc.stdin.write("stop\n")
        time.sleep(10)
        self.idle_loop()

    def server_loop(self):
        while True:
            line = self.proc.stdout.readline().strip()
            print(line)

            if "left" in line:
                print(self.get_player_count())

    def idle_loop(self):
        pass

        


    def get_player_count(self):

        self.proc.stdin.write("/list\n")
        line = self.proc.stdout.readline().strip()
        player_count = re.search(r'\d+', line).group()

        return player_count
