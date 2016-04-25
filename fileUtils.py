import glob
import os


class FileUtils:
  def concat_files(self, filePattern, outFn):
    for f in glob.glob(filePattern):
      os.system("cat " + f + " >> " + str(outFn) )
      
  def load_json(self, filename):
    data = []
    with open(filename, 'r') as df:
      for line in df:
        record = json.loads(line)
        data.append(record)
        break
    print(data)
    
    return data
  
  