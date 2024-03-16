from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit
import subprocess

class Terminal(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.output_view = QTextEdit()
        self.output_view.setReadOnly(True)
        self.layout.addWidget(self.output_view)
        
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.execute_command)
        self.layout.addWidget(self.input_field)
        
    def execute_command(self):
        command = self.input_field.text()
        self.input_field.clear()
        
        try:
            output = subprocess.check_output(command, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
            self.output_view.append(f">>> {command}\n{output}")
        except subprocess.CalledProcessError as e:
            self.output_view.append(f">>> {command}\n{e.output}")
        
    def clear_output(self):
        self.output_view.clear()
        
    def set_font_size(self, size):
        font = self.output_view.font()
        font.setPointSize(size)
        self.output_view.setFont(font)
        self.input_field.setFont(font)
        
    def set_background_color(self, color):
        self.output_view.setStyleSheet(f"background-color: {color};")
        self.input_field.setStyleSheet(f"background-color: {color};")
        
    def set_text_color(self, color):
        self.output_view.setStyleSheet(f"color: {color};")
        self.input_field.setStyleSheet(f"color: {color};")