from requests import Request, Session
from urllib.parse import urljoin

baseUrl = 'http://www.ceo.kerala.gov.in'
rollsearchUrl = urljoin(baseUrl, 'rollsearch.html')
searchUrl = urljoin(baseUrl, 'electoralroll/edetailListAjax.html')
detailsUrl = urljoin(baseUrl,'searchDetails.html')

searchParams = {
  "distNo": 8,
  "lacNo":75,
  "electorName": "a",
  "houseName": "",
  "epicNo": "",
  "relationName":"",
  "iDisplayLength":10,
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

s = Session()
s.headers.update(sessionHeaders)

s.get(baseUrl)
print("Session Headers: ", s.headers)
s.get('http://www.ceo.kerala.gov.in/rollsearch.html')
print("Session Headers: ", s.headers)
#req = Request('GET', searchUrl, headers=searchHeaders, params=searchParams)
#prepped = s.prepare_request(req)
#
#resp = s.send(prepped)
resp = s.get(searchUrl, headers=searchHeaders, params=searchParams)
print("Request Headers: ", resp.request.headers)
print("Response Headers: ", resp.headers)


print("Response:", resp.json())

#res1 = requests.get(deturl, headers=headers, params=detailsParams)
#print(res1)
