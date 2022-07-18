import sys
from typing import Union, Optional
from operator import add, sub, mul, truediv

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase

from design import Ui_MainWindow

operations = {
    '+': add,
    '-': sub,
    '×': mul,
    '/': truediv
}


class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("fonts/Rubic-Regular.ttf")

        # digits
        self.ui.btn_0.clicked.connect(lambda: self.add_digit('0'))
        self.ui.btn_1.clicked.connect(lambda: self.add_digit('1'))
        self.ui.btn_2.clicked.connect(lambda: self.add_digit('2'))
        self.ui.btn_3.clicked.connect(lambda: self.add_digit('3'))
        self.ui.btn_4.clicked.connect(lambda: self.add_digit('4'))
        self.ui.btn_5.clicked.connect(lambda: self.add_digit('5'))
        self.ui.btn_6.clicked.connect(lambda: self.add_digit('6'))
        self.ui.btn_7.clicked.connect(lambda: self.add_digit('7'))
        self.ui.btn_8.clicked.connect(lambda: self.add_digit('8'))
        self.ui.btn_9.clicked.connect(lambda: self.add_digit('9'))

        # actions
        self.ui.btn_C.clicked.connect(self.clear_all)
        self.ui.btn_CE.clicked.connect(self.clear_entry)
        self.ui.btn_fract.clicked.connect(self.add_point)

        # math
        self.ui.btn_rez.clicked.connect(self.calculate)
        self.ui.btn_plus.clicked.connect(lambda: self.add_temp(' + '))

    def add_digit(self, btn_text: str) -> None:
        if self.ui.lineEdit.text() == '0':
            self.ui.lineEdit.setText(btn_text)
        else:
            self.ui.lineEdit.setText(self.ui.lineEdit.text() + btn_text)

    def add_point(self) -> None:
        if '.' not in self.ui.lineEdit.text():
            self.ui.lineEdit.setText(self.ui.lineEdit.text() + '.')

    def clear_all(self) -> None:
        self.ui.lineEdit.setText('0')
        self.ui.label.clear()

    def clear_entry(self) -> None:
        self.ui.lineEdit.setText('0')

    @staticmethod
    def remove_trailing_zeros(num: str) -> str:
        n = str(float(num))
        return n[:-2] if n[-2:] == '.0' else n

    def add_temp(self, math_sign: str):
        if not self.ui.label.text():
            self.ui.label.setText(self.remove_trailing_zeros(self.ui.lineEdit.text()) +
                                  f'{math_sign}')
            self.ui.lineEdit.setText('0')

    def get_entry_num(self) -> Union[int, float]:
        entry = self.ui.lineEdit.text().strip('.')

        return float(entry) if '.' in entry else int(entry)

    def get_temp_num(self) -> Union[int, float, None]:
        if self.ui.label.text():
            temp = self.ui.label.text().strip('.').split()[0]
            return float(temp) if '.' in temp else int(temp)

    def get_math_sign(self) -> Optional[str]:
        if self.ui.label.text():
            return self.ui.label.text().strip('.').split()[-1]

    def calculate(self) -> Optional[str]:
        entry = self.ui.lineEdit.text()
        temp = self.ui.label.text()

        if temp:
            rezult = self.remove_trailing_zeros(
                str(operations[self.get_math_sign()](self.get_temp_num(),
                                                     self.get_entry_num()))
            )
            self.ui.label.setText(temp + self.remove_trailing_zeros(entry) + ' =')
            self.ui.lineEdit.setText(rezult)
            return rezult


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())
