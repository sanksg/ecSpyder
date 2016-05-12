import csv
import random
import math
import pickle
from pprint import pprint
from fileUtils import FileUtils


def split_dataset(dataList, splitRatio):
  trainSize = int(len(dataList) * splitRatio)
  trainSet = []
  copy = list(dataList)
  while len(trainSet) < trainSize:
    index = random.randrange(len(copy))
    trainSet.append(copy.pop(index))
  return [trainSet, copy]


def get_ngrams(name, ngramLen, wholeWord):
  if len(name) < ngramLen:
    ngramLen = len(name)
  ngramList = []
  
  if wholeWord:
    ngramList.append(name)
  
  for n in range(1, ngramLen+1):
    ngramList.append(name[-n:len(name)])
    ngramList = list(set(ngramList))
  
#  print(ngramList)
  return ngramList


def get_ngram_probs(dataList, ngramLen, wholeWord):
  
  condProbs = {}

  for rec in dataList:
    name, gender = rec
    
    # Create the 1st level dict for indep value
    if gender not in condProbs:
      condProbs[gender]={}
    
    for name in get_ngrams(name, ngramLen, wholeWord):
      # Create the 2nd level dict for dep value
      if name not in condProbs[gender]:
        condProbs[gender][name] = 0

      #Increment the conditional counts
      condProbs[gender][name] += 1

  # Now divide the conditional counts with the totals to get prob
  for gender in condProbs:
    # Denominator = total number of people/names in list who are M or F, not just uniques
    denom = sum(condProbs[gender].values())
    
    for nam in condProbs[gender]:
      condProbs[gender][nam] =  condProbs[gender][nam]/denom
  

  return condProbs
    

#  
#def load_probs(fn):
#  with open(fn, 'rb') as pf:
#    condProbs, nameProbs = pickle.load(pf)
#  
#  return (condProbs, nameProbs)



def calc_bayes_probs(dataList, condProbs, gendProbs, ngramLen, wholeWord):
  
  bayesProbs = {}
  
  for rec in dataList:
    name, gend = rec

    
    if name in bayesProbs:
      continue
      
    bayesProbs[name]={}

    pr_f = 1
    pr_m = 1
    for ngram in get_ngrams(name, ngramLen, wholeWord):
            
      if 'F' in condProbs and ngram in condProbs['F']:
        pr_f *= condProbs['F'][ngram]

      if 'M' in condProbs and ngram in condProbs['M']:
        pr_m *= condProbs['M'][ngram]

    if pr_f == 1:
      pr_f = 0
    if pr_m == 1:
      pr_m = 0
      
    pr_f = pr_f * gendProbs['F']
    pr_m = pr_m * gendProbs['M']
    
    #  print(pr_f, pr_m)
    
    bayesProbs[name]["M"] = pr_m
    bayesProbs[name]["F"] = pr_f

#  pprint(bayesProbs)
  return bayesProbs

    
def male_or_female(name, gender, bayesProbs):
  pr_m = 0
  pr_f = 0
  
  if name in bayesProbs:
    if "M" in bayesProbs[name]:
      pr_m = bayesProbs[name]["M"]  
  
    if "F" in bayesProbs[name]:
      pr_f = bayesProbs[name]["F"]
  
  if pr_f > pr_m:
    return "F"
  else:
    return gender

  
def get_probs(data, prob_fn, gendProbs, ngramLen, wholeWord):

  dataList = []

  for row in data:
    if len(row) < 10 or row[9] == "M":
      continue
#    if row[9] == "F":
    dataList.append([row[0].strip().lower(), row[9]])

#  (trainSet, testSet) = splitDataset(dataList, 0.67)
#  print(len(trainSet), len(testSet))
  
  condProbs = get_ngram_probs(dataList, ngramLen, wholeWord)
  bayesProbs = calc_bayes_probs(dataList, condProbs, gendProbs, ngramLen, wholeWord)
  
  return bayesProbs
#  with open(prob_fn, 'wb') as pickleFile:
#    pickle.dump([calcLogProbs, nameProbs], pickleFile)
  
  
def main():
  
  
  flt = FileUtils()
  
  dataFn = 'parsedCsvAll.csv'
  outFn = 'parsedCsv_gender.csv'
  
  
  for i in range(0, 1):
    print ("Run #%d with dataFn=%s, and outFn=%s" %(i, dataFn, outFn))
    data = flt.load_csv(dataFn)

    ngramLen = 2
    wholeWord = True
    gendProbs = {'F':0.50, 'M':0.50}
    
    prob_fn = 'probabilities.pcl'

    
    bayesProbs = get_probs(data[1:], prob_fn, gendProbs, ngramLen, wholeWord)


    newCsv = open(outFn, 'w', encoding='utf-8', newline='\n')
    csvWriter = csv.writer(newCsv, delimiter=',') 
    csvWriter.writerow(data[0])

    for row in data[1:]:
      if len(row) < 10:
        continue
      
      row[9] = male_or_female(row[0].strip().lower(), row[9], bayesProbs)

      csvWriter.writerow(row)

    temp = outFn
    outFn = dataFn
    dataFn = temp
    
if __name__ == "__main__":
  main()