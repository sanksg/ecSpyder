import glob
import os
import json
import pickle
import csv


class FileUtils:
  def __init__(self):
    pass
  
  
  def load_csv(self, fn):
    lines = csv.reader(open(fn, 'r', encoding='utf-8'))
    dataset = list(lines)
    return dataset
  
  def concat_files(self, filePattern, outFn):
    for f in glob.glob(filePattern):
      print(f)
      concat_cmd = "cat " + f + " >> " + str(outFn) 
      print("Concat comman: ", concat_cmd)
      os.system(concat_cmd)
      
  def load_json(self, filename):
    data = {}
    i = 0
    with open(filename, 'r') as df:
      for line in df:
        try:
          record = json.loads(line)
        except BaseException as e:
          print("Line Number: ", i+1)
          print(line)
          print(e)
          raise
        data[record[0][1]] = record

        i+=1
    
#    print(data)
    return data

  def save_pickle(self, data, outFn):
    with open(outFn, 'wb') as pickleFile:
      pickle.dump(data, pickleFile)
    
  
  def load_pickle(self, fn):
    with open(fn, 'rb') as pf:
      data = pickle.load(pf)
    
    return data