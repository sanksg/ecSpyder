from urllib.parse import urljoin

baseUrl = 'http://www.ceo.kerala.gov.in'
rollsearchUrl = urljoin(baseUrl, 'rollsearch.html')
searchUrl = urljoin(baseUrl, 'electoralroll/edetailListAjax.html')
detailsUrl = urljoin(baseUrl,'searchDetails.html')

searchParams = {
  "distNo": 0,
  "lacNo":0,
  "electorName": "",
  "houseName": "",
  "epicNo": "",
  "relationName":"",
  "iDisplayLength":0,
  "iDisplayStart":0,
}

detailsParams = {
  "paramValue": "0751211554"
}

sessionHeaders = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'en-US,en;q=0.5',
  'Connection': 'keep-alive',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
}

searchHeaders = {
  "Accept": "application/json, text/javascript, */*",
  "Accept-Encoding": "gzip, deflate",
  "Accept-Language": "en-US,en;q=0.5",
  "Connection": "keep-alive",
  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
}

outfile = 'keralaVoters.txt'