import string, json, time
from requests import Request, Session
from urllib.parse import urljoin

class Scraper:
  def __init__(self, sessionHeaders, searchHeaders):
    '''This function takes a
    '''
    self.sessionHeaders = sessionHeaders
    self.searchHeaders = searchHeaders
    self.s = None
    
  
  def setup_session(self, urlList):
    self.s = Session()
    self.s.headers.update(self.sessionHeaders)

    for url in urlList:
      self.s.get(url)
      #print("Session Headers: ", self.s.headers)
      
      
  def get_json_response(self, url, params):
    if self.s == None:
      raise Exception('The session has not been setup yet! Please call setup_session for this object')
      
    try:
      resp = self.s.get(url, headers=self.searchHeaders, params=params)
      #print("Request Headers: ", resp.request.headers)
      #print("Response Headers: ", resp.headers)
    except TypeError:
      return None
      
    try:
      respJson = resp.json()
    except ValueError:
      print ("Was expecting JSON response, but got something non-JSON!")
      print ("Response: ", resp.text)
      return None
    
    return respJson
    
    
    
    
  def get_write_records(self, searchUrl, sleepTime, startLetter, outFileName, searchParams):

    
    # Open a text file for writing the json response
    with open(outFileName, 'a') as outfile:

      #Init the search parameters
      searchParams['iDisplayLength'] = 0
      searchParams['iDisplayStart'] = 0
      searchParams['electorName'] = startLetter

      # Initial request for getting the total number of records
      respJson = self.get_json_response(searchUrl, searchParams)
      totRecs = respJson['iTotalRecords']
      print ("Total Records for %s : %d" % (startLetter, totRecs))

      i = 0
      reqAmt = 100

      # Get all the records for a particular letter
      while i < totRecs:      
        if i + reqAmt > totRecs:
          reqAmt = totRecs - i

        searchParams['iDisplayStart'] = i
        searchParams['iDisplayLength'] = reqAmt

        print("Requesting records %d - %d" % (i, i+reqAmt))
        jsonResp = self.get_json_response(searchUrl, searchParams)
        json.dump(jsonResp, outfile)
        outfile.write('\n')

        i += reqAmt

        time.sleep(sleepTime)
        
        
        
        
        
        
   