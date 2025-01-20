import subprocess
import time
import datetime
import socket
from contextlib import closing
import threading


class mc_server():
    def __init__(self):
        self._server_is_alive = False

    def server_start(self):
        directory = "D:\\Minecraft\\Minecraft_server"
        cmd = "start.bat"

        # opens a .bat file from a specified working directory (cwd), links input/output/errors to PIPE to be able to read and write, bufsize=1 will mean that every write ended with a "\n" termination character
        # will be flushed to the PIPE (thus being excecuted), shell is required to open the process and text=true removes the need of decoding the input and output strings.
        self.proc = subprocess.Popen(cmd, cwd=directory, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, bufsize=1)
        self._server_is_alive = True
        self.server_loop()


    def server_stop(self):
        self.proc.stdin.write("stop\n")
        for line in self.proc.stdout.readlines():
            print(line)
        time.sleep(10)
        self.idle_loop()


    def server_loop(self):
        thread = threading.Thread(target=self.server_countdown)
        self.shutdown_server = False

        while True:
            line = self.proc.stdout.readline().strip()
            print(line)

            if "left" in line:
                if int(self.get_player_count()) == 0 and not thread.is_alive():
                    thread.start()

            if "joined" in line and thread.is_alive():
                self.kill_thread = True
                thread.join()
                print("thread broken")

                thread = threading.Thread(target=self.server_countdown)

            if self.shutdown_server:
                self.server_stop()


    def server_countdown(self):
        self.kill_thread = False

        for _ in range(10):
            time.sleep(1)
            print(_)
            if self.kill_thread:
                return

        print("server is stopping")
        self.proc.stdin.write("say Server is shutting down\n")
        self.shutdown_server = True


    def idle_loop(self):
        with socket.socket() as sock:
            sock.bind(( "yep this was definetely here during time of commit", 42070))
            sock.listen()

            (proxy_socket, proxy_address) = sock.accept()
            message = proxy_socket.recv(1024).decode()

            print(message)

            if message == "Alive?":
                if self._server_is_alive:
                    proxy_socket.send("yes".encode())

                else:
                    proxy_socket.send("no".encode())
                    proxy_socket.close()
                    sock.close()
                    self.server_start()

        
    def get_player_count(self):

        self.proc.stdin.write("/list\n")
        line = self.proc.stdout.readline().strip()
        print(line)
        player_count = line[line.index("of a max")-2] # very rudementairy should change it to be more rigorous

        return player_count


if __name__ == "__main__":
    server = mc_server()
    server.server_start()
