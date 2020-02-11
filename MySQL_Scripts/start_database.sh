#Starts the SQL database and prepares the tables

DATA_DIR=../SqlDataDirectory
SOCKET_PATH=../ee464SqlSocket

mkdir -p ${DATA_DIR}
mysqld --datadir=${DATA_DIR} --socket=${SOCKET_PATH} &
mysql -u root --socket=${SOCKET_PATH} < create_databases.sql
mysql -u root --socket=${SOCKET_PATH} test < populate_database.sql
mysql -u root --socket=${SOCKET_PATH} production < populate_database.sql

