import sys
from PyQt5.QtWidgets import QApplication
from blessed import Terminal
from gui.browser import Browser
from gui.code_editor import CodeEditor
from gui.main_window import MainWindow
from agents.openai_agent import OpenAIAgent
from gui.task_list import TaskList

def main():
    # Create the Qt application
    app = QApplication(sys.argv)


    # Create an instance of the OpenAI agent
    agent = OpenAIAgent(Browser(), Terminal(), TaskList(), CodeEditor())

    # Create the main window and pass the agent instance
    main_window = MainWindow(agent)

    # Show the main window
    main_window.show()

    # Run the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()