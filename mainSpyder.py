import string, json
import conf
import datetime, time
import datetime, time
from scraper import Scraper


def main():

#  while datetime.datetime.now().time() < datetime.time(2, 30):
#    print "Sleeping for 300 secs"
#    time.sleep(300)
  scp = Scraper()
  print( "== Starting Script ==")
  startTime = datetime.datetime.now()
  
  scp.setup_session([conf.baseUrl, conf.rollSearchUrl])
  
  conf.searchParams['distNo'] = 8
  conf.searchParams['lacNo'] = 75

  # Cycle through the starting letters 
  for startLetter in ['k', 'l', 'm']:
    tries = 3
    while tries > 0:
      try:
        outFn = "voters_"+str(startLetter)+"_try_"+str(tries)+".txt"
        scp.get_write_records(conf.searchUrl, 10, startLetter, outFn, conf.searchParams)
      except:
        print("Retry #", tries)
        tries -= 1
        sleep(30)
        continue
      else:
        break
        

  
  endtime = datetime.datetime.now()
  
  print("Script running time : %f seconds" % (endtime - starttime).total_seconds())
  
  
if __name__ == "__main__":
  # execute only if run as a script
  main()

