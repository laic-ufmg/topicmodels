import sys
import gensim
import argparse

def read_args(argv=None):
    if( argv is None ):
        argv = sys.argv

    parser = argparse.ArgumentParser(description="DREx cache creator program.")

    parser.add_argument("-i", "--input", help="Input dataset file", required=True)
    parser.add_argument("-v", "--vectors", help="Words vectors file (word2vec format)", required=True)
    parser.add_argument("-b", "--binary", help="Set words vectors file to binary", action='store_true', default=False)
    parser.add_argument("-l", "--ngram_len", help="N-gram length", type=int, default=2)
    parser.add_argument("-n", "--num_similar_words", help="Number of similar words per ngram",type=int, default=200)
    parser.add_argument("-c", "--cache_filename", help="Cache file",required=True)

    args = parser.parse_args(argv[1:])
    
    return args

def read_words_model(args):

    if args.vectors is not None:
        print "Loading words vectors model...",
        sys.stdout.flush()
        
        try:
            words_model = None
            if args.binary:
                words_model = gensim.models.Word2Vec.load_word2vec_format(args.vectors, binary=True)
            else:
                words_model = gensim.models.Word2Vec.load_word2vec_format(args.vectors, binary=False)
            words_model.init_sims(replace=True)
        except:
            print "FAILED!"
            sys.stdout.flush()
        print "Done!"
        sys.stdout.flush()
    return words_model

def create_cache(args,words_model):
    fin = open(args.input)
    fout = open(args.cache_filename,'w')

    ngrams_set = set()


    print "Creating cache file"
    sys.stdout.flush()

    for line in fin:
        text = line.strip().split(',')[-1]
        words = text.strip().split()

        ngrams = zip(*[words[i:] for i in range(args.ngram_len)])

        for ngram in ngrams:
            ngram_words = sorted(ngram)
            ngram_str = "+".join(ngram_words)

            if ngram_str in ngrams_set:
                continue

            ngrams_set.add(ngram_str)

            similar_words_str_list = []
            for sim_word,sim_score in words_model.most_similar(positive=ngram_words, topn=args.num_similar_words):
                similar_words_str_list.append( "%s:%s" % (sim_word,sim_score) )

            similar_words_str = " ".join(similar_words_str_list)

            print >> fout, "%s;%s" % (ngram_str,similar_words_str)

    fout.close()
    print "Done!"
    sys.stdout.flush()

def main():
    args = read_args()
    words_model = read_words_model(args)
    create_cache(args,words_model)

if __name__ == "__main__":
    main()
