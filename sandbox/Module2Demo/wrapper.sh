#!/bin/bash
#rm changedFunctions.txt
echo "Calling git diff on the Anomaly Detection project..."
echo
./DiffLinesFunction.sh | while read entry
do
Rscript contextLineNumber.R $entry >> changedFunctions.txt
done

echo "Parsing list of functions that have changed..."
#cat changedFunctions.txt
#echo
#echo "Tests to be run:"
#python3 getTests.py
