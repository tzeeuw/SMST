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

string = "balasdfa" + "\n"
max_lines = 256
lines = [""]*256
lines[0] = string

lines[3] = "awdfasdf" + "\n"

print("".join(lines))

