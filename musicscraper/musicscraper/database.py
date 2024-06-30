import os
import subprocess
import pandas as pd
import sqlite3
import logging
from musicscraper.musicscraper.spiders import music_crawler
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def scrape_and_store(paragraph_name):
    # Define file paths for CSV and JSON output
    csv_file = "C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/item.csv"
    json_file = "C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/item.json"

    # Remove existing files if they exist
    if os.path.exists(csv_file):
        os.remove(csv_file)
    if os.path.exists(json_file):
        os.remove(json_file)

    # Run Scrapy spider to scrape data and save to CSV and JSON files
    subprocess.run(
        ["C:/Users/giann/PycharmProjects/Music_Web_Scraper/.venv/Scripts/python", "-m", "scrapy", "crawl", "music",
         "-a", f"paragraph_name={paragraph_name}", "-o", csv_file, "-o", json_file],
        cwd='C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper', stderr=subprocess.STDOUT)

    # Function to get the suffix based on the URL
    def get_suffix(url):
        return music_crawler.MusicSpider.get_suffix(url)

    # Read data from the JSON file into a Pandas DataFrame
    data_json = pd.read_json("C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/item.json")
    print("\n\n\n The json file is \n\n\n", data_json)
    print("JSON file read successfully!")
    # Get the file size of the JSON file
    file_size = os.path.getsize("C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/item.json")
    print("File Size is :", file_size, "bytes")

    # Ensure 'text' and 'urls' columns contain lists and handle non-list or missing values
    data_json['text'] = data_json['text'].apply(
        lambda x: x if isinstance(x, list) else [str(x) if pd.notnull(x) else ''])
    data_json['urls'] = data_json['urls'].apply(
        lambda x: x if isinstance(x, list) else [str(x) if pd.notnull(x) else ''])

    # Combine text lists and URL lists into comma-separated strings
    data_json['text'] = data_json['text'].apply(lambda x: ', '.join(x))
    data_json['urls'] = data_json['urls'].apply(lambda x: ', '.join(x))

    # Connect to the SQLite database
    db_connection = sqlite3.connect('mydatabase.db')
    cursor = db_connection.cursor()

    # Create the music_data table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS music_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            text TEXT,
            urls TEXT
        )
    """)

    # Print the DataFrame to the console
    # print("DataFrame before iteration:")
    # print(data_json)

    # Iterate over the rows in the DataFrame
    for index, row in data_json.iterrows():
        # Convert the row to a dictionary
        record = row.to_dict()

        # Get the suffix based on the URL and modify the title
        suffix = get_suffix(record['urls'])
        record['title'] = f"{record['title']} {suffix}"

        # Try to insert the record into the database
        try:
            cursor.execute("""
                INSERT INTO music_data (title, text, urls) VALUES (?, ?, ?)
            """, (record['title'], record['text'], record['urls']))
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate record: {record}")
            logging.warning(f"Skipping duplicate record: {record}")

    # Commit the changes and close the connection
    db_connection.commit()

    # Check which records don't have 'text' and 'urls' fields and delete them
    cursor.execute("""
        DELETE FROM music_data
        WHERE (text IS NULL OR text = '')
        AND (urls IS NULL OR urls = '')
    """)
    # Remove duplicates
    cursor.execute("""
            DELETE FROM music_data
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM music_data
                GROUP BY title, text, urls
            )
        """)

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