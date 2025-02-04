import subprocess
import time
import datetime
import socket
from contextlib import closing
import threading
import os
from server_proj.server.mc_server import mc_server

testing = True
directory = "D:\\Minecraft\\fabric_test"
command = "start.bat"




class mc_handling():
    def __init__(self, directory, command):
        self._server_is_alive = False
        self.server = mc_server(cmd=command, working_dir=directory)

    def server_start(self):
        self.server.start()
        self.server_loop()

    def server_stop(self):

        self.server.stop()

        if MANUAL_START:
            self.idle_loop(t_sec=0)

        else:
            self.idle_loop(t_sec=5*60)


    def input_thread(self):
        while True:
            user_input = input("")

            if user_input == "restart":
                self.restart()

            elif user_input != "":
                self.server.input(user_input)

                if user_input == "stop":
                    self.shutdown_server = True
                    break

            if self.input_kill:
                break
        return


    def restart(self, t=0):
        self.server.restart()


    def server_loop(self):
        thread = threading.Thread(target=self.server_countdown, args=(10*60,))

        self.input_kill = False
        input_thread = threading.Thread(target=self.input_thread)

        self.shutdown_server = False

        input_thread.start()

        while True:
            line = self.server.readline()
            print(line)


            if "left" in line or "pausing" in line:
                if int(self.get_player_count()) == 0 and not thread.is_alive():
                    thread.start()

            if "joined" in line and thread.is_alive():
                self.kill_thread = True
                thread.join()
                print("thread broken")

                thread = threading.Thread(target=self.server_countdown, args=(10*60,))

            if self.shutdown_server:
                break
        
        self.input_kill = True
        self.server_stop()



    def server_countdown(self, t_sec):
        self.kill_thread = False

        for t in range(t_sec):
            time.sleep(1)
            print(t)
            if self.kill_thread:
                return

        print("server is stopping")
        self.server.input("say Server is shutting down")
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
    MANUAL_START = True
    server = mc_handling(directory, command)
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
                server = mc_handling(directory, command)
                server.server_start()

        else:
            print("Not starting server, but idling")

            # if pc is manually started to not shutdown or leave the idle loop
            MANUAL_START=True
            server = mc_handling(directory, command)
            server.idle_loop(t_sec=0)
