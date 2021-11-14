# To run server_postgres.py, please make sure you have already done the following steps:
 1. Create the database "final_project"
 2. Import the tables created in "schema_postgres.sql"
 3. Have psycopg2 package on your device. If not, please run the command in your terminal: "pip install psycopg2-binary".
 
To read from the Twitter API, please call "python server_postgres.py" on your terminal. To stop reading, please press ctrl + C.
To read from JSON file, please call "python server_postgres.py --file 'name of file'".

# Examples you can try:
python server_postgres.py
python server_postgres.py --file 'tweets.json'
