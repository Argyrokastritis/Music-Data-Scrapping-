import os
import subprocess
import pandas as pd
import sqlite3


def scrape_and_store(paragraph_name):
    csv_file = "C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/item.csv"
    json_file = "C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/item.json"

    if os.path.exists(csv_file):
        os.remove(csv_file)
    if os.path.exists(json_file):
        os.remove(json_file)

    subprocess.run(
        ["C:/Users/giann/PycharmProjects/Music_Web_Scraper/.venv/Scripts/python", "-m", "scrapy", "crawl", "music",
         "-a", f"paragraph_name={paragraph_name}", "-o", csv_file, "-o", json_file],
        cwd='C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper', stderr=subprocess.STDOUT)

    data_json = pd.read_json("C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/item.json")
    print("JSON file read successfully!")

    file_size = os.path.getsize("C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/item.json")
    print("File Size is :", file_size, "bytes")

    data_json['text'] = data_json['text'].apply(lambda x: ', '.join(x))
    data_json['urls'] = data_json['urls'].apply(lambda x: ', '.join(x))

    # Connect to the SQLite database
    db_connection = sqlite3.connect('mydatabase.db')
    cursor = db_connection.cursor()

    # Create the music_data table if it doesn't exist
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS music_data (
                title TEXT UNIQUE,
                text TEXT,
                urls TEXT
            )
        """)

    # Iterate over the rows in the DataFrame
    for index, row in data_json.iterrows():
        # Convert the row to a dictionary
        record = row.to_dict()

        # Try to insert the record into the database
        try:
            data_json.iloc[[index]].to_sql('music_data', con=db_connection, if_exists='append', index=False)
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate record: {record}")

    # Commit the changes and close the connection
    db_connection.commit()
    db_connection.close()

def drop_database():
    # Connect to the SQLite database
    db_connection = sqlite3.connect('mydatabase.db')
    cursor = db_connection.cursor()

    # Drop the table
    cursor.execute("DROP TABLE IF EXISTS music_data")

    # Commit the changes and close the connection
    db_connection.commit()
    db_connection.close()

    # Remove the database file
    os.remove('mydatabase.db')

    print("Database dropped successfully!")


