#!/bin/sh

for file in $(ls tahoe); do
	echo -n $file " : "
	./droprate.py tahoe/$file
done
ex2/vegas-vegas/
