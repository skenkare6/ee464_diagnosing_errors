SOCKET_PATH=../ee464SqlSocket

mysql -u root --socket=${SOCKET_PATH} < destroy_database.sql
. start_database.sh
