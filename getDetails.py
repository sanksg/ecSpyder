import conf
import pickle
import json
import csv
import re
import multiprocessing as mp
from datetime import datetime
from myparser import MyParser
from fileUtils import FileUtils


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
  data = load_records('pickle', 'remainingDetails.pcl')

  detailsFile = open("remainingDetails.txt", 'a')

#  csvFile = open("parsedCsv9.csv", 'w', encoding='utf-8', newline='')
#  csvWriter = csv.writer(csvFile, delimiter=',')

  prs = MyParser()
  prs.init_web()
  
  pool = mp.Pool(10)
  startRec = 0
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

  
def parse_fetch_details_write_csv():
  fts = FileUtils()
#  fts.concat_files("backup/voterDetails*.txt", 'concatVoterDetails.txt')
#  details = fts.load_json('concatVoterDetails.txt')
#  fts.save_pickle(details, 'pickleDetails.pcl')
  
  records = load_records('pickle', 'voterRecords.pcl')
  details = fts.load_json('concatVoterDetails.txt')
  
  csvFile = open("parsedCsvAll.csv", 'w', encoding='utf-8', newline='\n')
  csvWriter = csv.writer(csvFile, delimiter=',') 
  csvWriter.writerow(['First Name', 'Middle Name', 'Relation Name', 'House Name', 'Serial No', 'LAC No', 'PS No', 'Status', 'Age', 'Gender'])
  csvRow = []
#  
#  prs = MyParser()
#  prs.init_web()
  
  rem_details = []
  i = 0
  for rec in records:
    # Name, RelationName, HouseName, SerialNo, LACNo, PSNo
#    print(rec)
    if ' ' in rec[0]:
      splt = rec[0].split(' ')
      firstN= splt[0]
      midN = ' '.join(splt[1:])
    else:
      firstN = rec[0]
      midN = ''
      
    csvRow = []
    csvRow.extend([firstN,midN])  
    csvRow.extend(rec[1:6])
    # Status
    csvRow.append(rec[7])

    elid = re.search('>([a-zA-Z0-9\/]+)<', rec[6])
    if elid:
      elid = elid.group(1)
      if elid in details:
        parsedDetails = details[elid]
      else:
#        print("Elector ID %s not found in fetched details" % elid)
#        print("Fetching from site...")
#        parsedDetails = prs.request_and_parse(rec)
        #Make sure that we got something back, otherwise skip this record
#        if parsedDetails == None:
#          continue
#        
        #Append a copy of the newly fetched details to a dict for saving to file later
        rem_details.append(rec)
        continue
#      print(parsedDetails)
      #Now parse the info for writing to csv
      #Age
      csvRow.append(parsedDetails[2][1])
      #Gender
      if re.search("Husband", parsedDetails[3][0]):
        csvRow.append('F')
      else:
        csvRow.append('M')
    
    # Write row to CSV
    csvWriter.writerow(csvRow)
#    i+=1
#    if i > 10:
#      break
  # END LOOP
  
  # If any new details were fetched, update our own coy of details
#  if new_details != {}:
#    details.update(new_details)
#    fts.save_pickle(details, 'pickleDetails.pcl')
#  
#  fts.save_pickle(rem_details, 'remainingDetails.pcl')  
  
  
def main():
  parse_fetch_details_write_csv()
#  get_details_from_site()
  
if __name__ == "__main__":
  main()
