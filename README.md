# ee464_diagnosing_errors

## Getting started
### Setting up the MySQL databases

1. Install and log into mysql
2. Run the following if you haven't already:

```
create database production;
create database test;
```

3. Select the `production` database:

```
use production;
```

4. Copy and paste the contents of `schema.sql` into the commandline.
5. Verify all of the tables specified in the `schema.sql` file are
   created via: `show tables;`.

6. Select the `test` database:

```
use test;
```

7. Repeat steps 4 and 5 and you're done.

## Design from 2020-02-05 meeting

* Database
* COVR vs foodweb/callgraphs
* Teams
  * As previously defined in the System Design Report
  * Test-to-source
    * Canyon
    * Saarila
  * Git diffs/regression test selection
    * Janvi
    * John
  * Source-to-test
    * Jennings
    * Michael
* Output
  * Will decide later down the road, maybe with Kevin?
  * For now, here is an example of some formatted text we agreed upon:

```
function1: test1,test2,test3
function2: test2,test4,test5
```
