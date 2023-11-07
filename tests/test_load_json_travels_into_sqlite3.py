import sys
import sqlite3
import io
sys.path.append("src")
from load_json_travels_into_sqlite3 import insert_data_into_database, query_and_display_results

db_connection = sqlite3.connect(':memory:')
cursor = db_connection.cursor()

sample_data = [
    {
        "year": 2019,
        "country": "Country1",
        "airports": [
            {"iata_code": "AAA", "icao_code": "TEST1"},
            {"iata_code": "BBB", "icao_code": "TEST2", "total_passengers": "20000"}
        ]
    },
    {
        "year": 2019,
        "country": "Country2",
        "airports": [
            {"iata_code": "CCC", "icao_code": "TEST3", "total_passengers": "30000"},
            {"iata_code": "DDD", "icao_code": "TEST4", "total_passengers": "40000"}
        ]
    }
]

cursor.execute('''CREATE TABLE IF NOT EXISTS travels(
                        year INT,
                        country TEXT,
                        iata_code CHAR(3),
                        icao_code CHAR(4),
                        total_passengers INT
                        )''')

def test_insert_data_into_database():
    '''Test if data is inserted correctly even if a key is missing in the JSON (supposition)'''
    # cursor.execute('DELETE FROM travels')
    insert_data_into_database(cursor, sample_data)
    cursor.execute('''SELECT * FROM travels''') 
    data = cursor.fetchall()
    
    assert data == [(2019, "Country1", "AAA", "TEST1", None),
                   (2019, "Country1", "BBB", "TEST2", 20000),
                   (2019, "Country2", "CCC", "TEST3", 30000),
                   (2019, "Country2", "DDD", "TEST4", 40000)]
    
def test_aggregation():
    query_and_display_results(cursor)

    # Capture the printed output
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Query and display results
    query_and_display_results(cursor)

    # Reset sys.stdout
    sys.stdout = sys.__stdout__

    # Check if the printed output matches the expected result
    expected_output = "Country2 --> Total Passengers: 70000\nCountry1 --> Total Passengers: 20000\n"
    assert captured_output.getvalue() == expected_output

