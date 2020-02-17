# ee464_diagnosing_errors

## Getting started
### Setting up the MySQL databases

1. Install and log into mysql
2. Copy and paste the contents of `schema.sql` into the commandline
3. If there are any errors, figure out what the last executed command
   was and repeat step 2 with the commands that weren't ran.

Alternatively, install `docker` and `docker-compose`, and run:

```
sh start_mysql.sh
```

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
