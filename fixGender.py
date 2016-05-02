import csv
import random
import math
import pickle
from fileUtils import FileUtils


def splitDataset(dataList, splitRatio):
  trainSize = int(len(dataList) * splitRatio)
  trainSet = []
  copy = list(dataList)
  while len(trainSet) < trainSize:
    index = random.randrange(len(copy))
    trainSet.append(copy.pop(index))
  return [trainSet, copy]


def get_ngrams(name, ngramLen):
  if len(name) < ngramLen:
    ngramLen = len(name)
  ngramList = [name]
#  for n in range(1, ngramLen+1):
  ngramList.append(name[-ngramLen:len(name)])
  ngramList = list(set(ngramList))
  
  return ngramList


def get_counts(dataList, ngramLen):
  genIdx = 1
  namIdx = 0
  
  condProbs = {}
  probs = {}

  for rec in dataList:
    gender = rec[genIdx]
    name = rec[namIdx]
    
    # Create the 1st level dict for indep value
    if gender not in condProbs:
      condProbs[gender]={}
    
    for name in get_ngrams(name, ngramLen):
      # Create the 2nd level dict for dep value
      if name not in condProbs[gender]:
        condProbs[gender][name] = 0

      #Increment the conditional counts
      condProbs[gender][name] += 1

      # Also calculate the probabilities of names
      if name not in probs:
        probs[name] = 0
        
      probs[name] += 1

  return (condProbs, probs)
    
def get_probs(condProbs, probs):
  # Now divide the conditional counts with the totals to get prob
  for gen in condProbs:
    # Denominator = total number of people/names in list who are M or F, not just uniques
    denom = sum(condProbs[gen].values())
    for nam in condProbs[gen]:
      condProbs[gen][nam] =  condProbs[gen][nam]/denom
  
  # Also divide the name counts with totals to get prob
  # Denominator = total number of people/names in list, not the number of unique names
  tot = sum(probs.values())
  for nam in probs:
    probs[nam] = probs[nam]/tot
    
  return (condProbs, probs)
    
 
  
def save_probs(data, fn, ngramLen):

  dataList = []

  for row in data:
    if len(row) < 10:
      continue
    dataList.append([row[0], row[9]])

#  (trainSet, testSet) = splitDataset(dataList, 0.67)
#  print(len(trainSet), len(testSet))
  
  condProbs, nameProbs = get_counts(dataList, ngramLen)
  condProbs, nameProbs = get_probs(condProbs, nameProbs)
  
  with open(fn, 'wb') as pickleFile:
    pickle.dump([condProbs, nameProbs], pickleFile)
  
  
  
def load_probs(fn):
  with open(fn, 'rb') as pf:
    condProbs, nameProbs = pickle.load(pf)
  
  return (condProbs, nameProbs)


def is_female(rec, condProbs, nameProbs, gendProbs, ngramLen):
  name,gend = rec
  
  pr_f = 0
  pr_m = 0
  
  for ngram in get_ngrams(name, ngramLen):
    if ngram in condProbs['F']:
      pr_f += math.log(condProbs['F'][ngram])
    if ngram in condProbs['M']:
      pr_m = math.log(condProbs['M'][ngram])
                          
  pr_f = math.exp(pr_f + math.log(gendProbs['F']))
  pr_m = math.exp(pr_m + math.log(gendProbs['M']))
  
  if pr_f > pr_m:
    if gend=='M':
      
#      print("%s should be F but marked M, with probs, M: %f, F:%f" % (name, pr_m, pr_f))
      pass
    return 'F'
  else:
    return gend
  
  
def main():
    
  flt = FileUtils()
  data = flt.load_csv('parsedCsvAll.csv')
  
  ngramLen = 0

  prob_fn = 'probabilities.pcl'
  
  save_probs(data[1:100], prob_fn, ngramLen)
  condProbs, nameProbs = load_probs(prob_fn)
  print(condProbs, nameProbs)
  gendProbs = {'F':0.52, 'M':0.48}
  

#  newCsv = open("parsedCsv_gender.csv", 'w', encoding='utf-8', newline='\n')
#  csvWriter = csv.writer(newCsv, delimiter=',') 
#  csvWriter.writerow(data[0])

  for row in data[1:]:
    if len(row) < 10:
      continue
    if row[9] == 'M':
      row[9] = is_female([row[0], row[9]], condProbs, nameProbs, gendProbs, ngramLen)
      
#    csvWriter.writerow(row)

  
if __name__ == "__main__":
  main()