#!/usr/bin/env python3
"""
DailyRoutine - Habit Tracker Application
Main entry point
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication

from config.constants import APP_NAME, APP_VERSION
from ui.main_window import MainWindow

# Set up basic logging to print to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - DailyRoutine - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    """Main function to run the application."""
    logging.info(f"Starting {APP_NAME} v{APP_VERSION}")

    app = QApplication(sys.argv)

    try:
        main_win = MainWindow()
        main_win.show()
        logging.info("Application started successfully.")
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
