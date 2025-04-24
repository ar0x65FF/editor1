from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import pyqtSignal

import rofile.midictrl

from PyQt6.QtWidgets import (
    QWidget, 
    QDialog,
    QTableWidget, 
    QTableWidgetItem, 
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGroupBox,
    QTabWidget,
    QLineEdit,
    QSpinBox,
    QSpacerItem,
    QSizePolicy,
    QRadioButton,
    QFileDialog
)

class EditorControlsTone(QWidget):
    update_item_entry_signal = pyqtSignal()
    add_item_entry_signal = pyqtSignal()

    test_01_signal = pyqtSignal()
    test_02_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.input_layout = QHBoxLayout()
        self.id_spinbox = QSpinBox()
        self.id_spinbox.setRange(0,100000)

        self.instruction_lineedit = QLineEdit()
        self.instruction_lineedit.setText("0x10")

        self.param_1_lineedit = QLineEdit()
        self.param_1_lineedit.setText("0x00")

        self.param_2_lineedit = QLineEdit()
        self.param_2_lineedit.setText("0x00")

        self.input_layout.addWidget(self.id_spinbox)
        self.input_layout.addWidget(self.instruction_lineedit)
        self.input_layout.addWidget(self.param_1_lineedit)
        self.input_layout.addWidget(self.param_2_lineedit)


        self.buttons_layout = QHBoxLayout()
        self.update_button = QPushButton("Update")
        self.add_button = QPushButton("Add")

        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.update_button)


        self.update_button.clicked.connect(self.emit_update_item_entry_signal)
        self.add_button.clicked.connect(self.emit_add_item_entry_signal)

        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)
    
    def emit_update_item_entry_signal(self):
        self.update_item_entry_signal.emit()
    
    def emit_add_item_entry_signal(self):
        self.add_item_entry_signal.emit()

    def emit_test_01(self):
        self.test_01_signal.emit()
    def emit_test_02(self):
        self.test_02_signal.emit()


class EditorControlsObligato(QWidget):
    update_item_entry_signal = pyqtSignal()
    add_item_entry_signal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        
        self.input_layout = QHBoxLayout()
        self.id_spinbox = QSpinBox()
        self.id_spinbox.setRange(0,100000)

        self.instruction_lineedit = QLineEdit()
        self.instruction_lineedit.setText("0x10")

        self.param_1_lineedit = QLineEdit()
        self.param_1_lineedit.setText("0x00")

        self.param_2_lineedit = QLineEdit()
        self.param_2_lineedit.setText("0x00")

        self.input_layout.addWidget(self.id_spinbox)
        self.input_layout.addWidget(self.instruction_lineedit)
        self.input_layout.addWidget(self.param_1_lineedit)
        self.input_layout.addWidget(self.param_2_lineedit)


        self.buttons_layout = QHBoxLayout()
        self.update_button = QPushButton("Update")
        self.add_button = QPushButton("Add")

        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.update_button)


        self.update_button.clicked.connect(self.emit_update_item_entry_signal)
        self.add_button.clicked.connect(self.emit_add_item_entry_signal)

        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

    def emit_update_item_entry_signal(self):
        self.update_item_entry_signal.emit()
    
    def emit_add_item_entry_signal(self):
        self.add_item_entry_signal.emit()

class EditorControlsChord(QWidget):
    update_item_entry_signal = pyqtSignal()
    add_item_entry_signal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.input_layout = QHBoxLayout()
        self.id_spinbox = QSpinBox()
        self.id_spinbox.setRange(0,100000)

        self.instruction_lineedit = QLineEdit()
        self.instruction_lineedit.setText("0x10")

        self.param_1_lineedit = QLineEdit()
        self.param_1_lineedit.setText("0x00")


        self.input_layout.addWidget(self.id_spinbox)
        self.input_layout.addWidget(self.instruction_lineedit)
        self.input_layout.addWidget(self.param_1_lineedit)


        self.buttons_layout = QHBoxLayout()
        self.update_button = QPushButton("Update")
        self.add_button = QPushButton("Add")

        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.update_button)


        self.update_button.clicked.connect(self.emit_update_item_entry_signal)
        self.add_button.clicked.connect(self.emit_add_item_entry_signal)

        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

    def emit_update_item_entry_signal(self):
        self.update_item_entry_signal.emit()
    
    def emit_add_item_entry_signal(self):
        self.add_item_entry_signal.emit()

class SomeToolsControls(QWidget):
    export_midi_signal = pyqtSignal()

    import_tone_signal = pyqtSignal()
    import_obligato_signal = pyqtSignal()
    import_chord_signal = pyqtSignal()
    import_all_signal = pyqtSignal()

    export_tone_signal = pyqtSignal()
    export_obligato_signal = pyqtSignal()
    export_chord_signal = pyqtSignal()
    export_all_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        
        #MIDI GROUP - BEGIN
        midi_group_box = QGroupBox("MIDI")
        midi_group_box_layout = QHBoxLayout()
        export_midi_button = QPushButton("Export MIDI")
        convert_midi_button = QPushButton("Convert MIDI to Part")

        midi_group_box_layout.addWidget(export_midi_button)
        midi_group_box_layout.addWidget(convert_midi_button)

        midi_group_box_layout.addSpacerItem(QSpacerItem(40,20,QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum))
        midi_group_box.setLayout(midi_group_box_layout)
        #MIDI GROUP - END

        #IMPORT PARTS
        import_group_box = QGroupBox("Import/Export")
        import_group_box_layout = QVBoxLayout()

        import_part_group_box = QGroupBox("Part")
        import_part_group_box_layout = QHBoxLayout()
        self.tone_radio_button = QRadioButton("Tone")
        self.obligato_radio_button = QRadioButton("Obligato")
        self.chord_radio_button = QRadioButton("Chord")
        self.all_radio_button = QRadioButton("All")
        import_part_group_box_layout.addWidget(self.tone_radio_button)
        import_part_group_box_layout.addWidget(self.obligato_radio_button)
        import_part_group_box_layout.addWidget(self.chord_radio_button)
        import_part_group_box_layout.addWidget(self.all_radio_button)
        import_part_group_box.setLayout(import_part_group_box_layout)
        

        import_button = QPushButton("Import")
        export_button = QPushButton("Export")

        import_button.clicked.connect(self.import_button_func)
        export_button.clicked.connect(self.export_button_func)

        import_group_box_layout.addWidget(import_part_group_box)
        import_group_box_layout.addWidget(import_button)
        import_group_box_layout.addWidget(export_button)
        import_group_box.setLayout(import_group_box_layout)

        convert_midi_button.clicked.connect(self.convertmiditopart_func)
        export_midi_button.clicked.connect(self.exportmidi_emitsignal)

        layout.addWidget(midi_group_box)
        layout.addWidget(import_group_box)
        self.setLayout(layout)
    def exportmidi_emitsignal(self):
        self.export_midi_signal.emit()
    def convertmiditopart_func(self):
        src_file_dialog = QFileDialog()
        src_filename, _ = src_file_dialog.getOpenFileName(self, "Open MIDI","","MIDI (*.mid);;All files(*.*)")
        

        dst_file_dialog = QFileDialog()
        dst_filename, _ = dst_file_dialog.getSaveFileName(self, "Save part","","Part (*.part);;All files(*.*)")
        if dst_filename:
            if not dst_filename.lower().endswith(".part"):
                dst_filename += ".part"
        

        midictrl = rofile.midictrl.PartMidiControl()
        midictrl.part_converter(src_filename=src_filename, dst_filename=dst_filename)
    def import_button_func(self):
        if self.tone_radio_button.isChecked():
            self.import_tone_signal.emit()
        elif self.obligato_radio_button.isChecked():
            self.import_obligato_signal.emit()
        elif self.chord_radio_button.isChecked():
            self.import_chord_signal.emit()
        elif self.all_radio_button.isChecked():
            self.import_all_signal.emit()
        else:
            print("IM-UNK")
    
    def export_button_func(self):
        if self.tone_radio_button.isChecked():
            self.export_tone_signal.emit()
        elif self.obligato_radio_button.isChecked():
            self.export_obligato_signal.emit()
        elif self.chord_radio_button.isChecked():
            self.export_chord_signal.emit()
        elif self.all_radio_button.isChecked():
            self.export_all_signal.emit()
        else:
            print("EX-UNK")

class DataEditorWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.m_layout = QVBoxLayout()
        self.setWindowTitle("Editor")
        self.setMinimumSize(640,480)

        self.tone_elements = []
        self.obligato_elements = []
        self.chord_elements = []

        tab = QTabWidget()
        tone_edit_tab = QWidget()
        tone_edit_tab_layout = QVBoxLayout()
        self.tone_editor_controls = EditorControlsTone()
        self.tone_editor_controls.add_item_entry_signal.connect(self.add_element_tone)
        self.tone_editor_controls.update_item_entry_signal.connect(self.update_element_tone)
        self.tone_table = QTableWidget()
        self.tone_table.setColumnCount(5)
        self.tone_table.setHorizontalHeaderLabels(["INS","PARAM1","PARAM2","REMOVE","UPDATE"])
        
        tone_edit_tab_layout.addWidget(self.tone_editor_controls)
        tone_edit_tab_layout.addWidget(self.tone_table)
        tone_edit_tab.setLayout(tone_edit_tab_layout)

        

        obligato_edit_tab = QWidget()
        obligato_edit_tab_layout = QVBoxLayout()
        self.obligato_editor_controls = EditorControlsObligato()
        self.obligato_editor_controls.add_item_entry_signal.connect(self.add_element_obligato)
        self.obligato_editor_controls.update_item_entry_signal.connect(self.update_element_obligato)
        self.obligato_table = QTableWidget()
        self.obligato_table.setColumnCount(5)
        self.obligato_table.setHorizontalHeaderLabels(["INS","PARAM1","PARAM2","REMOVE", "UPDATE"])
        obligato_edit_tab_layout.addWidget(self.obligato_editor_controls)
        obligato_edit_tab_layout.addWidget(self.obligato_table)
        obligato_edit_tab.setLayout(obligato_edit_tab_layout)

        chord_edit_tab = QWidget()
        chord_edit_tab_layout = QVBoxLayout()
        self.chord_editor_controls = EditorControlsChord()
        self.chord_editor_controls.add_item_entry_signal.connect(self.add_element_chord)
        self.chord_editor_controls.update_item_entry_signal.connect(self.update_element_chord)
        self.chord_table = QTableWidget()
        self.chord_table.setColumnCount(5)
        self.chord_table.setHorizontalHeaderLabels(["INS","PARAM","REMOVE","UPDATE","DESC"])
        chord_edit_tab_layout.addWidget(self.chord_editor_controls)
        chord_edit_tab_layout.addWidget(self.chord_table)
        chord_edit_tab.setLayout(chord_edit_tab_layout)

        sometools_tab = QWidget()
        sometoolstab_layout = QVBoxLayout()
        self.sometoolscontrols = SomeToolsControls()
        sometoolstab_layout.addWidget(self.sometoolscontrols)
        sometools_tab.setLayout(sometoolstab_layout)

        self.sometoolscontrols.export_midi_signal.connect(self.exportmidi)

        self.sometoolscontrols.import_tone_signal.connect(lambda: self.import_part_func(1))
        self.sometoolscontrols.import_obligato_signal.connect(lambda: self.import_part_func(2))
        self.sometoolscontrols.import_chord_signal.connect(lambda: self.import_part_func(3))
        self.sometoolscontrols.import_all_signal.connect(lambda: self.import_part_func(4))

        self.sometoolscontrols.export_tone_signal.connect(lambda: self.export_part_func(1))
        self.sometoolscontrols.export_obligato_signal.connect(lambda: self.export_part_func(2))
        self.sometoolscontrols.export_chord_signal.connect(lambda: self.export_part_func(3))
        self.sometoolscontrols.export_all_signal.connect(lambda: self.export_part_func(4))


        tab.addTab(tone_edit_tab, "Tone")
        tab.addTab(obligato_edit_tab, "Obligato")
        tab.addTab(chord_edit_tab, "Chord")
        tab.addTab(sometools_tab, "Tools")
        self.m_layout.addWidget(tab)


        self.setLayout(self.m_layout)

    def load_elements_tone(self, elements):
        self.tone_elements = elements
        self.tone_table.setRowCount(len(elements))
        
        for i, el in enumerate(self.tone_elements):
            self.tone_table.setItem(i, 0, QTableWidgetItem(str(hex(el[0]))))
            self.tone_table.setItem(i, 1, QTableWidgetItem(str(hex(el[1]))))
            self.tone_table.setItem(i, 2, QTableWidgetItem(str(hex(el[2]))))

            remove_button = QPushButton()
            remove_button.setIcon(QIcon.fromTheme("entry-delete"))
            remove_button.clicked.connect(lambda _, idx=i: self.remove_item_tone(idx))
            self.tone_table.setCellWidget(i, 3, remove_button)

            update_button = QPushButton()
            update_button.setIcon(QIcon.fromTheme("entry-edit"))
            update_button.clicked.connect(lambda _, idx=i: self.load_item_data_tone(idx))
            self.tone_table.setCellWidget(i, 4, update_button)

    def load_elements_obligato(self, elements):
        self.obligato_elements = elements
        self.obligato_table.setRowCount(len(elements))

        for i, el in enumerate(self.obligato_elements):
            self.obligato_table.setItem(i, 0, QTableWidgetItem(str(hex(el[0]))))
            self.obligato_table.setItem(i, 1, QTableWidgetItem(str(hex(el[1]))))
            self.obligato_table.setItem(i, 2, QTableWidgetItem(str(hex(el[2]))))

            remove_button = QPushButton()
            remove_button.setIcon(QIcon.fromTheme("entry-delete"))
            remove_button.clicked.connect(lambda _, idx=i: self.remove_item_obligato(idx))
            self.obligato_table.setCellWidget(i,3,remove_button)

            update_button = QPushButton()
            update_button.setIcon(QIcon.fromTheme("entry-edit"))
            update_button.clicked.connect(lambda _, idx=i: self.load_item_data_obligato(idx))
            self.obligato_table.setCellWidget(i,4,update_button)
    
    def load_elements_chord(self, elements):
        self.chord_elements = elements
        self.chord_table.setRowCount(len(elements))

        for i, el in enumerate(self.chord_elements):
            self.chord_table.setItem(i, 0, QTableWidgetItem(str(hex(el[0]))))
            self.chord_table.setItem(i, 1, QTableWidgetItem(str(hex(el[1]))))

            remove_button = QPushButton()
            remove_button.setIcon(QIcon.fromTheme("entry-delete"))
            remove_button.clicked.connect(lambda _, idx=i: self.remove_item_chord(idx))
            self.chord_table.setCellWidget(i,2,remove_button)

            update_button = QPushButton()
            update_button.setIcon(QIcon.fromTheme("entry-edit"))
            update_button.clicked.connect(lambda _, idx=i: self.load_item_data_chord(idx))
            self.chord_table.setCellWidget(i,3,update_button)

            self.chord_table.setItem(i, 4, QTableWidgetItem(str(self.desc_element_chord(el))))

    def desc_element_chord(self,element):
        if element[0] == 0x10 and element[1] == 0x00:
            return "INIT/REST"
        elif element[0] == 0xF0 and element[1] == 0x00:
            return "END OF CHANNEL"

    def remove_item_tone(self,index):
        del self.tone_elements[index]
        self.load_elements_tone(self.tone_elements)

    def remove_item_obligato(self,index):
        del self.obligato_elements[index]
        self.load_elements_obligato(self.obligato_elements)

    def remove_item_chord(self,index):
        del self.chord_elements[index]
        self.load_elements_chord(self.chord_elements)

    def load_item_data_tone(self,index):
        self.tone_editor_controls.id_spinbox.setValue(index)
        self.tone_editor_controls.instruction_lineedit.setText(str(hex(self.tone_elements[index][0])))
        self.tone_editor_controls.param_1_lineedit.setText(str(hex(self.tone_elements[index][1])))
        self.tone_editor_controls.param_2_lineedit.setText(str(hex(self.tone_elements[index][2])))
    
    def load_item_data_obligato(self,index):
        self.obligato_editor_controls.id_spinbox.setValue(index)
        self.obligato_editor_controls.instruction_lineedit.setText(str(hex(self.obligato_elements[index][0])))
        self.obligato_editor_controls.param_1_lineedit.setText(str(hex(self.obligato_elements[index][1])))
        self.obligato_editor_controls.param_2_lineedit.setText(str(hex(self.obligato_elements[index][2])))

    def load_item_data_chord(self,index):
        self.chord_editor_controls.id_spinbox.setValue(index)
        self.chord_editor_controls.instruction_lineedit.setText(str(hex(self.chord_elements[index][0])))
        self.chord_editor_controls.param_1_lineedit.setText(str(hex(self.chord_elements[index][1])))


    def update_element_tone(self):
        target_id = self.tone_editor_controls.id_spinbox.value()
        instruction = int(self.tone_editor_controls.instruction_lineedit.text(), 16)
        param_1 = int(self.tone_editor_controls.param_1_lineedit.text(), 16) 
        param_2 = int(self.tone_editor_controls.param_2_lineedit.text(), 16)
        b = bytearray()
        b.append(instruction)
        b.append(param_1)
        b.append(param_2) 
        self.tone_elements[target_id] = b
        self.load_elements_tone(self.tone_elements)

    def add_element_tone(self):
        target_id = self.tone_editor_controls.id_spinbox.value()
        instruction = int(self.tone_editor_controls.instruction_lineedit.text(), 16)
        param_1 = int(self.tone_editor_controls.param_1_lineedit.text(), 16) 
        param_2 = int(self.tone_editor_controls.param_2_lineedit.text(), 16)
        b = bytearray()
        b.append(instruction)
        b.append(param_1)
        b.append(param_2) 
        self.tone_elements.insert(target_id,b)
        self.load_elements_tone(self.tone_elements)
        self.tone_editor_controls.id_spinbox.setValue(target_id+1)

    def update_element_obligato(self):
        target_id = self.obligato_editor_controls.id_spinbox.value()
        instruction = int(self.obligato_editor_controls.instruction_lineedit.text(), 16)
        param_1 = int(self.obligato_editor_controls.param_1_lineedit.text(), 16)
        param_2 = int(self.obligato_editor_controls.param_2_lineedit.text(), 16)
        b = bytearray()
        b.append(instruction)
        b.append(param_1)
        b.append(param_2)
        self.obligato_elements[target_id] = b
        self.load_elements_obligato(self.obligato_elements)
    
    def add_element_obligato(self):
        target_id = self.obligato_editor_controls.id_spinbox.value()
        instruction = int(self.obligato_editor_controls.instruction_lineedit.text(), 16)
        param_1 = int(self.obligato_editor_controls.param_1_lineedit.text(), 16)
        param_2 = int(self.obligato_editor_controls.param_2_lineedit.text(), 16)
        b = bytearray()
        b.append(instruction)
        b.append(param_1)
        b.append(param_2)
        self.obligato_elements.insert(target_id,b)
        self.load_elements_obligato(self.obligato_elements)
        self.obligato_editor_controls.id_spinbox.setValue(target_id+1)

    def update_element_chord(self):
        target_id = self.chord_editor_controls.id_spinbox.value()
        instruction = int(self.chord_editor_controls.instruction_lineedit.text(), 16)
        param = int(self.chord_editor_controls.param_1_lineedit.text(), 16)
        b = bytearray()
        b.append(instruction)
        b.append(param)
        self.chord_elements[target_id] = b
        self.load_elements_chord(self.chord_elements)
        self.chord_editor_controls.id_spinbox.setValue(target_id+1)
    
    def add_element_chord(self):
        target_id = self.chord_editor_controls.id_spinbox.value()
        instruction = int(self.chord_editor_controls.instruction_lineedit.text(), 16)
        param = int(self.chord_editor_controls.param_1_lineedit.text(), 16)
        b = bytearray()
        b.append(instruction)
        b.append(param)
        self.chord_elements.insert(target_id,b)
        self.load_elements_chord(self.chord_elements)
        self.chord_editor_controls.id_spinbox.setValue(target_id+1)

    def exportmidi(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getSaveFileName(self, "Export MIDI","","MIDI (*.mid);;All files(*.*)")
        if filename:
            if not filename.lower().endswith(".mid"):
                filename += ".mid"
        midictrl = rofile.midictrl.PartMidiControl()
        midictrl.writemidifile(self.tone_elements, self.obligato_elements,filename=filename)

    def import_part_func(self, data):
        src_file_dialog = QFileDialog()
        src_filename, _ = src_file_dialog.getOpenFileName(self, "Load part","","Part (*.part);;All files(*.*)")

        if src_filename != None and src_filename != "":
            all_data = []

            if data == 1:
                with open(src_filename, "rb") as f:
                    while True:
                        chunk = f.read(3)
                        if len(chunk) < 3:
                            break
                        all_data.append(bytearray(chunk))
                        self.tone_elements.append(chunk)
                        self.load_elements_tone(self.tone_elements)
            elif data == 2:
                with open(src_filename, "rb") as f:
                    while True:
                        chunk = f.read(3)
                        if len(chunk) < 3:
                            break
                        all_data.append(bytearray(chunk))
                        self.obligato_elements.append(chunk)
                        self.load_elements_obligato(self.obligato_elements)
            elif data == 3:
                with open(src_filename, "rb") as f:
                    while True:
                        chunk = f.read(2)
                        if len(chunk) < 2:
                            break
                        all_data.append(bytearray(chunk))
                        self.chord_elements.append(chunk)
                        self.load_elements_chord(self.chord_elements)
            

    def export_part_func(self, data):
        dst_file_dialog = QFileDialog()
        dst_filename, _ = dst_file_dialog.getSaveFileName(self, "Save part","","Part (*.part);;All files(*.*)")
        
        if dst_filename is not None and dst_filename != "":
            if dst_filename:
                if not dst_filename.lower().endswith(".bin"):
                    dst_filename += ".bin"
            if data == 1:
                with open(dst_filename, "wb") as f:
                    for chunk in self.tone_elements:
                        f.write(chunk)
            if data == 2:
                with open(dst_filename, "wb") as f:
                    for chunk in self.obligato_elements:
                        f.write(chunk)
            if data == 3:
                with open(dst_filename, "wb") as f:
                    for chunk in self.chord_elements:
                        f.write(chunk)