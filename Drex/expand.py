import sys
import argparse
import numpy as np

def read_args(argv=None):
    if( argv is None ):
        argv = sys.argv

    parser = argparse.ArgumentParser(description="DREx cache creator program.")

    parser.add_argument("-i", "--input", help="Input dataset file", required=True)
    parser.add_argument("-s", "--type_scale", help="Set DREx to calculate the number of expansion words using a scale factor of the document size", action='store_true', default=False)
    parser.add_argument("-v","--expansion_values", help="List of number of expansion words or scaling factors (separated by commas)", required=True)
    parser.add_argument("-l", "--ngram_len", help="N-gram length", type=int, default=2)
    parser.add_argument("-c", "--cache_filename", help="Cache file",required=True)
    parser.add_argument("-o", "--output_path", help="Output path",required=True)
    parser.add_argument("-f", "--output_files_prefix", help="Prefix of output files", required=True)
    parser.add_argument("-p", "--probabilistic_selection", help="Set DREx to use probabilistic selection instead of top N selection",default=False,action="store_true")

    args = parser.parse_args(argv[1:])

    return args


def read_cache(args):
    cache = {}

    fin = open(args.cache_filename)
    for line in fin:
        ngram,similars = line.strip().split(";")
        similars = [ (pair.strip().split(":")[0],float(pair.strip().split(":")[1])) for pair in similars.strip().split() ]

        cache[ngram] = similars

    return cache

def selection(args,candidates,n):
    if( args.probabilistic_selection == True ):
        words = candidates.keys()
        probs = np.array( map(float,candidates.values()) )
        probs /= probs.sum()

        expansionWords = np.random.choice(a=words,size=n,replace=False, p=probs)
    else:
        expansionWords = [pair[0] for pair in sorted(candidates.items(),key=lambda x:x[1],reverse=True)[:n] ]

    return list(expansionWords)

def expand_documents(args,cache,value,corpus):
    fout = open("%s/%s_%s.csv" % (args.output_path,args.output_files_prefix,value), "w")

    for line in corpus:
        beforeText = line.strip().split(",")[:-1]
        text = line.strip().split(",")[-1]

        original_words = text.strip().split()
        doc_size = len(original_words)

        nExpand = 0
        if(args.type_scale == True):
            target_size = int(float(value) * doc_size + 0.5)
            nExpand = target_size - doc_size
        else:
            nExpand = int(value) - doc_size

        if nExpand <= 0:
            print >> fout, line.strip()
            continue

        ngrams = zip(*[original_words[i:] for i in range(args.ngram_len)])
        
        candidates = {}
        for ngram in ngrams:
            ngram_words = sorted(ngram)
            ngram_str = "+".join(ngram_words)

            if ngram_str not in cache:
                print "Failed to retrieve similars words for ngram %s" % (ngram_str)
                print "Please verify the cache file"
                print "Exiting"
                sys.stdout.flush()
                sys.exit(1)

            
            for similarWord,similarScore in cache[ngram_str][:nExpand]:
                candidates[similarWord] = candidates.get(similarWord,0) + similarScore

        
        expansion_words = selection(args,candidates,nExpand)
        
        expandedText = " ".join(original_words+expansion_words)
        print >> fout, ",".join(beforeText + [expandedText])

    fout.close()


def main():
    args = read_args()
    cache = read_cache(args)


    corpus = [line.strip() for line in open(args.input)]
    expansion_values = args.expansion_values.strip().split(",")
    for value in expansion_values:
        expand_documents(args,cache,value,corpus)


if __name__ == "__main__":
    main()
