#!/bin/sh

for file in $(ls ex2/vegas-vegas); do
	echo -n $file " : "
	./droprate.py ex2/vegas-vegas/$file
done
