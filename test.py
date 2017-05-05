import subprocess
import os
import sys
x = "hell"
#os.system('"/Users/kevingottfried/Documents/CS_228/final/final/helloworld"')
p = subprocess.Popen(["/Users/kevingottfried/Documents/CS_228/Deliverables/Deliverable_7/helloworld"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p.communicate(x)
p.wait()
#x = raw_input()
#sys.stdout.write(x)
