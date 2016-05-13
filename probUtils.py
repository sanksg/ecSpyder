import random

class ProbUtils:
  def __init__(self):
    pass

  def split_dataset(self, dataList, splitRatio):
    trainSize = int(len(dataList) * splitRatio)
    trainSet = []
    testSet = list(dataList)
    while len(trainSet) < trainSize:
      index = random.randrange(len(testSet))
      trainSet.append(testSet.pop(index))
    return [trainSet, testSet]


  def get_ngrams(self, name, ngramLen, wholeWord):
    if len(name) < ngramLen:
      ngramLen = len(name)
    ngramList = []

    if wholeWord:
      ngramList.append(name)

#    for n in range(1, ngramLen+1):
    ngramList.append(name[-ngramLen:len(name)])
    ngramList = list(set(ngramList))

#    print(ngramList)
    return ngramList


  def get_ngram_probs(self, dataList, ngramLen, wholeWord):

    condProbs = {}

    #Calculate Pr(name | gender) for each record
    for rec in dataList:
      name, gender = rec
      name = name.strip().lower()
      
      # First level is gender
      if gender not in condProbs:
        condProbs[gender]={}

      # Second level is the name
      for name in self.get_ngrams(name, ngramLen, wholeWord):
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
