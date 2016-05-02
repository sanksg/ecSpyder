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


def get_probs(dataList, separator):
  if separator == 'gender':
    indIdx = -1
    depIdx = 0
  else:
    indIdx = 0
    depIdx = -1
  
  condProbs = {}
  probs = {}

  for rec in dataList:
    indVal = rec[indIdx]
    depVal = rec[depIdx]
    nam = rec[0]
        
    # Create the 1st level dict for indep value
    if indVal not in condProbs:
      condProbs[indVal]={}
    # Create the 2nd level dict for dep value
    if depVal not in condProbs[indVal]:
      condProbs[indVal][depVal] = 0
      
    # Also calculate the probabilities of names
    if nam not in probs:
      probs[nam] = 0
    probs[nam] += 1
    
    #Increment the conditional counts
    condProbs[indVal][depVal] += 1
  
  # Now divide the conditional counts with the totals to get prob
  for key in condProbs:
    # Denominator = total number of people/names in list who are M or F, not just uniques
    denom =sum(condProbs[key].values())
    for pred in condProbs[key]:
      condProbs[key][pred] =  condProbs[key][pred]/denom
  
  # Also divide the name counts with totals to get prob
  # Denominator = total number of people/names in list, not the number of unique names
  tot = sum(probs.values())
  print(tot)
  for nam in probs:
    probs[nam] = probs[nam]/tot
    
  return (condProbs, probs)
    
 

def male_or_female(dataList, condProbs, nameProbs, gendProbs):
  right = 0
  wrong = 0

  for name,gend in dataList:
    pr_f = 0
    pr_m = 0
    if name in condProbs['F']:
      pr_f = math.exp(math.log(condProbs['F'][name]) + math.log(gendProbs['F']))
    if name in condProbs['M']:
      pr_m = math.exp(math.log(condProbs['M'][name]) + math.log(gendProbs['M']))
    
    if pr_m > pr_f and gend=='F':
      print("%s should be M but marked F, with probs, M: %f, F:%f" % (name, pr_m, pr_f))
      wrong+=1
    elif pr_f > pr_m and gend == 'F':
      right+=1
    elif pr_f > pr_m and gend=='M':
#      print("%s should be F but marked M, with probs, M: %f, F:%f" % (name, pr_m, pr_f))
      pass    
  
  print("Acurracy of F or not: %f" % float((right/(right+wrong)) * 100))
  
def main():
  flt = FileUtils()
  data = flt.load_csv('parsedCsvAll.csv')
#  print(str(data).encode('utf-8'))
  data = data[1:]
  dataList = []

  for row in data:
    dataList.append([row[0], row[9]])
#    print(dataList)

#  (trainSet, testSet) = splitDataset(dataList, 0.67)
#  print(len(trainSet), len(testSet))
  
  condProbs, nameProbs = get_probs(dataList,'gender')
  with open('probabilities.pcl', 'wb') as pickleFile:
      pickle.dump([condProbs, nameProbs], pickleFile)
      
#  gendProbs = {'F':0.52, 'M':0.48}
  
#  maleSet = [rec for rec in dataList if rec[1]=='M']
  
#  male_or_female(testSet, condProbs, nameProbs, gendProbs)
  
  
if __name__ == "__main__":
  main()