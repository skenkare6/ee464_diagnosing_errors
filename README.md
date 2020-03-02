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

4. Copy and paste the contents of `schema.sql` into the commandline.
5. Verify all of the tables specified in the `schema.sql` file are
   created via: `show tables;`.

6. Select the `test` database:

```
use test;
```

7. Repeat steps 4 and 5 and you're done.

### Fixes for issues with Python or mysql

Issue: pymysql.err.InternalError: (1698, "Access denied for user 'root'@'localhost'"). <br/>
Solution: Login into to mysql and enter the following lines.

```
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
mysql> FLUSH PRIVILEGES;
```   
Issue: Missing modules or other general python errors. <br/>
Solution: 
* Ensure you are using the following python tools:
  * python3
  * pymysql
  * pytest-3

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
