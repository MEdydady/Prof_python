from datetime import datetime

import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets

from application.salary import calculate_salary
from application.db.people import get_employees


if __name__ == "__main__":
    print(datetime.today())
    calculate_salary()
    get_employees()
