import subprocess
import time


class mc_server():
    """Server object that handels communicates with the minecraft server
    """    

    def __init__(self, cmd, working_dir):
        """Server object that handels communicates with the minecraft server

        Args:
            cmd (str, list): command to execute (for example a batch file)
            working_dir (str, dir): working directory to execute command in. This should be equal to the absolute path
            of the parent folder of the command
        """        
        self.cmd = cmd
        self.cwd = working_dir

    
    def __create_subproc(self, cmd, working_dir):
        """Creates a subprocess. It should only be accessed by the class.

        Args:
            cmd (str, list): command to execute (for example a batch file)
            working_dir (str, dir): working directory to execute command in. This should be equal to the absolute path
            of the parent folder of the command
        """        

        self.subproc = subprocess.Popen(cmd, cwd=working_dir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, bufsize=1)

    

    def start(self, cmd=None, working_dir=None):
        """Starts the subprocess to run the server. Command and working directory can be changed to allow
        for multiple uses of the same class.

        Args:
            cmd (str, list, optional): command to execute (for example a batch file). Defaults to None
            working_dir (str, dir, optional): working directory to execute command in. This should be equal to the absolute path
            of the parent folder of the command. Defaults to None
        """        
        if cmd != None:
            self.cmd = cmd

        if working_dir != None:
            self.cwd = working_dir

        self.__create_subproc(cmd=self.cmd, working_dir=self.cwd)
    

    def stop(self):
        """Stops the server and returns the last lines

        Returns:
            str: last lines of the server
        """      
        self.input("stop")
        self.subproc.wait()


    def force_stop(self):
        """Force stops the server
        """        
        self.subproc.terminate()
        self.subproc.wait()
    

    def restart(self, t=0):
        """Restarts the server
        """
        time.sleep(t)      
        self.stop()
        self.start()


    def flush(self):
        """Flushes the data inside the output to make sure the program is up to date with lines.
        """        
        self.subproc.stdout.flush()


    def input(self, string):
        """Inputs commands into the running subprocess

        Args:
            string (str): command for the subprocess to execute
        """        
        self.subproc.stdin.write(f"{string}\n")


    def readline(self):
        """Reads a single line and strips it from its termination character.

        Returns:
            str: Single line of output from the subprocess
        """        
        return self.subproc.stdout.readline().strip()


    def readlines(self):
        """Reads all lines starting from the call of this method to the end of the subprocess.

        Returns:
            str: all lines of the subprocess
        """
        return self.subproc.stdout.readlines()

