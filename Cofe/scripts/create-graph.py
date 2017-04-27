import os, sys
import numpy as np

# inverted index for dataset
def createIndex (filename):
  with open(filename) as fin:
    index = {} # inverted index
    docID = 0
    for line in fin:
      words = line.split(';')[2].strip().split()
      for w in words:
        if w not in index:
          index[w] = set()
        index[w].add(docID)
      docID += 1

    return index

# creates word similarity graph with Jaccard index
# graph is an adjacency list
# indexes in list comes from word indexes in sorted vocab
def createGraph(index, nAdjs):
  vocab = index.keys()
  vocab.sort()
  graph = [[] for i in range(len(vocab))]
  for i1 in range(len(vocab) - 1):
    for i2 in range(i1 + 1, len(vocab)):
      w1 = vocab[i1]
      w2 = vocab[i2]

      docs1 = index[w1]
      docs2 = index[w2]

      intersec = len(docs1.intersection(docs2))
      union = len(docs1.union(docs2))
      jacc = intersec / float(union)
      
      if intersec > 0:
        graph[i1].append((jacc, i2))
        graph[i2].append((jacc, i1))

  # keeps only the nAdjs best adjs for each word
  for i1 in range(len(vocab) - 1):
    graph[i1].sort(reverse=True)
    if len(graph[i1]) > nAdjs:
      graph[i1] = graph[i1][:nAdjs]

  return graph, vocab


# format:
# filename nAdjs
# word:adj;sim adj2;sim adj3;sim
def storeGraph(nameInput, nameOutput, graph, vocab, nAdjs):
  nameOutput += "-graph" + '.txt'
  with open(nameOutput, 'w') as fout:
    fout.write("%s %s\n" % (filename, nAdjs))
    for i in range(len(vocab)):
      w = vocab[i]
      fout.write(w + ':')
      for sim, adj in graph[i]:
        fout.write("%s;%f " % (vocab[adj], sim))
      fout.write('\n')

        
filename = sys.argv[1]
nAdjs = int(sys.argv[2])
outname = sys.argv[3]
index = createIndex(filename)
graph, vocab = createGraph(index, nAdjs)
storeGraph(filename, outname, graph, vocab, nAdjs)










