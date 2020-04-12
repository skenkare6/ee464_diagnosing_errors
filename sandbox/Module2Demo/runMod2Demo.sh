
cp contextLineNumber.R DiffLinesFunction.sh module2.py wrapper.sh ../AnomalyDetection/
cd ../AnomalyDetection/

python3 module2.py

rm changedFunctions.txt contextLineNumber.R DiffLinesFunction.sh module2.py wrapper.sh
