import os
import time
os.system('start cmd /K "python servidor.py"')
time.sleep(1)
for i in range(1):
    time.sleep(1)
    os.system('start cmd /K "python cliente.py"')
