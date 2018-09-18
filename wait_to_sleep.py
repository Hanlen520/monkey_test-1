import os
from time import sleep

sleep(120)
cmd  = "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
result = os.system(cmd)
print(result)