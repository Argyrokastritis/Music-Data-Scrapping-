import os
import sqlite3
import webbrowser
import pandas as pd

def create_music_sites():
    print("Starting the function...")

    # Connect to the SQLite database
    print("Connecting to the SQLite database...")
    db_connection = sqlite3.connect('mydatabase.db')

    # Read the data from the database
    print("Reading the data from the database...")
    data = pd.read_sql_query("SELECT * from music_data", db_connection)

    # Close the database connection
    print("Closing the database connection...")
    db_connection.close()

    #############################################

    # Start the HTML content with a style tag for the title
    html = """
        <html>
        <head>
            <style>
                h1 {
                    color: #ff6347;  /* Tomato color */
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
            </style>
        </head>
        <body>
        """

    # Iterate over the rows in the DataFrame
    for index, row in data.iterrows():
        # Add the title, text, and urls to the HTML content
        html += f"<h1>{row['title']}</h1>"
        html += f"<p>{row['text']}</p>"
        html += f"<p>{row['urls']}</p>"

    # End the HTML content
    html += "</body></html>"

    # Define the HTML file path
    html_file_path = "C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/music_data.html"

    # Write the HTML to a file
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print("HTML file created successfully!")

    # Open the HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(html_file_path))

    print("Function completed successfully!")

