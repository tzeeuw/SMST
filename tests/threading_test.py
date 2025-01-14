import threading
import time


class socket():
    def __init__(self):
        pass

    def readline(self):
        return "test"

class moc_server():
    def __init__(self):
        self.sock = socket()

    def server(self):
        count = 0
        thread = threading.Thread(target=self.server_countdown)
        while True:
            count += 1
            time.sleep(5)
            line = self.sock.readline()
            print(line)

            if count > 2 and not thread.is_alive():
                thread.start()

            if "joined" in line and thread.is_alive():
                self.kill_thread = True
                thread.join()
                thread = threading.Thread(target=self.server_countdown)
    
    def server_countdown(self):
        self.kill_thread = False

        for i in range(10):
            time.sleep(1)
            if self.kill_thread:
                break

        print("exiting server")


moc_server().server()
