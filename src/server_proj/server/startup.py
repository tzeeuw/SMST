import subprocess
import time
import datetime
import socket
from contextlib import closing
import threading
import os


testing = True
directory = "D:\\Minecraft\\fabric_test"
command = "start.bat"


class mc_server():
    def __init__(self, directory, command):
        self._server_is_alive = False
        self.directory = directory
        self.command = command

    def server_start(self):


        # opens a .bat file from a specified working directory (cwd), links input/output/errors to PIPE to be able to read and write, bufsize=1 will mean that every write ended with a "\n" termination character
        # will be flushed to the PIPE (thus being excecuted), shell is required to open the process and text=true removes the need of decoding the input and output strings.
        self.proc = subprocess.Popen(self.command, cwd=self.directory, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, bufsize=1)
        self._server_is_alive = True
        self.server_loop()


    def server_stop(self):
        self.proc.stdin.write("stop\n")
        for line in self.proc.stdout.readlines():
            print(line.split())

        if MANUAL_START:
            self.idle_loop(t_sec=0)
        
        else:
            self.idle_loop(t_sec=5*60)


    def input_thread(self):
        user_input = input("")
        self.proc.stdin.write(f"{user_input}\n")
        return



    def server_loop(self):
        thread = threading.Thread(target=self.server_countdown, args=(10*60,))
        input_thread = threading.Thread(target=self.input_thread)

        self.shutdown_server = False

        input_thread.start()

        while True:
            line = self.proc.stdout.readline().strip()
            print(line)

            if not input_thread.is_alive():
                input_thread = threading.Thread(target=self.input_thread)
                input_thread.start()

            if "left" in line or "pause" in line:
                if int(self.get_player_count()) == 0 and not thread.is_alive():
                    thread.start()

            if "joined" in line and thread.is_alive():
                self.kill_thread = True
                thread.join()
                print("thread broken")

                thread = threading.Thread(target=self.server_countdown, args=(10*60,))

            if self.shutdown_server:
                break
                
        self.server_stop()



    def server_countdown(self, t_sec):
        self.kill_thread = False

        for t in range(t_sec):
            time.sleep(1)
            print(t)
            if self.kill_thread:
                return

        print("server is stopping")
        self.proc.stdin.write("say Server is shutting down\n")
        self.shutdown_server = True


    def shutdown_countdown(self, t_sec):
        self.kill_thread = False

        for t in range(t_sec):
            time.sleep(1)
            print(t)
            if self.kill_thread:
                return

        with closing(socket.socket()) as sock:
            sock.connect(( "yep this was definetely here during time of commit", 42070))
            sock.send("shutdown".encode())



    def idle_loop(self, t_sec=0):

        if t_sec:
            thread = threading.Thread(target=self.shutdown_countdown, args=(t_sec,))
            thread.start()


        with closing(socket.socket()) as sock:
            sock.bind(( "yep this was definetely here during time of commit", 42070))

            while True:
                sock.listen()

                (proxy_socket, proxy_address) = sock.accept()
                message = proxy_socket.recv(1024).decode()

                if message=="start server":
                    if not MANUAL_START:
                        if thread.is_alive():
                            self.kill_thread=True
                            thread.join()
                    break

                if message=="shutdown" and not MANUAL_START:
                    os.system('shutdown -s')
                    exit()

        self.server_start()

        
    def get_player_count(self):

        self.proc.stdin.write("/list\n")
        line = self.proc.stdout.readline().strip()
        print(line)
        player_count = line[line.index("of a max")-2] # very rudementairy should change it to be more rigorous

        return player_count



# if __name__ == "__main__":
#     server = mc_server()
#     server.idle_loop(t_sec=30)

if testing:
    server = mc_server(directory, command)
    server.server_start()

else:
    with closing(socket.socket()) as sock:
        sock.settimeout(10)
        result = sock.connect_ex((( "and this one too", 42070)))

        if result==0:
            sock.send("wake up?".encode())

            response = sock.recv(1024).decode()

            print(response)

            if response=="yes":

                MANUAL_START=False
                server = mc_server()
                server.server_start()

        else:
            print("Not starting server, but idling")

            # if pc is manually started to not shutdown or leave the idle loop
            MANUAL_START=True
            server = mc_server()
            server.idle_loop(t_sec=0)
