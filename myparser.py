import time
import re
import conf
import random
import json
from datetime import datetime
from bs4 import BeautifulSoup as BS
from scraper import Scraper



class myParser:
  def __init__(self):
    pass
    
  def init_web(self):
    self.detailsParams = conf.detailsParams
    self.detailsUrl =  conf.detailsUrl
    self.scp = Scraper(conf.sessionHeaders, conf.searchHeaders, [conf.baseUrl, conf.rollSearchUrl])
    self.scp.setup_session()

  
  def request_and_parse(self, rec):
#    startTime = datetime.now()
    
#    print(str(rec[0]).encode('utf-8'))
    csvRow = rec[0:5]
    csvRow.append(rec[7])

    urlTag = re.search("paramValue=(\w+)\"", rec[6])
    if not urlTag:
      raise Exception('Cannot find a details url in the record: \n'+str(rec))

#    print ("After paramvalue RE search: ", (datetime.now()-startTime).total_seconds())
    self.detailsParams['paramValue'] = urlTag.group(1)

    #      print(detailsParams)

    resp = self.scp.get_response(self.detailsUrl, self.detailsParams, 3)
    
#    print ("After GET: ", (datetime.now()-startTime).total_seconds())
    
    
    checkInvalid = re.search("Invalid access to the page", resp.text)
    if checkInvalid:
      print("Looks like the record for %s %s is not in the database anymore. Continuing on..." % (rec[0],rec[1]))
      return ("", "")
      
    #      print(resp.request.url)    
    soup = BS(resp.content, 'html.parser')
#    print(soup.prettify('latin-1'))

    parsedDetails = []

    tables = soup.find_all('table')

    # Go through all the info in the details page and extract 
    for table in tables:
      rows = table.find_all('tr')

      for row in rows:
        cols = row.find_all('td')
        txtCols = []
    #          txtCols = [ele.text.strip() for ele in cols]
    #          print([ele for ele in cols if ele.has_attr('a')])

        for ele in cols:
          txtCols.append(ele.text.strip())
          if ele.a:
            txtCols.append(ele.a.get('href').split("Value=")[1].strip())

        parsedRow = [ele for ele in txtCols if ele]
        parsedDetails.append(parsedRow)

#    # Now we have gone through all the tables on the page and parseDetails is complete
#    try:
#      csvRow.append(parsedDetails[2][1])
#    except:
#      print("Exception while parsing details for record: \n"+str(rec))
#      print("P`arsed details: %s" % str(parsedDetails))
#      print("Continuing with blank values")
#      csvRow.append("")
#    else:
#      if re.search("Husband", parsedDetails[3][0]):
#        csvRow.append('F')
#      else:
#        csvRow.append('M')
    
#    print ("After all processing: ", (datetime.now()-startTime).total_seconds())
    
    time.sleep(random.uniform(0.5,1))
    return parsedDetails

  
