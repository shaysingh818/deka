cd server
cd db
rm server.db
touch server.db
cat server.sql | sqlite3 server.db
cd ../ 
cd ../

cd cli_tool
cd db
rm client.db
touch client.db
cat client.sql | sqlite3 client.db

#made a change here
