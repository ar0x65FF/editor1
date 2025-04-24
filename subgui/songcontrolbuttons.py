from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal

class SongControlButtonsWidget(QWidget):
    add_row_signal = pyqtSignal()
    import_song_signal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

        self.add_song_button = QPushButton(QIcon.fromTheme("add-entry"), "Add")
        self.add_song_button.setDisabled(True)
        self.add_song_button.clicked.connect(self.add_item_signal)

        self.import_song_button = QPushButton("Import")
        self.import_song_button.setDisabled(True)
        self.import_song_button.clicked.connect(self.import_song_signal)

    

        layout = QHBoxLayout()
        layout.addWidget(self.add_song_button)
        layout.addWidget(self.import_song_button)
        layout.addSpacerItem(QSpacerItem(40,20,QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.setLayout(layout)
    def add_item_signal(self):
        self.add_row_signal.emit()
    def import_song_func(self):
        self.import_song_signal.emit()