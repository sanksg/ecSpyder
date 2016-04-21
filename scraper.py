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
    

    
  def get_json_response(self, url, params, maxTries):
    ''' This function call the get_response function and tries to convert the response content into JSON'''
    if self.s == None:
      raise Exception('The session has not been setup yet! Please call setup_session for this object')


    curTry = 1
    while curTry <= maxTries:
      # Try to get a response
      try:
        resp = self.get_response(url, params, maxTries)
      except:
        print("\t**=> Exception in get_response() call")
        raise
      # Convert the response to JSOn
      try:
        respJson = resp.json()
      except:
        print ("\t**=> Exception occured while converting GET response to JSON!! Sleeping for 30 secs then trying again...")
        curTry += 1
        if curTry > 3:
          print("\tCould not convert response to JSON even after 3 tries!")
          print ("\tResponse Text: ", resp.text)
          raise
        time.sleep(30)
        continue
        
      else:
        break
      
    return respJson
    
    
  def get_response(self, url, params, maxTries):
    ''' This function takes in a url and a set of parameters and uses the previously set up session to send a GET request with the parameters as params and the headers in self.searchHeaders'''
    
    curTry = 1
    while curTry <= maxTries:
      try:
        resp = self.s.get(url, headers=self.searchHeaders, params=params)

      except:
        print("\t**=> Exception while making the GET request through the session!")
        print("\tURL: %s \n\tHeaders: %s \n\tParameters: %s" % (url, self.searchHeaders, params))
        print ("\t**=> Sleeping for 30 secs then trying again...\n")
        curTry += 1
        if curTry > 3:
          print("\tCould not get response even after %d tries!" % maxTries)
          raise
        time.sleep(30)
        print("\tGET Request Try #%d" % curTry)
        continue
        
      else:
        break
  
    
    return resp
    
  
  def get_and_write_records(self, searchUrl, sleepTime, searchParams, outFile):
    '''This function queries the searchUrl with the searchParams. It figures out the total number of records for the query and then gets all of them. It sleeps for sleepTime seconds between requests.'''

    #Init the search parameters
    searchParams['iDisplayLength'] = 0
    searchParams['iDisplayStart'] = 0

    # Initial request for getting the total number of records
    respJson = self.get_json_response(searchUrl, searchParams, 3)
    totRecs = respJson['iTotalRecords']
    print ("Total Records: %d" % totRecs)

    i = 0
    reqAmt = 1000

    # Get all the records for a particular letter
    while i < totRecs:      
      if i + reqAmt > totRecs:
        reqAmt = totRecs - i

      searchParams['iDisplayStart'] = i
      searchParams['iDisplayLength'] = reqAmt

      print("Requesting records %d - %d for letter %s" % (i, i+reqAmt, searchParams['electorName']))

      jsonResp = self.get_json_response(searchUrl, searchParams, 3)

      json.dump(jsonResp, outFile)
      outFile.write('\n')

      i += reqAmt

      time.sleep(sleepTime)






