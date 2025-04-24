from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import QDateTime
from PyQt6.QtGui import QColor

class MessageLoggerBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.msg_logger = QTextEdit()
        self.msg_logger.setStyleSheet(''' background-color: black; ''')
        self.msg_logger.setReadOnly(True)

        __layout = QVBoxLayout()
        __layout.addWidget(self.msg_logger)
        self.setLayout(__layout)

    def log_message_info(self, message):
        self.msg_logger.setTextColor(QColor("white"))
        self.msg_logger.append("["+QDateTime.currentDateTime().toString("dd-mm-yyyy hh:mm:ss")+"]: "+str(message))

    def log_message_warning(self, message):
        self.msg_logger.setTextColor(QColor("yellow"))
        self.msg_logger.append("["+QDateTime.currentDateTime().toString("dd-mm-yyyy hh:mm:ss")+"]: "+str(message))

    def log_message_error(self, message):
        self.msg_logger.setTextColor(QColor("red"))
        self.msg_logger.append("["+QDateTime.currentDateTime().toString("dd-mm-yyyy hh:mm:ss")+"]: "+str(message))

    def log_message_success(self, message):
        self.msg_logger.setTextColor(QColor("green"))
        self.msg_logger.append("["+QDateTime.currentDateTime().toString("dd-mm-yyyy hh:mm:ss")+"]: "+str(message))