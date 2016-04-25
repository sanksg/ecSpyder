import conf
import pickle
import json
import csv
import multiprocessing as mp
from datetime import datetime
from myparser import myParser
from fileUtils import fileUtils

def load_records(fileType, filename):
  if fileType == 'pickle':
    with open(filename, 'rb') as data_file:
      data=pickle.load(data_file)
  else:
    data = []
    with open(filename) as data_file:    
        for line in data_file:
          jsonD = json.loads(line)
          for voter in jsonD['aaData']:
            data.append(voter)

  return data


def get_details_from_site():
  startTime = datetime.now()
  data = load_records('pickle', 'voterRecords.pcl')

  detailsFile = open("voterDetails14.txt", 'a')

#  csvFile = open("parsedCsv9.csv", 'w', encoding='utf-8', newline='')
#  csvWriter = csv.writer(csvFile, delimiter=',')

  prs = myParser()
  prs.init_web()
  
  pool = mp.Pool(10)
  startRec = 158728
  dataSlice = data[startRec:]
  
  results = pool.imap( prs.request_and_parse, dataSlice, 10)
  pool.close()
  
  for i in range(len(dataSlice)):
    
    parsedDetails = next(results)
    json.dump(parsedDetails, detailsFile)
      
    print("Wrote record #", i+startRec)
#      
#      i+=1
#      print("Record #%d" % i)
  print("Elapsed Time: ", (datetime.now() - startTime).total_seconds())

  
def parse_details_file():
  fts = FileUtils()
  fts.concat_files("backup/voterDetals*.txt", 'concatVoterDetails.txt')
  
  
  
def main():
  parse_details_file()
 
  
  
if __name__ == "__main__":
  main()
