import json
import sqlite3

# Functions
def load_json_into_memory(path):
    '''Load JSON into Python memory if the path exists'''
    try:
        with open(path, 'r') as f:
            travels = json.load(f)
        return travels
    except FileNotFoundError:
        print('The file does not exist')
        return None

def create_database_schema(cursor):
    '''Creates the destination database schema in sqlite3 DB if it doesn't exist'''
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS travels(
                        year INT,
                        country TEXT,
                        iata_code CHAR(3),
                        icao_code CHAR(4),
                        total_passengers INT
                        )''')
    except sqlite3.Error as e:
        print(f'*****Error creating the database schema: {e}*****')

def insert_data_into_database(cursor, travels_data):
    '''Iterates over the JSON file, saving the required fields into variables. If the field is missing --> None value is added to prevent error'''
    # Iterate every country
    for obj in travels_data:
        year = obj.get('year', None)
        country = obj.get('country', None)
        airports = obj.get('airports', None)

        if airports:
            # Iterates the airports information array
            for airport_data in airports:
                iata_code = airport_data.get('iata_code', None)
                icao_code = airport_data.get('icao_code', None)
                total_passengers = airport_data.get('total_passengers', None)
                # Insert the values into the sqlite3 DB named travels
                cursor.execute('''INSERT INTO travels
                                  VALUES(?, ?, ?, ?, ?)''',
                                  (year, country, iata_code, icao_code, total_passengers))

def query_and_display_results(cursor):
    '''Displays in the console the total passengers per country'''
    try:
        cursor.execute('''SELECT
                        country,
                        SUM(total_passengers)
                        FROM travels
                        GROUP BY country
                        ORDER BY SUM(total_passengers) DESC''') 
        # Fetch the query result --> List of Tuples
        results = cursor.fetchall()

        # Display the results iterating over the list
        for row in results:
            print(f'{row[0]} --> Total Passengers: {row[1]}')
    except sqlite3.Error as e:
        print(f'Error querying the table: {e}')

# Script
travels_json_path = '../raw-data/data.json'
travels_data = load_json_into_memory(travels_json_path)

if travels_data:
    db_connection = sqlite3.connect('travels.db')
    cursor = db_connection.cursor()

    create_database_schema(cursor)
    insert_data_into_database(cursor, travels_data)
    query_and_display_results(cursor)

    # Close the connection to the database following best practices
    db_connection.close()