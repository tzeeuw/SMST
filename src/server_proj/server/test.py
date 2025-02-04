# import re

# user_input = input("")

# match user_input:

#     case "test":
#         print("test2")
#     case _:
#         print("test123")

# numbers = re.findall(r'\d+', user_input)
# result = list(map(int,numbers))

# if result:
#     print('test')
# print(result)

import subprocess

cmd = ['python', 'proc.py']
working_dir = 'src\\server_proj\\server'

subproc = subprocess.Popen(cmd, cwd=working_dir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, bufsize=1)

while True:
    line = subproc.stdout.readline()
    print(line)
