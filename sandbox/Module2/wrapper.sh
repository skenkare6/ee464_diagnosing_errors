#!/bin/bash

. DiffLinesFunction.sh | while read entry
do
Rscript contextLineNumber.R $entry
done
