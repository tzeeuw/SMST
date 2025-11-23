import time
import re
import datetime
import math
import socket
from contextlib import closing
import threading
import os
from smst.server.mc_server import mc_server
import collections
import json

with open('properties.json', 'r') as file:
    properties = json.load(file)

IP = properties["local_server_ip"]
PORT = int(properties["com_port"])
BOT_IP = properties["local_bot_ip"]
testing = False
directory = properties["cwd"]
command = properties["cmd"]
TOKEN = properties["token"]



#TODO: remodel entire class as it is too user input dependent
class mc_handling():
    """Handles the minecraft server using the mc_server class to interact with the server
    """    

    def __init__(self, directory, command):
        """Handles the minecraft server using the mc_server class to interact with the server
        Args:
            cmd (str, list): command to execute (for example a batch file)
            working_dir (str, dir): working directory to execute command in. This should be equal to the absolute path
            of the parent folder of the command
        """        
        self._server_is_alive = False
        self.server = mc_server(cmd=command, working_dir=directory)
        self.MANUAL_STOP = False

        max_lines = 256
        self.lines = collections.deque([""]*max_lines)


    def start_server(self):
        """Starts the server.
        """        
        self.server.start()
        self.server_thread = threading.Thread(target=self.server_loop)
        self.server_thread.start()


    def stop_server(self, t_idle=300):
        """Stops the server and puts it into idling mode.
        """

        self.idling_time = t_idle
        print("server is stopping")
        self.shutdown_server = True
        self.server.input("say Server is shutting down")

        self.server.stop()
        lines = self.server.readlines()

        for line in lines:
            print(line.strip())




    def input_handling(self, user_input):
        """Main body of input handling. Allows for custom commands.

        Args:
            user_input (str): input to be send to the server
        """        

        match user_input:

                case x if x.startswith("restart"):
                    numbers = re.findall(r'\d+', user_input)

                    # check if list is empty, if not give integer to restart function
                    if numbers:
                        self.restart(t=int(numbers[0]))

                    else:
                        self.restart()

                case "stop":
                    self.MANUAL_STOP = True
                    self.stop_server(t_idle=1)


                case "force stop":
                    self.MANUAL_STOP = True
                    self.server.force_stop()


                case x if x.startswith("overwrite"):
                    self.overwrite_eepy_time = True
                    numbers = re.findall(r'\d+', user_input)

                    if numbers:
                        self.overwrite_delta = int(numbers[0])
                    
                    else:
                        self.overwrite_delta = 30
                    
                case _:
                    self.server.input(user_input)
   


    def input_thread(self):
        """Thread to read input from the user into the command prompt and output it to the server.
        Also is able to handle custom commands like "restart". Uses a try/except block to avoid crashing of python
        while server keeps running.
        """        
        while not self.kill_input_thread:
            user_input = input("")

            # check if user input is not empty
            if user_input:

                try:
                    self.input_handling(user_input=user_input)

                except Exception as e:
                    print(f"Error occurred: {e}")
            
        return
    

    def remote_socket(self, conn: socket.socket):

        # use token verification because it is cool
        conn.sendall(b"Token: ")
        recv_token = conn.recv(1024).decode().strip()

        if recv_token != TOKEN:
            conn.sendall(b"Auth failed\n")
            conn.close()
            return
        
        conn.sendall(b"your*, help for all commands.\n")

        # so that lines are also parsed to the connected shell
        self.shell_connect = True
        self.conn = conn

        try:
            while True:
                conn.sendall(b"> ")
                line = conn.recv(1024)

                # test if the line is not empty
                if not line:
                    continue

                # get the command
                command = line.decode().strip().lower()


                match command:
                    case "exit":
                        conn.sendall(b"Nah fuck you\n")
                        break

                    # sends the history of lines from the terminal
                    case x if x.startswith("history"):
                        nlines = int(re.findall(r'\d+', command)[0])

                        if nlines and nlines < 256:
                            # maybe could be cleaner idk
                            for line in list(self.lines)[-nlines:]:
                                conn.sendall(f"{line}\n".encode())

                        elif nlines and nlines >= 256:
                            conn.sendall(f"{nlines} is greater than buffer, showing 256 lines.\n".encode())
                            for line in self.lines:
                                conn.sendall(f"{line}\n".encode())
                        
                        else:
                            conn.sendall(f"No history lenght is given, showing last 10 lines.\n".encode())
                        
                    case _:
                        self.input_handling(command)
                        

        # close the connection when python script is closed on other end
        finally:
            conn.close()
            self.shell_connect = False

    def remote_input(self):
        
        # this creates a socket once and continiously reaccepts connections to this socket and creates a new thread when a new connection is made
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((IP, PORT-1))
        s.listen(5)
        print(f"listening on {IP}:{PORT-1}")
        while not self.kill_remote_input_thread:
            conn, _ = s.accept()
            threading.Thread(target=self.remote_socket, kwargs={'conn': conn}, daemon=True).start()


    def time_check(self):
        """Checks and automatically stops the server after a set time. Can be overwritten with the custom overwrite command in which
        minutes can be added. Usage of overwrite command is "overwrite {n_minutes}"
        """        
        self.overwrite_delta=0
        delta = 0
        shutdown_said = False

        while not self.kill_time_thread:
            time.sleep(10)

            # convert overwrite in minutes into hours and minutes
            if math.floor((delta + 50)/ 60) <= datetime.datetime.now().hour < 10 and datetime.datetime.now().minute >= (delta + 50) % 60 and not shutdown_said:
                self.server.input("say Server shutting down in 10 minutes. Reason: Eepy time")
                shutdown_said = True

            if self.overwrite_delta:
                self.server.input(f"say Server shutdown time overwritten with {self.overwrite_delta} minutes")
                delta += self.overwrite_delta

                self.overwrite_delta = 0
                shutdown_said = False

            if math.floor(delta / 60 + 1) <= datetime.datetime.now().hour < 10 and datetime.datetime.now().minute >= (delta) % 60:
                self.stop_server(t_idle=1)
                


    def restart(self, t=0):
        """Restarts server with specified amount of seconds

        Args:
            t (int, optional): amount of seconds until restart. Defaults to 0.
        """
        self.server.input(f"say Restarting in {t} seconds")    
        self.server.restart(t=t)


    def countdown(self, idle=None, server=None, t=300):
        """Countdown function which handels the timings on when server or idle loop has to stop.
        Because idling and server are treated differently, it must be specified which mode is used

        Args:
            idle (boolean, optional): Idle mode. Defaults to None.
            server (boolean, optional): Server mode. Defaults to None.
            t (int, optional): Amount of time to countdown from. Defaults to 300.
        """        
        self.kill_countdown_thread = False

        idle = idle is not None
        server = server is not None

        assert idle + server == 1, "Please choose exactly one of idle or server"

        for t_sec in range(t):
            time.sleep(1)

            if t_sec % 10 == 0:
                print(f'{t_sec} seconds have passed')

            if self.kill_countdown_thread:
                return

        if server:
            self.stop_server(t_idle=300)
            return
            

        # connect with port that idle loop is listening to and send shutdown message
        if idle:
            with closing(socket.socket()) as sock:
                sock.connect((IP, PORT))
                sock.send("shutdown".encode())



    def server_loop(self, t=600):
        """Main loop which handles server output and user input. Also automatically shutsdown the server when no players are online.
        """        
        countdown_thread = threading.Thread(target=self.countdown, kwargs={'server': True, 't': t})

        time_thread = threading.Thread(target=self.time_check)
        self.kill_time_thread = False
        time_thread.start()
        
        input_thread = threading.Thread(target=self.input_thread)
        self.kill_input_thread = False
        input_thread.start()

        # used to send output back to the ssh shell
        self.shell_connect = False
        remote_input = threading.Thread(target=self.remote_input)
        self.kill_remote_input_thread = False
        remote_input.start()

        self.shutdown_server = False

        self.MANUAL_STOP = False
        

        while not self.shutdown_server:
            line = self.server.readline()
           

            if line:
                print(line)
                self.lines.append(line)
                self.lines.popleft()

                # also send to shell if it is connected
                if self.shell_connect:
                    self.conn.sendall(f"{line}\n".encode())
                    self.conn.sendall(b"> ")


            # see if players left and there are still players online
            if "left" in line or "pausing" in line:

                # make sure that thread is not already online
                if int(self.get_player_count()) == 0 and not countdown_thread.is_alive():
                    countdown_thread.start()

            # if player joins, kill the countdown thread and create new one
            if "joined" in line and countdown_thread.is_alive():
                self.kill_countdown_thread = True
                countdown_thread.join()

                print("thread broken")

                countdown_thread = threading.Thread(target=self.countdown, kwargs={'server': True, 't': t})

        self.kill_time_thread=True
        self.kill_input_thread = True

        # bit of a cheesy and bad fix should fix this fix?
        if self.idling_time == -1:
            return

        if MANUAL_START:
            self.idle_loop(t=0)

        else:
            self.idle_loop(t=self.idling_time)


    def idle_loop(self, t=0):
        """Idle loop which will idle while server is not running but computer is still on.

        Args:
            t (int, optional): Amount of seconds to idle for, if 0 the idle time is infinite. Defaults to 0.
        """        

        # start countdown thread if t is provided
        if t:
            thread = threading.Thread(target=self.countdown, kwargs={'idle': True, 't': t})
            thread.start()

        elif t == -1:
            return

        # listen on socket connected with proxy to see if new connection request is asked and start the server if requested
        with closing(socket.socket()) as sock:
            sock.bind((IP, PORT))

            while True:
                sock.listen()

                (proxy_socket, proxy_address) = sock.accept()
                message = proxy_socket.recv(1024).decode()

                

                if testing or self.MANUAL_STOP:
                    exit()

                if message=="start server":
                    if not MANUAL_START:
                        if thread.is_alive():
                            self.kill_countdown_thread=True
                            thread.join()
                    break                           #break so that server is not started from within while True loop

                # if countdown is finished it sends shutdown message
                if message=="shutdown" and not MANUAL_START:
                    os.system('shutdown -s')
                    exit()

        # start server
        self.start_server()

        
    def get_player_count(self):
        """Poorly made command to get the player count of the server at the time of calling the method.

        Returns:
            int: amount of players on the server.
        """        
        self.server.flush()
        self.server.input("list")
        line = self.server.readline()
        print(line)
        try:
            player_count = line[line.index("of a max")-2] # very rudementairy should change it to be more rigorous
        
        except:
            player_count = 0
            print("Could not find amount of players due to index out of range error")

        return int(player_count)



if __name__ == "__main__":
    if testing:
        MANUAL_START = False
        server = mc_handling(directory, command)
        server.start_server()



    else:
        with closing(socket.socket()) as sock:
            sock.settimeout(10)
            result = sock.connect_ex(((BOT_IP, PORT)))

            if result==0:
                sock.send("wake up?".encode())

                response = sock.recv(1024).decode()

                print(response)

                if response=="yes":

                    MANUAL_START=False
                    server = mc_handling(directory, command)
                    server.start_server()

            else:
                print("Not starting server, but idling")

                # if pc is manually started to not shutdown or leave the idle loop
                MANUAL_START=True
                server = mc_handling(directory, command)
                server.idle_loop(t=0)
