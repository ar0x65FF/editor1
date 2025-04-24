import sys

from subgui.songtablewidget import SongTableWidget
from subgui.loggerwidget import MessageLoggerBox
from subgui.songcontrolbuttons import SongControlButtonsWidget

from rofile.rofile import ROMPackData, Song, SongData
from rofile.roctrl import ROCtrl

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMenuBar,
    QMenu,
    QFileDialog,
    QLabel,
    QVBoxLayout,
)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Event Editor")
        self.setWindowIcon(QIcon.fromTheme("media-floppy"))

        #self.setFixedSize(QSize(1280,720))
        self.setMinimumSize(1280,720)

        self.songtablewidget = SongTableWidget(self)

        self._create_actions_for_MB()
        self._create_menu_bar()
        self._create_main_window_layout()

    def _create_menu_bar(self):
        menuBar = self.menuBar()

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.file_initialize_rofile_action)
        fileMenu.addAction(self.file_open_rofile_action)
        fileMenu.addAction(self.file_save_rofile_action)
        
        infoMenu = QMenu("&About", self)
        menuBar.addMenu(infoMenu)
        infoMenu.addAction(self.infomenu_aboutAction)
        
        self.setMenuBar(menuBar)

    def _create_actions_for_MB(self):
        self.file_initialize_rofile_action = QAction("&Initialize RO-FILE", self)
        self.file_initialize_rofile_action.triggered.connect(self._file_func_initialize_rofile_action)

        self.file_open_rofile_action = QAction(QIcon.fromTheme("default-fileopen"), "&Open RO-FILE", self)
        self.file_open_rofile_action.triggered.connect(self._file_func_open_rofile_action)

        self.file_save_rofile_action = QAction(QIcon.fromTheme("media-floppy"), "&Save RO-FIle")
        self.file_save_rofile_action.setDisabled(True)
        self.file_save_rofile_action.triggered.connect(self._file_func_save_rofile_action)


        self.infomenu_aboutAction = QAction("&About...", self)

    def _file_func_open_rofile_action(self):
        """
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open RO-FILE")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setNameFilter("CASIO Binary Standard File(*.bin);; RO File(*.ro);; All files(*.*)")

        if file_dialog.exec():
            target_file = file_dialog.selectedFiles()
            self.msg_logger.log_message_info("Open File:\t"+target_file[0])
            ROCtrl.rodata = ROMPackData()
            status = ROCtrl.rodata.readfile(target_file[0])
            if status == 0:
                self.songtablewidget.load_elements(ROCtrl.rodata.songs)
                self.buttons.add_song_button.setDisabled(False)
                self.buttons.import_song_button.setDisabled(False)
                self.file_save_rofile_action.setDisabled(False)
            elif status == 1:
                self.msg_logger.log_message_error("Invalid HEADER")
                ROCtrl.rodata = None
            else:
                print(status)
        """

        open_rofile_file_dialog = QFileDialog(self)
        rofile_filename, _ = open_rofile_file_dialog.getOpenFileName(self, "Open RO-FILE-2", "", "CASIO Binary Standard File(*.bin);; RO File(*.ro);; All files(*.*)")
        if rofile_filename != None and rofile_filename != "":
            self.msg_logger.log_message_info("Open File:\t"+rofile_filename)
            ROCtrl.rodata = ROMPackData()
            status = ROCtrl.rodata.readfile(rofile_filename)
            if status == 0:
                self.songtablewidget.load_elements(ROCtrl.rodata.songs)
                self.buttons.add_song_button.setDisabled(False)
                self.buttons.import_song_button.setDisabled(False)
                self.file_save_rofile_action.setDisabled(False)
            elif status == 1:
                self.msg_logger.log_message_error("Invalid HEADER")
                ROCtrl.rodata = None
            else:
                print(status)
            
    
    def _file_func_initialize_rofile_action(self):
        self.msg_logger.log_message_info("new ROFile created!")
        ROCtrl.rodata = ROMPackData()
        ROCtrl.rodata.header = b'\x5A\x00\x00'
        ROCtrl.rodata.footer_address = 0
        ROCtrl.rodata.song_count = 0
        ROCtrl.rodata.endofdata = 0
        ROCtrl.rodata.endofdataplus3 = 0

        ROCtrl.rodata.songs.append(Song(0,0,0,0,SongData([bytearray(b"\x10\x00\x00"),bytearray(b"\xF0\x00\x00")],[bytearray(b"\x10\x00\x00"),bytearray(b"\xF0\x00\x00")],[bytearray(b"\x10\x00"),bytearray(b"\xF0\x00")]), 0))
        self.songtablewidget.load_elements(ROCtrl.rodata.songs)
        self.buttons.add_song_button.setDisabled(False)
        self.buttons.import_song_button.setDisabled(False)
        self.file_save_rofile_action.setDisabled(False)


    def _file_func_save_rofile_action(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getSaveFileName(self, "Save RO-File","","CASIO Binary Standard File(*.bin);;RO File(*.ro);;All files(*.*)")
        if filename:
            if not filename.lower().endswith(".bin"):
                filename += ".bin"
            self.msg_logger.log_message_info("Save File:\t"+filename)
            ROCtrl.rodata.writefile(filename)

    def _create_main_window_layout(self):

        main_layout_01 = QVBoxLayout()
        main_layout_01.addWidget(QLabel("<h2>Nenette Event Editor</h2>"))

        
        self.msg_logger = MessageLoggerBox(self)
        self.msg_logger.setFixedHeight(140)

        self.buttons = SongControlButtonsWidget()
        self.buttons.add_row_signal.connect(self._add_item_to_table)
        self.buttons.import_song_signal.connect(self._import_song)

        main_layout_01.addWidget(self.buttons)
        main_layout_01.addWidget(self.songtablewidget)
        main_layout_01.addWidget(self.msg_logger)
        
        window = QWidget()
        window.setLayout(main_layout_01)
        self.setCentralWidget(window)
        self.msg_logger.log_message_info("Nenette Event Editor. Hello!")
    
    def _add_item_to_table(self):
        new_song = Song(0,0,0,0,SongData([bytearray(b"\x10\x00\x00"),bytearray(b"\xF0\x00\x00")],[bytearray(b"\x10\x00\x00"),bytearray(b"\xF0\x00\x00")],[bytearray(b"\x10\x00"),bytearray(b"\xF0\x00")]), 0)
        ROCtrl.rodata.songs.append(new_song)
        self.songtablewidget.load_elements(ROCtrl.rodata.songs)

    def _import_song(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open RO-FILE")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setNameFilter("Song (*.bin);; All files(*.*)")

        if file_dialog.exec():
            target_file = file_dialog.selectedFiles()
            self.msg_logger.log_message_info("Song import:\t"+target_file[0])
            
            ROCtrl.rodata.loadsongpart(target_file[0])
            self.songtablewidget.load_elements(ROCtrl.rodata.songs)

app = QApplication(sys.argv)
#app.setStyle("Windows")
window = MainWindow()
window.show()

app.exec()
