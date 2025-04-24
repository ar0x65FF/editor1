from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from subgui.editor.dataeditorwindow import DataEditorWindow

from PyQt6.QtWidgets import (
    QWidget, 
    QTableWidget, 
    QTableWidgetItem, 
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidgetItem
)

class SongTableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = QTableWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.elements = []
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["Name", "TA", "OA", "CA", "EOD","Move Up","Mode Down","Edit","Remove"])

    def load_elements(self, elements):
        self.elements = elements
        self.table.setRowCount(len(elements))
        

        for i, el in enumerate(self.elements):
            self.table.setItem(i, 0, QTableWidgetItem("Song "+str(i)))
            self.table.setItem(i, 1, QTableWidgetItem(str(hex(el.tone_addr))))
            self.table.setItem(i, 2, QTableWidgetItem(str(hex(el.obligato_addr))))
            self.table.setItem(i, 3, QTableWidgetItem(str(hex(el.chord_addr))))
            self.table.setItem(i, 4, QTableWidgetItem(str(hex(el.endofdata))))

            up_btn = QPushButton()
            up_btn.setIcon(QIcon.fromTheme("arrow-up"))
            up_btn.clicked.connect(lambda _, idx=i: self.move_up(idx))
            self.table.setCellWidget(i, 5, up_btn)

            down_btn = QPushButton()
            down_btn.setIcon(QIcon.fromTheme("arrow-down"))
            down_btn.clicked.connect(lambda _, idx=i: self.move_down(idx))
            self.table.setCellWidget(i, 6, down_btn)

            edit_item_btn = QPushButton("Edit")
            edit_item_btn.setIcon(QIcon.fromTheme("entry-edit"))
            edit_item_btn.clicked.connect(lambda _, idx=i: self.edit_item(idx))
            self.table.setCellWidget(i, 7, edit_item_btn)

            remove_item_btn = QPushButton()
            remove_item_btn.setIcon(QIcon.fromTheme("entry-delete"))
            remove_item_btn.clicked.connect(lambda _, idx=i: self.remove_item(idx))
            self.table.setCellWidget(i, 8, remove_item_btn)

    def move_up(self, index):
        if index > 0:
            self.elements[index - 1], self.elements[index] = self.elements[index], self.elements[index-1]
            self.load_elements(self.elements)

    def move_down(self, index):
        if index < len(self.elements) - 1:
            self.elements[index - 1], self.elements[index] = self.elements[index], self.elements[index-1]
            self.load_elements(self.elements)
        
    def edit_item(self,index):
        editor = DataEditorWindow(self)
        editor.show()
        editor.load_elements_tone(self.elements[index].songdata.tone)
        editor.load_elements_obligato(self.elements[index].songdata.obligato)
        editor.load_elements_chord(self.elements[index].songdata.chord)

    def remove_item(self,index):
        del self.elements[index]
        self.load_elements(self.elements)