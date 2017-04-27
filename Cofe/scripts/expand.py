import os, sys
import numpy as np
import random
import math

def readGraph(filename):
  with open(filename) as fin:
    sims = {}
    info = fin.readline().split()
    oriInput = info[0]
    nAdjs = int(info[1].strip())
    for line in fin:
      info = line.split(':')
      word = info[0]
      if word not in sims:
        sims[word] = []
      for pair in info[1].split():
        adj, sim = pair.split(';')
        sims[word].append((adj, float(sim)))
    return sims


# select pseudo-randomly a word from a list
# using the 'weight' value of the tuple to represent
# the item's likelihood to be chosen
def selectWord(words):
  max_value = sum([weight for vertex, weight in words])
  rand_num = random.uniform(0, max_value)
  pointer = 0 
  for vertex, weight in words:
    pointer += weight
    if rand_num <= pointer:
      return vertex, weight


def expand(originalName, outputName, graph, nTimes):
  originalFile = open(originalName)
  outputFile = open(outputName, 'w')
  for line in originalFile:
    info = line.strip().split(';')
    id = info[0]
    label = info[1]
    doc = info[2].split()
     
    candidates = {}
    for word in doc:
      for adj, sim in graph[word]:
        if adj not in candidates:
          candidates[adj] = 0
        candidates[adj] += sim
    
    # selecting candidates that are not in the orginal doc
    candidates = [(w, candidates[w]) for w in candidates if w not in doc and candidates[w] > 0]
    
    # selecting new words
    newDoc = doc[:]
    while len(newDoc) < len(doc) * nTimes and len(candidates) > 0:
      pair = selectWord(candidates)
      word, sim = pair
      newDoc.append(word)
      candidates.remove(pair) # without replacement
    
    # writing final pseudo document
    outputFile.write("%s;%s;" % (id, label))
    for w in newDoc:
      outputFile.write(w + ' ')
    outputFile.write('\n')
  outputFile.close()
  originalFile.close()



originalFile = sys.argv[1]
outputFile = sys.argv[2]
graphName = sys.argv[3]
nTimes = int(sys.argv[4])
graph = readGraph(graphName)
expand(originalFile, outputFile, graph, nTimes)
