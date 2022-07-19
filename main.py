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
        self.ui.btn_0.clicked.connect(self.add_digit)
        self.ui.btn_1.clicked.connect(self.add_digit)
        self.ui.btn_2.clicked.connect(self.add_digit)
        self.ui.btn_3.clicked.connect(self.add_digit)
        self.ui.btn_4.clicked.connect(self.add_digit)
        self.ui.btn_5.clicked.connect(self.add_digit)
        self.ui.btn_6.clicked.connect(self.add_digit)
        self.ui.btn_7.clicked.connect(self.add_digit)
        self.ui.btn_8.clicked.connect(self.add_digit)
        self.ui.btn_9.clicked.connect(self.add_digit)

        # actions
        self.ui.btn_C.clicked.connect(self.clear_all)
        self.ui.btn_CE.clicked.connect(self.clear_entry)
        self.ui.btn_fract.clicked.connect(self.add_point)

        # math
        self.ui.btn_rez.clicked.connect(self.calculate)
        self.ui.btn_plus.clicked.connect(lambda: self.math_operation(' + '))
        self.ui.btn_min.clicked.connect(lambda: self.math_operation(' - '))
        self.ui.btn_mult.clicked.connect(lambda: self.math_operation(' × '))
        self.ui.btn_div.clicked.connect(lambda: self.math_operation(' / '))

    def add_digit(self):
        btn = self.sender()

        digit_buttons = ('btn_0', 'btn_1', 'btn_2', 'btn_3', 'btn_4', 'btn_5', 'btn_6',
                         'btn_7', 'btn_8', 'btn_9')

        if btn.objectName() in digit_buttons:
            if self.ui.lineEdit.text() == '0':
                self.ui.lineEdit.setText(btn.text())
            else:
                self.ui.lineEdit.setText(self.ui.lineEdit.text() + btn.text())

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

    def add_temp(self) -> None:
        btn = self.sender()
        entry = self.remove_trailing_zeros(self.ui.lineEdit.text())

        if not self.ui.label.text() or self.get_math_sign() == '=':
            self.ui.label.setText(entry + f'{btn.text()}')
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

    def math_operation(self)->None:
        temp = self.ui.label.text()
        btn = self.sender()

        if not temp:
            self.add_temp()
        else:
            if self.get_math_sign() != math_sign:
                if self.get_math_sign() == '=':
                    self.add_temp()
                else:
                    self.ui.label.setText(temp[:-2] + f'{btn.text()}')
            else:
                self.ui.label.setText(self.calculate() + f'{btn.text()}')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())
