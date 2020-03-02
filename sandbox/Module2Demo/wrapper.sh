rm changedFunctions.txt
. DiffLinesFunction.sh | while read entry
do
Rscript contextLineNumber.R $entry >> changedFunctions.txt
done

echo "Functions that were changed:"
cat changedFunctions.txt
echo
echo "Tests to be run:"
python3 getTests.py
