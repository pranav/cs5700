#!/bin/sh

for file in $(ls tahoe); do
  NUM=$(echo $file | egrep -o '_[0-9]*\.' | egrep -o '[0-9]*')
  sed -i "s/\$/,$NUM/g" tahoe/$file
done
