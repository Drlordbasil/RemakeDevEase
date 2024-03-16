import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from agents.openai_agent import OpenAIAgent

def main():
    # Create the Qt application
    app = QApplication(sys.argv)

    # Create an instance of the OpenAI agent
    agent = OpenAIAgent(model="gpt-3.5-turbo", api_key="your_api_key")

    # Create the main window and pass the agent instance
    main_window = MainWindow(agent)

    # Show the main window
    main_window.show()

    # Run the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()