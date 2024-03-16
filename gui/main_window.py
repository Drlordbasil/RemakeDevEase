from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from gui.browser import Browser
from gui.terminal import Terminal
from gui.task_list import TaskList
from gui.code_editor import CodeEditor

class MainWindow(QMainWindow):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.setWindowTitle("AI-Assisted Development Environment")
        
        # Create the central widget and layout
        central_widget = QWidget(self)
        main_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Create the browser widget
        self.browser = Browser()
        main_layout.addWidget(self.browser)
        
        # Create the right-side layout
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)
        
        # Create the code editor widget
        self.code_editor = CodeEditor()
        right_layout.addWidget(self.code_editor)
        
        # Create the terminal widget
        self.terminal = Terminal()
        right_layout.addWidget(self.terminal)
        
        # Create the task list widget
        self.task_list = TaskList()
        right_layout.addWidget(self.task_list)
        
        # Create the input layout
        input_layout = QHBoxLayout()
        right_layout.addLayout(input_layout)
        
        # Create the user input widget
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Type your message...")
        self.user_input.returnPressed.connect(self.send_user_input)
        input_layout.addWidget(self.user_input)
        
        # Create the send button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_user_input)
        input_layout.addWidget(send_button)
        
        # Create the assistant output widget
        self.assistant_output = QTextEdit()
        self.assistant_output.setReadOnly(True)
        right_layout.addWidget(self.assistant_output)
    
    def send_user_input(self):
        user_input = self.user_input.text()
        self.user_input.clear()
        
        # Process the user input using the agent
        self.agent.process_input(user_input)
        
        # Generate the agent's response
        response = self.agent.generate_response()
        
        # Display the response in the assistant output widget
        self.assistant_output.append(f"<b>Assistant:</b> {response}")
        
        # Execute the agent's action
        self.agent.execute_action(response)