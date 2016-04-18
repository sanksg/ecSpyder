import string, json
import conf
import datetime, time

from requests import Request, Session
from urllib.parse import urljoin


def get_json_response(session, url, headers, params):
  resp = session.get(url, headers=headers, params=params)
  #print("Request Headers: ", resp.request.headers)
  #print("Response Headers: ", resp.headers)

  try:
    respJson = resp.json()
  except ValueError:
    print ("Was expecting JSON response, but got something non-JSON!")
    print ("Response: ", resp.text)

  return respJson
    

def setup_session():
  s = Session()
  s.headers.update(conf.sessionHeaders)

  s.get(conf.baseUrl)
  #print("Session Headers: ", s.headers)
  s.get(conf.rollsearchUrl)
  #print("Session Headers: ", s.headers)
  #req = Request('GET', searchUrl, headers=searchHeaders, params=searchParams)
  #prepped = s.prepare_request(req)

  return s


def main():

#  while datetime.datetime.now().time() < datetime.time(2, 30):
#    print "Sleeping for 300 secs"
#    time.sleep(300)
  
  print( "== Starting Script ==")
  startTime = datetime.datetime.now()
  
  conf.searchParams['distNo'] = 8
  conf.searchParams['lacNo'] = 75

  
  # Setup the session
  session = setup_session()

  # Open a text file for writing the json response
  with open("test.txt", 'a') as outfile:
    
    # Cycle through the starting letters 
    for startLetter in string.ascii_lowercase:
      
      #Init the search parameters
      conf.searchParams['iDisplayLength'] = 0
      conf.searchParams['iDisplayStart'] = 0
      conf.searchParams['electorName'] = startLetter

      # Initial request for getting the total number of records
      respJson = get_json_response(session, conf.searchUrl, conf.searchHeaders, conf.searchParams)
      totRecs = respJson['iTotalRecords']
      print ("Total Records for %s : %d" % (startLetter, totRecs))
      
      i = 0
      reqAmt = 10
      
      # Get all the records for a particular letter
      while i < totRecs:      
        if i + reqAmt > totRecs:
          reqAmt = totRecs - i

        conf.searchParams['iDisplayStart'] = i
        conf.searchParams['iDisplayLength'] = reqAmt
        
        print("Requesting records %d - %d" % (i, i+reqAmt))
        jsonResp = get_json_response(session, conf.searchUrl, conf.searchHeaders, conf.searchParams)
        json.dump(jsonResp, outfile)
        outfile.write('\n')

        i += reqAmt
        
        time.sleep(10)

  endtime = datetime.datetime.now()
  
  print("Script running time : %f seconds" % (endtime - starttime).total_seconds())
  
  
if __name__ == "__main__":
  # execute only if run as a script
  main()
