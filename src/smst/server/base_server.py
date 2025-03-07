from smst.server.mc_server import mc_server
import threading
import collections
import re

class base_server():
    def __init__(self, cmd, cwd):
        self.cmd = cmd
        self.cwd = cwd
        self.server = mc_server(self.cmd, self.cwd)
        max_lines = 256
        self.lines = collections.deque(maxlen=max_lines)


    def start_server(self):
        self.server.start()
        self.line_thread=threading.Thread(target=self.add_lines)
        self.line_thread.start()

    def stop_server(self):
        self.server.stop()

    def restart(self, t=0):
        self.say(f"Restarting in {t} seconds")    
        self.server.restart(t=t)


    def add_lines(self):
        for line in iter(self.server.raw_readline, ''):
            self.lines.append(line.strip())
            print(line.strip())

    def get_lines(self):
        return self.lines
    

    def input(self, user_input):
        self.server.input(user_input)

    def say(self, user_input):
        self.server.input(f"say {user_input}")

    def input_handling(self, user_input):
        match user_input:

                case x if x.startswith("restart"):
                    numbers = re.findall(r'\d+', user_input)

                    if numbers:
                        self.restart(t=int(numbers[0]))

                    else:
                        self.restart()

                case "stop":
                    self.stop_server()

                case "force stop":
                    self.server.force_stop()
                    
                case _:
                    self.server.input(user_input)
