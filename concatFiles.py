import glob
import os
for f in glob.glob('*.txt'):
  os.system("cat "+f+" >> finalVoterList.txt")  
  