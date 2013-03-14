#!/bin/sh

VARIANT=$1

#for file in $(ls $VARIANT); do
#  echo $file ',' $(./latency.py $VARIANT/$file) ',' $(./droprate.py $VARIANT/$file) ',' $(./throughput.py $VARIANT/$file)
#done

for file in $(ls $VARIANT); do
  LATENCY=$(echo $(./latency.py $VARIANT/$file | sed 's/\://g'))
  REALLATENCY=$(echo $LATENCY | awk '{ print $1, "," , $2 "," , $3 ",", $4 }')
  echo $file ',' $REALLATENCY ',' $(./droprate.py $VARIANT/$file) ',' $(./throughput.py $VARIANT/$file) | sed 's/ //g'
done

