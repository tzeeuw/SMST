import time
import re
import socket
from contextlib import closing
import threading
import os
from server_proj.server.mc_server import mc_server

testing = True
directory = "D:\\Minecraft\\fabric_test"
command = "start.bat"




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


    def start_server(self):
        """Starts the server.
        """        
        self.server.start()
        self.server_loop()


    def stop_server(self):
        """Stops the server and puts it into idling mode.
        """        

        lines = self.server.stop()

        for line in lines:
            print(line.strip())

        if MANUAL_START:
            self.idle_loop(t=0)

        else:
            self.idle_loop(t=300)



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
                    self.shutdown_server = True
                    self.server.input("say Shutting down the server")

                case "force stop":
                    self.server.force_stop()
                    
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
            print("server is stopping")
            self.server.input("say Server is shutting down")
            self.shutdown_server = True


        # connect with port that idle loop is listening to and send shutdown message
        if idle:
            with closing(socket.socket()) as sock:
                sock.connect(("192.168.178.17", 42070))
                sock.send("shutdown".encode())


    def server_loop(self):
        """Main loop which handles server output and user input. Also automatically shutsdown the server when no players are online.
        """        
        countdown_thread = threading.Thread(target=self.countdown, kwargs={'server': True, 't': 600})
        
        input_thread = threading.Thread(target=self.input_thread)
        self.kill_input_thread = False
        input_thread.start()

        self.shutdown_server = False


        while not self.shutdown_server:
            
            line = self.server.readline()

            if line:
                print(line)

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

                countdown_thread = threading.Thread(target=self.countdown, kwargs={'server': True, 't': 600})

        

        self.stop_server()



    def idle_loop(self, t=0):
        """Idle loop which will idle while server is not running but computer is still on.

        Args:
            t (int, optional): Amount of seconds to idle for, if 0 the idle time is infinite. Defaults to 0.
        """        

        # start countdown thread if t is provided
        if t:
            thread = threading.Thread(target=self.countdown, kwargs={'idle': True, 't': t})
            thread.start()


        # listen on socket connected with proxy to see if new connection request is asked and start the server if requested
        with closing(socket.socket()) as sock:
            sock.bind(("192.168.178.17", 42070))

            while True:
                sock.listen()

                (proxy_socket, proxy_address) = sock.accept()
                message = proxy_socket.recv(1024).decode()

                if message=="start server":
                    if not MANUAL_START:
                        if thread.is_alive():
                            self.kill_thread=True
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
        player_count = line[line.index("of a max")-2] # very rudementairy should change it to be more rigorous

        return int(player_count)




if testing:
    MANUAL_START = False
    server = mc_handling(directory, command)
    server.start_server()



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
                server.start_server()

        else:
            print("Not starting server, but idling")

            # if pc is manually started to not shutdown or leave the idle loop
            MANUAL_START=True
            server = mc_handling(directory, command)
            server.idle_loop(t_sec=0)
