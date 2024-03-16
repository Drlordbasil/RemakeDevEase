from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QPushButton

class TaskList(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.layout.addWidget(self.task_input)
        
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)
        
        self.remove_button = QPushButton("Remove Task")
        self.remove_button.clicked.connect(self.remove_task)
        self.layout.addWidget(self.remove_button)
        
    def add_task(self):
        task = self.task_input.text()
        if task:
            item = QListWidgetItem(task)
            self.task_list.addItem(item)
            self.task_input.clear()
            
    def remove_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            self.task_list.takeItem(self.task_list.row(current_item))
            
    def get_tasks(self):
        tasks = []
        for i in range(self.task_list.count()):
            tasks.append(self.task_list.item(i).text())
        return tasks
    
    def clear_tasks(self):
        self.task_list.clear()
        
    def load_tasks(self, tasks):
        self.clear_tasks()
        for task in tasks:
            item = QListWidgetItem(task)
            self.task_list.addItem(item)