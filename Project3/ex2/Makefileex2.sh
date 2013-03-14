#!/bin/sh

VARIANT=$1

for file in $(ls $VARIANT); do
  latency=$(echo $(./latency.py $VARIANT/$file) | sed 's/ /,/g')
  droprate=$(echo $(./droprate.py $VARIANT/$file) | sed 's/ /,/g')
  throughput=$(echo $(./throughput.py $VARIANT/$file) | sed 's/ /,/g')
  echo $file ',' $latency ',' $droprate ',' $throughput | sed 's/ //g'
done

