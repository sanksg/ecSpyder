import conf
import pickle
import json
import csv
import multiprocessing as mp
from scraper import Scraper
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

  scp = Scraper(conf.sessionHeaders, conf.searchHeaders)
  scp.setup_session([conf.baseUrl, conf.rollSearchUrl])

  detailsFile = open("test.txt", 'a')

  csvFile = open("test.csv", 'w', encoding='utf-8')
  csvWriter = csv.writer(csvFile)

  prs = myParser(scp, conf.detailsUrl, conf.detailsParams)
  
  pool = mp.Pool(10)
  results = pool.imap( prs.get_and_parse, data[12342:12352])
  pool.close()
  
  for i in range(len(data[12342:12352])):
    print("Processing Results")
    (parsedDetails, csvRow) = results.next()
    json.dump(parsedDetails, detailsFile)
    csvWriter.writerow(csvRow)

#      
#      i+=1
#      print("Record #%d" % i)

if __name__ == "__main__":
  main()