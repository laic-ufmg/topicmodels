Drex

Needs to be executed in 2 steps:
1. Cache generation, using command

python create_cache.py -i Datasets/newsN20short.csv -v WordVectors/newsN20short_vectors_glove.txt -l 2 -n 100 -c Cache/n20_100.txt

2. Expand Documents, using commnd

python expand.py -i Datasets/newsN20short.csv -s -v 2,7,20 -l 2 -c Cache/n20_100.txt -o Output/ -f n20_scale

