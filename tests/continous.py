import time
import sys

# test code run python with -u to run it unbuffered so flush is not needed.
print('left')
while True:
    time.sleep(1)
    print("test")
    sys.stdout.flush()