# ee464_diagnosing_errors

## Contents of the repo
* `MySQL_Scripts` contains scripts for setting up MySQL
* `env` is a python virtual environment. This isn't fully set up, so you
  might not want to use this yet.
* `reports` contains all of our written reports for our Senior Design
  class. The report `i5_EE464FinalReport.pdf` is our final report that
  documents our work on this project.
* `sandbox` currently contains scratch code and our code for the testing
  harness, test-to-source tool, and diffs-in-code tool. Ideally,
  everything that is not scratch would be moved to `src`.
* `src` contains our source code
* `test` contains our source code's tests.
* Other misc. files: `Docker` files and convenience scripts for `MySQL`.

## TODO

* Add test case description to `RTestCase` in database
* Move modules 1 and 2 into `src/` directory of our repo

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

