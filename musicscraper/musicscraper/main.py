from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
import sys
from musicscraper.musicscraper import database


def scrape_music():
    # Get the paragraph name from the text input field
    paragraph_name = text_input.text()

    # Call the function from the database module
    database.scrape_and_store(paragraph_name)


app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Music Scraper")
window.setGeometry(100, 100, 250, 100)  # sets the default dimensions to 300x200
window.setWindowIcon(QIcon(
    'C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/musicscraper/note.ico'))  # sets the window icon

# TODO
# Set the background color of the window to light yellow
window.setStyleSheet("background-color: yellow;")

# Create a QWidget and set it as the central widget
central_widget = QWidget()
window.setCentralWidget(central_widget)

# Create a QVBoxLayout and add it to the central widget
layout = QVBoxLayout(central_widget)

# Create the 'Create Music Sites' button
create_button = QPushButton('Create Music Sites')
create_button.setStyleSheet(
    'QPushButton {background-color: orange; color: white;}')  # changes the button color to orange and text color to white
# create_button.clicked.connect(create_music_sites)
create_button.setFixedSize(120, 30)
layout.addWidget(create_button, 0, Qt.AlignCenter)

# Add a label for the text input field
label = QLabel("Select a topic to scrape:")
layout.addWidget(label, 0, Qt.AlignCenter)

# Create a text input field for the paragraph name
text_input = QLineEdit()
layout.addWidget(text_input, 0, Qt.AlignCenter)

# Add a stretch to push the button to the bottom
layout.addStretch()

button = QPushButton('Scrape')
button.setStyleSheet(
    'QPushButton {background-color: red; color: white;}')  # changes the button color to red and text color to white
button.clicked.connect(scrape_music)
button.setFixedSize(40, 30)
layout.addWidget(button, 0, Qt.AlignCenter)

window.show()

sys.exit(app.exec_())
