import re
from bs4 import BeautifulSoup as BS

class myParser:
  def __init__(self, scp, url, params):
    self.scp = scp
    self.detailsParams = params
    self.detailsUrl = url
  
  def get_and_parse(self, rec):

    print(str(rec[0]).encode('utf-8'))
    csvRow = rec[0:5]
    csvRow.append(rec[7])

    urlTag = re.search("paramValue=(\w+)\"", rec[6])
    if not urlTag:
      raise Exception('Cannot find a details url in the record: \n'+str(rec))

    self.detailsParams['paramValue'] = urlTag.group(1)

    #      print(detailsParams)
    resp = self.scp.get_response(self.detailsUrl, self.detailsParams, 3)
    #      print(resp.request.url)    
    soup = BS(resp.content, 'html.parser')
    #      print(soup.prettify('latin-1'))

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

    # Now we have gone through all the tables on the page and parseDetails is complete
    try:
      csvRow.append(parsedDetails[2][1])
    except:
      print("Exception while parsing details for record: \n"+rec)
      print("Continuing with blank values")
      csvRow.append("")
      csvRow.append("")
    else:
      if re.search("Husband", parsedDetails[3][0]):
        csvRow.append('F')
      else:
        csvRow.append('M')

    return (parsedDetails, csvRow)
