from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QPushButton
from utils.data_handling import connect_to_database, create_cursor, create_tasks_table, add_task, get_tasks, mark_tasks_as_done
import sys
from PyQt5.QtCore import Qt

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

        self.conn = connect_to_database()
        self.cursor = create_cursor(self.conn)
        create_tasks_table(self.cursor)
        self.load_tasks_from_database()

    def add_task(self):
        task = self.task_input.text()
        if task:
            item = QListWidgetItem(task)
            self.task_list.addItem(item)
            self.task_input.clear()
            add_task(self.conn, task)
            self.load_tasks_from_database()
            print(f"Added task: {task}")
        else:
            print("No task entered.")

    def remove_task(self, task_text):
        items = self.task_list.findItems(task_text, Qt.MatchExactly)
        if items:
            row = self.task_list.row(items[0])
            task_id = self.task_list.item(row).data(Qt.UserRole)
            self.task_list.takeItem(row)
            mark_tasks_as_done(self.conn, self.cursor, task_id)
            print(f"Removed task: {task_text}")
            self.load_tasks_from_database()
        else:
            print(f"Task '{task_text}' not found in the task list.")

    def load_tasks_from_database(self):
        self.task_list.clear()
        tasks = get_tasks(self.cursor)
        for task_id, content in tasks:
            item = QListWidgetItem(content)
            item.setData(Qt.UserRole, task_id)
            self.task_list.addItem(item)
        print(f"Loaded {self.task_list.count()} tasks from the database.")

    def get_tasks(self):
        tasks = []
        for i in range(self.task_list.count()):
            tasks.append(self.task_list.item(i).text())
        return tasks

    def closeEvent(self, event):
        self.conn.close()
        print("TaskList widget closed. Database connection closed.")