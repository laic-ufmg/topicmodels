#!/bin/bash

home=/home/speed/gabrielmip/TopicModeling
dataExpanded=$home/ShortTailedCoFE/data_expanded
output=$home/Results/ShortTailedCoFE

cd ${home}/Baselines/Src/LDAOpt

for sizeDoc in 1 2 3 4 5 6 7 8; do
  for input in `ls ${dataExpanded}/${sizeDoc}/*_LDA.txt`; do
    #if [[ $input == *"All"* || $input == *"all"* || $input == *"Fold"* || $input == *"loseitComments"* || $input == *"Posts"* || $input == *"Full"* ]] ; then
    #  continue
    #fi
    file=$(basename $input)
    dataset=${file%_LDA.*}
    echo $dataset
    echo $input
    for nt in 20 50 100; do
      for i in 1 ; do #nexec
        outputDir="${output}/${dataset}/${nt}Topics/LDA-ShortTailedCoFE-${sizeDoc}/${i}/"
        mkdir -p $outputDir
        if [[ ! -s $outputDir/model-final.twords ]] ; then
            echo $nt $i
            sbatch -p phocus ./run.sh $input $nt $outputDir
        fi
      done
    done
  done
done
