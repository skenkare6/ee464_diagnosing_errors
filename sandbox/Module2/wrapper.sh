#!/bin/bash

GIT_ROOT=$(git rev-parse --show-toplevel)

. DiffLinesFunction.sh | grep *\.[rR]$ | while read entry
do
Rscript contextLineNumber.R ${GIT_ROOT}/${entry}
done
