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

    # Set the window title, color and default size
    dialog.setWindowTitle('Color Picker Menu')
    dialog.setStyleSheet("QDialog { background-color: lightpink; }")
    dialog.resize(300, 150)

    # Create labels to display the chosen colors
    font_color_label = QLabel()
    bg_color_label = QLabel()

    # Create buttons and connect them to color dialogs
    font_color_button = QPushButton('Choose Font Color')
    font_color_button.clicked.connect(lambda: choose_color(font_color_label))
    bg_color_button = QPushButton('Choose Background Color')
    bg_color_button.clicked.connect(lambda: choose_color(bg_color_label))

    # Create an OK button to close the dialog
    ok_button = QPushButton('OK')
    ok_button.clicked.connect(dialog.accept)

    # Add the buttons and labels to the layout
    layout.addWidget(font_color_button)
    layout.addWidget(font_color_label)
    layout.addWidget(bg_color_button)
    layout.addWidget(bg_color_label)
    layout.addWidget(ok_button)

    # Set the layout on the dialog and show the dialog
    dialog.setLayout(layout)
    dialog.exec_()

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

    # # Start the HTML content with a style tag for the title
    # html = f"""
    #         <html>
    #         <head>
    #             <style>
    #                 body {{
    #                     color: {font_color};
    #                     background-color: {bg_color};
    #                 }}
    #                 h1 {{
    #                     color: tomato;
    #                     font-family: Arial, sans-serif;
    #                     text-align: center;
    #                 }}
    #             </style>
    #         </head>
    #         <body>
    #         """
    # print("Start the creating of the page")
    #
    # # Iterate over the rows in the DataFrame
    # for index, row in data.iterrows():
    #     # Add the title to the HTML content if it's not None
    #     if pd.notna(row['title']):
    #         html += f"<h1>{row['title']}</h1>"
    #         if "of Music" in row['title']:
    #             html += f'The original source of the paragraph can be found here: <button onclick="window.open(\'https://en.wikipedia.org/wiki/Music\', \'_blank\');">Original Source</button>'
    #         elif "of Clef" in row['title']:
    #             html += f'The original source of the paragraph can be found here: <button onclick="window.open(\'https://en.wikipedia.org/wiki/Clef\', \'_blank\');">Original Source</button>'
    #
    #     # Add the text and urls to the HTML content if they are not None
    #     if pd.notna(row['text']):
    #         html += f"<p>{row['text']}</p>"
    #     if pd.notna(row['urls']):
    #         html += f"<p>{row['urls']}</p>"
    #
    # # End the HTML content
    # html += "</body></html>"
    #
    # # Define the HTML file path
    # html_file_path = "C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/music_data.html"
    #
    # # Write the HTML to a file
    # with open(html_file_path, 'w', encoding='utf-8') as f:
    #     f.write(html)
    #
    # print("HTML file created successfully!")

    # Iterate over the unique titles in the DataFrame
    for title in data['title'].unique():
        # Filter the data for the current title
        title_data = data[data['title'] == title]

        # Start the HTML content for the current title
        title_html = f"""
                    <html>
                    <head>
                        <style>
                            body {{
                                color: {font_color};
                                background-color: {bg_color};
                            }}
                            h1 {{
                                color: tomato;
                                font-family: Arial, sans-serif;
                                text-align: center;
                            }}
                        </style>
                    </head>
                    <body>
                    """

        # Iterate over the rows in the title data
        for index, row in title_data.iterrows():
            # Add the title, text and urls to the HTML content if they are not None
            if pd.notna(row['title']):
                title_html += f"<h1>{row['title']}</h1>"
                if "of Music" in row['title']:
                    title_html += f'The original source of the paragraph can be found here: <button onclick="window.open(\'https://en.wikipedia.org/wiki/Music\', \'_blank\');">Original Source</button>'
                elif "of Clef" in row['title']:
                    title_html += f'The original source of the paragraph can be found here: <button onclick="window.open(\'https://en.wikipedia.org/wiki/Clef\', \'_blank\');">Original Source</button>'
            if pd.notna(row['text']):
                title_html += f"<p>{row['text']}</p>"
            if pd.notna(row['urls']):
                title_html += f"<p>{row['urls']}</p>"

        # End the HTML content for the current title
        title_html += "</body></html>"

        # Define the HTML file path for the current title
        title_html_file_path = f"C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/{title.replace(' ', '_')}.html"

        # Write the HTML for the current title to a file
        with open(title_html_file_path, 'w', encoding='utf-8') as f:
            f.write(title_html)

    # Start the HTML content for the main page
    main_html = f"""
                <html>
                <head>
                    <style>
                        body {{
                            color: {font_color};
                            background-color: {bg_color};
                        }}
                        h1 {{
                            color: tomato;
                            font-family: Arial, sans-serif;
                            text-align: center;
                        }}
                    </style>
                </head>
                <body>
                """

    # Iterate over the unique titles in the DataFrame
    for title in data['title'].unique():
        # Add a button for the current title to the HTML content
        main_html += f'<button onclick="window.open(\'{title.replace(' ', '_')}.html\', \'_blank\');">{title}</button><br>'

    # End the HTML content for the main page
    main_html += "</body></html>"

    # Define the HTML file path for the main page
    main_html_file_path = "C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/main.html"

    # Write the HTML for the main page to a file
    with open(main_html_file_path, 'w', encoding='utf-8') as f:
        f.write(main_html)

    # Open the main HTML file in the default web browser
    # webbrowser.open('file://' + os.path.realpath(main_html_file_path))

    # ########    edit .html file    ########
    #
    # # Open the HTML file and read its content
    # with open(html_file_path, 'r', encoding='utf-8') as f:
    #     soup = BeautifulSoup(f, 'html.parser')
    #
    # # Find all <p> tags and replace commas
    # for p in soup.find_all('p'):
    #     if p.string is not None:
    #         p.string.replace_with(p.text.replace(',', ''))
    #
    # # Write the modified HTML back to the file
    # with open(html_file_path, 'w', encoding='utf-8') as f:
    #     f.write(str(soup))
    #
    # print("Commas removed successfully from <p> tags!")
    # print("The new .html file without commas created")
    #
    # # Open the HTML file in the default web browser
    # webbrowser.open('file://' + os.path.realpath(html_file_path))
    #
    # print("Function completed successfully!")

    # Iterate over the unique titles in the DataFrame
    for title in data['title'].unique():
        # Define the HTML file path for the current title
        title_html_file_path = f"C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/{title.replace(' ', '_')}.html"

        ########    edit .html file    ########

        # Open the HTML file and read its content
        with open(title_html_file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Find all <p> tags and replace commas
        for p in soup.find_all('p'):
            if p.string is not None:
                p.string.replace_with(p.text.replace(',', ''))

        # Write the modified HTML back to the file
        with open(title_html_file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"Commas removed successfully from <p> tags in {title}!")
        print(f"The new .html file without commas for {title} created")

    # Start the HTML content for the main page
    main_html = f"""
                <html>
                <head>
                    <style>
                        body {{
                            color: {font_color};
                            background-color: {bg_color};
                            text-align: center;
                        }}
                        h1 {{
                            color: tomato;
                            font-family: Arial, sans-serif;
                            text-align: center;
                        }}
                        button {{
                            font-size: 20px;
                            margin: 10px;
                        }}
                    </style>
                </head>
                <body>
                <h1>List of Extracted Paragraphs</h1>
                """

    # Iterate over the unique titles in the DataFrame
    for title in data['title'].unique():
        # Add a button for the current title to the HTML content
        main_html += f'<button onclick="window.open(\'{title.replace(' ', '_')}.html\', \'_blank\');">{title}</button><br>'

    # End the HTML content for the main page
    main_html += "</body></html>"

    # Define the HTML file path for the main page
    main_html_file_path = "C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/main.html"

    # Write the HTML for the main page to a file
    with open(main_html_file_path, 'w', encoding='utf-8') as f:
        f.write(main_html)

    # Open the main HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(main_html_file_path))

    print("Function completed successfully!")


if __name__ == '__main__':
    create_music_sites()
