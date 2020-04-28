Command to run module 2:
>> python3 module2.py -r \<repository name\> --mode \<execution mode\>

The repository name is the name of the github repository we are testing
The execution mode options are testselection or redrawmappings

Things to do:
- Need to find an alternate to the source() method in contextLineNumber.R
- Call source-to-test from within module2.py function redrawmappings() (right now its just printing)
- If database is empty:
	- Can we assume that the repository name will be in the database prior to calling redrawmappings?
	- Can we assume that if RFunctions table is populated than the other tables (RTestCases, etc) are populated?
