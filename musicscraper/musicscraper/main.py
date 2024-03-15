from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import subprocess


def scrape_music():
    # Call your scrapy function here
    subprocess.run(
        ["C:/Users/giann/PycharmProjects/Music_Web_Scraper/.venv/Scripts/python", "-m", "scrapy", "crawl", "music"],
        cwd='C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper', stderr=subprocess.STDOUT)


app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Music Scraper")
window.setGeometry(100, 100, 250, 100)  # sets the default dimensions to 300x200
window.setWindowIcon(QIcon('C:/Users/giann/PycharmProjects/Music_Web_Scraper/musicscraper/musicscraper/note.ico'))  # sets the window icon

# Set the background color of the window to white
window.setStyleSheet("background-color: yellow;")

# Create a QWidget and set it as the central widget
central_widget = QWidget()
window.setCentralWidget(central_widget)

# Create a QVBoxLayout and add it to the central widget
layout = QVBoxLayout(central_widget)

# Create the 'Create Music Sites' button
create_button = QPushButton('Create Music Sites')
create_button.setStyleSheet('QPushButton {background-color: orange; color: white;}')  # changes the button color to orange and text color to white
#create_button.clicked.connect(create_music_sites)
create_button.setFixedSize(120, 30)
layout.addWidget(create_button, 0, Qt.AlignCenter)

# Add a stretch to push the button to the bottom
layout.addStretch()

button = QPushButton('Scrape')
button.setStyleSheet('QPushButton {background-color: red; color: white;}')  # changes the button color to red and text color to white
button.clicked.connect(scrape_music)
button.setFixedSize(40, 30)
layout.addWidget(button, 0, Qt.AlignCenter)

window.show()

sys.exit(app.exec_())