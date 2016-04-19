import conf
import datetime, time
from scraper import Scraper


def main():

#  while datetime.datetime.now().time() < datetime.time(2, 30):
#    print "Sleeping for 300 secs"
#    time.sleep(300)
  scp = Scraper(conf.sessionHeaders, conf.searchHeaders)
  print( "== Starting Script ==")
  startTime = datetime.datetime.now()
  
  scp.setup_session([conf.baseUrl, conf.rollSearchUrl])
  
  conf.searchParams['distNo'] = 8
  conf.searchParams['lacNo'] = 75

  # Cycle through the starting letters 
  for startLetter in ['m']:#, 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '$']:
    outFn = "voters_"+str(startLetter)+".txt"
    print("Records for letter " + startLetter)
    
    conf.searchParams['electorName'] = startLetter

    scp.get_and_write_records(conf.searchUrl, 10, outFn, conf.searchParams)
        
  endtime = datetime.datetime.now()
  
  print("Script running time : %f seconds" % (endtime - startTime).total_seconds())
  
  
if __name__ == "__main__":
  # execute only if run as a script
  main()

