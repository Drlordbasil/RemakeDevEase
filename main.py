import sys
from PyQt5.QtWidgets import QApplication

from gui.main_window import MainWindow


def main():
    # Create the Qt application
    app = QApplication(sys.argv)




    # Create the main window and pass the agent instance
    main_window = MainWindow()

    # Show the main window
    main_window.show()

    # Run the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()