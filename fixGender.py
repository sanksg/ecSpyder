import csv
import random
import math
import pickle
from pprint import pprint
from fileUtils import FileUtils
from probUtils import ProbUtils


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
    name = name.strip().lower()
    
    if name in bayesProbs:
      continue
      
    bayesProbs[name]={}

    pr_f = float(1)
    pr_m = float(1)
    for ngram in probUtils.get_ngrams(name, ngramLen, wholeWord):
            
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
#  pprint (bayesProbs)
  return bayesProbs

    
def male_or_female(name, gender, bayesProbs):
  pr_m = 0
  pr_f = 0
  
  #Check lowercase only
  name = name.strip().lower()
  
  if name in bayesProbs:
    if "M" in bayesProbs[name]:
      pr_m = bayesProbs[name]["M"]  
  
    if "F" in bayesProbs[name]:
      pr_f = bayesProbs[name]["F"]
#  else:
#    print(name)
#  
  if pr_f > pr_m:
    return "F"
  else:
    return gender

  
def get_probs(data, prob_fn, gendProbs, ngramLen, wholeWord):

  dataList = []

  #Calculate probabilities for F records only
  for row in data:
    if len(row) < 10:# or row[9] == "M":
      continue

    dataList.append([row[0].strip().lower(), row[9]])
  
  condProbs = probUtils.get_ngram_probs(dataList, ngramLen, wholeWord)
  bayesProbs = calc_bayes_probs(dataList, condProbs, gendProbs, ngramLen, wholeWord)
  
  return bayesProbs

  
def main():
  dataFn = 'parsedCsvAll.csv'
  outFn = 'parsedCsv_gender.csv'
  probsOut = "calcProbs.csv"
  prob_fn = 'probabilities.pcl'

  trainTestRatio = 0.67
  ngramLen = 0
  wholeWord = True
  gendProbs = {'F':0.52, 'M':0.48}

  global flt
  global probUtils
  flt = FileUtils()
  probUtils = ProbUtils()
  
  csvWriter = flt.init_csv(outFn)
  probWriter = flt.init_csv(probsOut)
  
  print ("Filenames dataFn=%s, and outFn=%s" %(dataFn, outFn))
  data = flt.load_csv(dataFn)
  (trainSet, testSet) = probUtils.split_dataset(data[1:], trainTestRatio)

  print(len(trainSet), len(testSet))
  bayesProbs = get_probs(trainSet, prob_fn, gendProbs, ngramLen, wholeWord)
  probWriter.writerow(["Name", "Prob_M", "Prob_F"])
  for key in bayesProbs:
    probWriter.writerow([key, bayesProbs[key]['M'], bayesProbs[key]['F']])
  
  # Write the column headings
  data[0].append("Orig")
  csvWriter.writerow(data[0])

  
  total = 0
  f2m = 0
  m2f = 0
  fems = 0
  males = 0
  
  for row in testSet:
    # If the row doesn't have all the parameters, just skip it
    if len(row) < 10:
      continue
    
    predGender = male_or_female(row[0], row[9], bayesProbs)
    
    total+=1
    #Check if right or wrong
    if (predGender == "F"):
      fems += 1
      if row[9] == "M":
        m2f +=1
    else:
      #If original value was F and we marked it as M, it's an error
      if row[9] == "F":
        f2m += 1
        
      males += 1
    
    #Write the predictions
    row.append(row[9])
    row[9] = predGender
    csvWriter.writerow(row)
  
  
  percents = []
  for val in [m2f, f2m, fems, males]:
    percents.append((val/total)*100)
    
  
  print("M2F: {:f}%  F2M: {:f}% , Females: {:f}%, Males: {:f}%".format(*percents))
  print("Total: ", total)

    
if __name__ == "__main__":
  main()