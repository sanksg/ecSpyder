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


def get_counts(dataList):
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
    denom =sum(condProbs[gen].values())
    for nam in condProbs[gen]:
      condProbs[gen][nam] =  condProbs[gen][nam]/denom
  
  # Also divide the name counts with totals to get prob
  # Denominator = total number of people/names in list, not the number of unique names
  tot = sum(probs.values())
  for nam in probs:
    probs[nam] = probs[nam]/tot
    
  return (condProbs, probs)
    
 

def is_female(rec, condProbs, nameProbs, gendProbs):
  name,gend = rec
  
  pr_f = 0
  pr_m = 0
  if name in condProbs['F']:
    pr_f = math.exp(math.log(condProbs['F'][name]) + math.log(gendProbs['F']))
  if name in condProbs['M']:
    pr_m = math.exp(math.log(condProbs['M'][name]) + math.log(gendProbs['M']))

  if pr_f > pr_m:
    if gend=='M':
      print("%s should be F but marked M, with probs, M: %f, F:%f" % (name, pr_m, pr_f))
    return 'F'
  else:
    return gend
  
  
  
def save_probs(data, fn):

  dataList = []

  for row in data:
    if len(row) < 10:
      continue
    dataList.append([row[0], row[9]])

#  (trainSet, testSet) = splitDataset(dataList, 0.67)
#  print(len(trainSet), len(testSet))
  
  condProbs, nameProbs = get_counts(dataList)
  condProbs, nameProbs = get_probs(condProbs, nameProbs)
  
  with open(fn, 'wb') as pickleFile:
    pickle.dump([condProbs, nameProbs], pickleFile)
  
  
  
def load_probs(fn):
  with open(fn, 'rb') as pf:
    condProbs, nameProbs = pickle.load(pf)
  
  return (condProbs, nameProbs)
  
  
def main():
    
  flt = FileUtils()
  data = flt.load_csv('parsedCsvAll.csv')

  prob_fn = 'probabilities.pcl'
#  save_probs(data[1:], prob_fn)
#  return 0
  condProbs, nameProbs = load_probs(prob_fn)
  gendProbs = {'F':0.52, 'M':0.48}
  

  newCsv = open("parsedCsv_gender.csv", 'w', encoding='utf-8', newline='\n')
  csvWriter = csv.writer(newCsv, delimiter=',') 
  csvWriter.writerow(data[0])
  
#  i = 1
  for row in data[1:]:
#    print(i)
    if len(row) < 10:
      continue
    if row[9] == 'M':
      row[9] = is_female([row[0], row[9]], condProbs, nameProbs, gendProbs)
      
    csvWriter.writerow(row)

  
if __name__ == "__main__":
  main()