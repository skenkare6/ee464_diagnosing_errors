Command to run module 2:
>> python3 module2.py --mode <execution mode>

The execution mode options are testselection or redrawmappings

- Need to fix the execution so the module can be run from outside the Anomaly Detection folder
- Need to find an alternate to the source() method in contextLineNumber.R]
- Consolidate mod2_getFunctionNames.sh + mod2_getFileNames.sh into one file
- Find a way to not create changedFunctions.txt/changedFiles.txt when calling mod2_getFunctionNames.sh/mod2_getFileNames.sh respectively
- Call source-to-test from within module2.py function redrawmappings()
