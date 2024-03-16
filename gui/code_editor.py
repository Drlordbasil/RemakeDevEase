from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QToolBar, QAction, QFileDialog
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QTextDocument
import keyword
from PyQt5.QtCore import QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlightingRules = []

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("#008000"))
        keywordFormat.setFontWeight(QFont.Bold)
        self.highlightingRules.append((f"\\b({'|'.join(keyword.kwlist)})\\b", keywordFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QColor("#808080"))
        self.highlightingRules.append(("#[^\n]*", singleLineCommentFormat))

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor("#800000"))
        self.highlightingRules.append(("\".*\"", quotationFormat))
        self.highlightingRules.append(("'.*'", quotationFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            index = match.hasMatch()
            while index >= 0:
                match = expression.match(text)
                length = match.capturedLength()
                self.setFormat(index, length, format)
                match = expression.match(text, index + length)
                index = match.hasMatch()

class CodeEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.toolbar = QToolBar()
        self.layout.addWidget(self.toolbar)
        
        self.editor = QPlainTextEdit()
        font = QFont("Courier", 12)
        self.editor.setFont(font)
        self.layout.addWidget(self.editor)
        
        self.highlighter = PythonHighlighter(self.editor.document())
        
        self.new_action = QAction("New", self)
        self.new_action.triggered.connect(self.new_file)
        self.toolbar.addAction(self.new_action)
        
        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.open_file)
        self.toolbar.addAction(self.open_action)
        
        self.save_action = QAction("Save", self)
        self.save_action.triggered.connect(self.save_file)
        self.toolbar.addAction(self.save_action)
        
    def new_file(self):
        self.editor.clear()
        
    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Python Files (*.py)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, "r") as file:
                self.editor.setPlainText(file.read())
                
    def save_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Python Files (*.py)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, "w") as file:
                file.write(self.editor.toPlainText())
                
    def get_code(self):
        return self.editor.toPlainText()
    
    def set_code(self, code):
        self.editor.setPlainText(code)