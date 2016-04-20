import pickle

with open('voterRecords.pcl', 'rb') as voterFile:
  data = pickle.load(voterFile)

print(len(data))
