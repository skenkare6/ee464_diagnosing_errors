#!/bin/bash

if [ -e changedCode.txt ]
then
	rm changedCode.txt
fi

if [ $1 = 'redrawmappings' ]
then
        ./DiffLinesFunction.sh | while read entry
        do
        echo $entry >> changedCode.txt
        done
elif [ $1 = 'testselection' ]
then
        ./DiffLinesFunction.sh | while read entry
        do
        Rscript contextLineNumber.R $entry >> changedCode.txt
        done
else
        echo "Not a proper input"
fi
