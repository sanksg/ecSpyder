import conf
import pickle
import json
import csv
import multiprocessing as mp

from myparser import myParser

def load_data(fileType, filename):
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


def main():
  data = load_data('pickle', 'voterRecords.pcl')

  detailsFile = open("voterDetails5.txt", 'a')

  csvFile = open("parsedCsv5.csv", 'w', encoding='utf-8')
  csvWriter = csv.writer(csvFile)

  prs = myParser()
  
  pool = mp.Pool(10)
  startRec = 47433
  dataSlice = data[startRec:]
  
  results = pool.imap( prs.get_and_parse, dataSlice, 100)
  pool.close()
  
  for i in range(len(dataSlice)):
    
    (parsedDetails, csvRow) = next(results)
    json.dump(parsedDetails, detailsFile)
    try:
      csvWriter.writerow(csvRow)
    except:
      print("Error while writing to CSV file. Skipping...")
      
    print("Wrote record #", i+startRec, " - ", csvRow)
#      
#      i+=1
#      print("Record #%d" % i)

if __name__ == "__main__":
  main()