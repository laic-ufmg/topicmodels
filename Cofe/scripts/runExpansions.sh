#!/bin/bash

datasets=/home/speed/p.bicalho/UFMG/TopicModeling/Datasets/Preprocessed
home=/home/speed/gabrielmip/TopicModeling/ShortTailedCoFE
caches=$home/caches
dataExpanded=$home/data_expanded
nAdjs=10

for i in 1 2 3 4 5; do
  if [[ ! -d $dataExpanded/$i ]] ; then
    mkdir $dataExpanded/$i
  fi
done

for input in `ls ${datasets}/*/*/*.csv`; do
  if [[ $input == *"All"* || $input == *"all"* || $input == *"Fold"* || $input == *"loseitComments"* || $input == *"Posts"* || $input == *"Full"* ]] ; then
    continue
  fi

  file=$(basename $input)
  dataset=${file%.*}

  echo $dataset
  echo $input

  if [[ ! -e $caches/$dataset-graph.txt ]] ; then
    echo "Creating graph..."
    python $home/scripts/create-graph.py $input $nAdjs $caches/$dataset
  fi
  
  for i in 1 2 3 4 5 6 7 8; do
    echo "Expanding... ${i} times the original document size"
    python $home/scripts/expand.py $input $dataExpanded/$i/$dataset.csv $caches/$dataset-graph.txt $i
  done
done

for input in `ls ${datasets}/*/*.csv`; do
  if [[ $input == *"All"* || $input == *"all"* || $input == *"Fold"* || $input == *"loseitComments"* || $input == *"Posts"* || $input == *"Full"* ]] ; then
    continue
  fi

  file=$(basename $input)
  dataset=${file%.*}

  echo $dataset
  echo $input

  if [[ ! -e $caches/$dataset-graph.txt ]] ; then
    echo "Creating graph..."
    python $home/scripts/create-graph.py $input $nAdjs $caches/$dataset
  fi
  
  for i in 1 2 3 4 5 6 7 8; do
    echo "Expanding... ${i} times the original document size"
    python $home/scripts/expand.py $input $dataExpanded/$i/$dataset.csv $caches/$dataset-graph.txt $i
  done
done

