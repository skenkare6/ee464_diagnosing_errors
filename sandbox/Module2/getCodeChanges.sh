#!/bin/bash

if [ -e changedCode.txt ]
then
	rm changedCode.txt
fi

if [ $# -eq 2 ]
then

	if [ $1 = 'redrawmappings' ]
	then
        	./DiffLinesFunction.sh $2 | while read entry
        	do
        	echo $entry >> changedCode.txt
        	done
	elif [ $1 = 'testselection' ]
	then
        	./DiffLinesFunction.sh $2 | while read entry
        	do
        	Rscript contextLineNumber.R $entry $2 >> changedCode.txt
        	done
	else
        	echo "Not a proper input"
	fi
else
	echo "no repository specified"
fi
