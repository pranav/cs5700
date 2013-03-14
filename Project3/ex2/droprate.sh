#!/bin/sh

for file in $(ls vegas-vegas); do
	echo -n $file " : "
	./droprate.py vegas-vegas/$file
done
