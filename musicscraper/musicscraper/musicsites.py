import ast
import sqlite3
import pandas as pd
import webbrowser
import os
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QColorDialog, QLabel

app = None


def choose_color(label):
    color = QColorDialog.getColor()
    if color.isValid():
        label.setText(color.name())


def create_music_sites():
    global app
    app = QApplication([])
    dialog = QDialog()
    layout = QVBoxLayout()

    # Create labels to display the chosen colors
    font_color_label = QLabel()
    bg_color_label = QLabel()

    # Create buttons and connect them to color dialogs
    font_color_button = QPushButton('Choose Font Color')
    font_color_button.clicked.connect(lambda: choose_color(font_color_label))
    bg_color_button = QPushButton('Choose Background Color')
    bg_color_button.clicked.connect(lambda: choose_color(bg_color_label))

    # Add the buttons and labels to the layout
    layout.addWidget(font_color_button)
    layout.addWidget(font_color_label)
    layout.addWidget(bg_color_button)
    layout.addWidget(bg_color_label)

    # Set the layout on the dialog and show the dialog
    dialog.setLayout(layout)
    dialog.exec_()  # This will block the code execution until the dialog is closed

    # Get the chosen colors
    font_color = font_color_label.text()
    bg_color = bg_color_label.text()

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

    # Start the HTML content with a style tag for the title
    html = f"""
            <html>
            <head>
                <style>
                    body {{
                        color: {font_color};  /* User chosen color for the font */
                        background-color: {bg_color};  /* User chosen color for the background */
                    }}
                    h1 {{
                        color: tomato;  /* Tomato color for the title */
                        font-family: Arial, sans-serif;
                        text-align: center;
                    }}
                </style>
            </head>
            <body>
            """
    print("Start the creating of the page")

    # Iterate over the rows in the DataFrame
    for index, row in data.iterrows():
        # Add the title to the HTML content
        html += f"<h1>{row['title']}</h1>"

        # Add the text and urls to the HTML content
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

    ########    edit .html file    ########

    # Open the HTML file and read its content
    with open(html_file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find all <p> tags and replace commas
    for p in soup.find_all('p'):
        p.string.replace_with(p.text.replace(',', ''))

    # Write the modified HTML back to the file
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print("Commas removed successfully from <p> tags!")
    print("The new .html file without commas created")

    # Open the HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(html_file_path))

    print("Function completed successfully!")
