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
    
  
  def try_and_get_response(self, maxTries, sleepTime, url, params):
    ''' This function is wrapper for the get_json_response function. It handles any exception, and tries to call get_json_response again, up to maxTries number of times.'''
    curTry = 1
    while curTry <= maxTries:
      print("\tTry #%d" % curTry)
      try:
        jsonResp = self.get_json_response(url, params)

      except:
        print ("\tException occured!! Sleeping for 30 secs then trying again...")
        curTry += 1
        if curTry > 3:
          print("\tCould not get response even after 3 tries!")
          raise
        time.sleep(sleepTime)
        continue
        
      else:
        break
      
    return jsonResp
      
    
  def get_json_response(self, url, params):
    ''' This function call the get_response function and tries to convert the response content into JSON'''
    if self.s == None:
      raise Exception('The session has not been setup yet! Please call setup_session for this object')
    
    # Try to get a response
    try:
      resp = self.get_response(url, params)
    except:
      print("Exception in Scraper.get_response() call")
      raise
      
    # Try to convert the response to JSON
    try:
      respJson = resp.json()
    except ValueError:
      print ("Exception while converting the GET request's response to JSON! Doesn't look like it's JSON.")
      print ("\tResponse Text: ", resp.text)
      raise
    
    return respJson
    
    
  def get_response(self, url, params):
    ''' This function takes in a url and a set of parameters and uses the previously set up session to send a GET request with the parameters as params and the headers in self.searchHeaders'''
    try:
      resp = self.s.get(url, headers=self.searchHeaders, params=params)
      #print("Request Headers: ", resp.request.headers)
      #print("Response Headers: ", resp.headers)
    except:
      print("Exception while making the GET through the session!")
      print("\tURL: %s \n\tHeaders: %s \n\tParameters: %s" % (url, self.searchHeaders, params))
      raise
    
  
  def get_and_write_records(self, searchUrl, sleepTime, outFileName, searchParams):
    '''This function queries the searchUrl with the searchParams. It figures out the total number of records for the query and then gets all of them. It sleeps for sleepTime seconds between requests.'''
    # Open a text file for writing the json response
    with open(outFileName, 'a') as outfile:

      #Init the search parameters
      searchParams['iDisplayLength'] = 0
      searchParams['iDisplayStart'] = 0

      # Initial request for getting the total number of records
      respJson = self.get_json_response(searchUrl, searchParams)
      totRecs = respJson['iTotalRecords']
      print ("Total Records: %d" % totRecs)

      i = 0
      reqAmt = 100

      # Get all the records for a particular letter
      while i < totRecs:      
        if i + reqAmt > totRecs:
          reqAmt = totRecs - i

        searchParams['iDisplayStart'] = i
        searchParams['iDisplayLength'] = reqAmt

        print("Requesting records %d - %d" % (i, i+reqAmt))
        
        jsonResp = self.try_and_get_response(3, 10, searchUrl, searchParams)

        json.dump(jsonResp, outfile)
        outfile.write('\n')

        i += reqAmt

        time.sleep(sleepTime)
        
        
        
        
        
        
   