# ee464_diagnosing_errors

## Design from 2020-02-05 meeting

* Database
  * MySQL
  * Format
    * `production` database and `test` database
      * each database has a `functions` and a `tests` table
      * `tests` table has fields: `name`, `id`, `function_id`
      * `functions` table has fields: `name`, `id`, `test_id`
  * John is creating the schema file and setup script that should
    set up the database on first use/reload
  * Need to ask Kevin about where database can live: persisted or set up
    on each use? `dump_to_csv` and `load_from_csv`?
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
