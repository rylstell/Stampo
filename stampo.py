import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QPlainTextEdit)






class Time(object):

    def __init__(self, sec=0, min=0, hour=0):
        self.sec = sec
        self.min = min
        self.hour = hour

    def __str__(self):
        if self.hour:
            ts = str(self.sec).rjust(2, "0")
            tm = str(self.min).rjust(2, "0")
            th = str(self.hour)
            return f"{th}:{tm}:{ts}"
        elif self.min:
            ts = str(self.sec).rjust(2, "0")
            tm = str(self.min)
            return f"{tm}:{ts}"
        else:
            ts = str(self.sec).rjust(2, "0")
            return f"0:{ts}"

    def __add__(self, other):
        new = Time()
        new.sec = self.sec + other.sec
        new.min = self.min + other.min
        new.hour = self.hour + other.hour
        if new.sec > 59:
            new.sec = new.sec - 60
            new.min += 1
        if new.min > 59:
            new.min = new.min - 60
            new.hour += 1
        return new

    @classmethod
    def from_str(cls, s):
        try:
            sp = s.split(":")
            new = cls()
            new.sec = int(sp[-1])
            if len(sp) > 1:
                new.min = int(sp[-2])
            if len(sp) > 2:
                new.hour = int(sp[-3])
            return new
        except:
            return None







class Model(object):

    def calc_time_stamps(self, input):
        time_stamps = [Time()]
        for line in input.split("\n"):
            time = self.extract_time(line)
            if time:
                time += time_stamps[-1]
                time_stamps.append(time)
        return "\n".join([str(t) for t in time_stamps])

    def extract_time(self, line):
        return Time.from_str(line[line.rfind(" ")+1:])







class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.connect_calc_btn(self.calc_btn_handler)

    def start(self):
        self.view.show()

    def calc_btn_handler(self):
        input = self.view.get_input_text()
        ouput = self.model.calc_time_stamps(input)
        self.view.set_output_text(ouput)








class View(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Stampo")
        self.central_widget = QWidget(parent=self)
        self.main_vlayout = QVBoxLayout(self.central_widget)
        self.hlayout = QHBoxLayout()
        self.vlayout1 = QVBoxLayout()
        self.vlayout2 = QVBoxLayout()

        self.input_label = QLabel("Input song lengths:", parent=self.central_widget)
        self.output_label = QLabel("Output:", parent=self.central_widget)

        self.input_text = QPlainTextEdit(parent=self.central_widget)

        self.output_text = QPlainTextEdit(parent=self.central_widget)
        self.output_text.setReadOnly(True)

        self.calc_btn = QPushButton("Calculate", parent=self.central_widget)

        self.vlayout1.addWidget(self.input_label)
        self.vlayout1.addWidget(self.input_text)

        self.vlayout2.addWidget(self.output_label)
        self.vlayout2.addWidget(self.output_text)

        self.hlayout.addLayout(self.vlayout1)
        self.hlayout.addLayout(self.vlayout2)

        self.main_vlayout.addLayout(self.hlayout)
        self.main_vlayout.addWidget(self.calc_btn)

        self.central_widget.setLayout(self.main_vlayout)
        self.setCentralWidget(self.central_widget)

    def connect_calc_btn(self, func):
        self.calc_btn.clicked.connect(func)

    def get_input_text(self):
        return self.input_text.toPlainText()

    def set_output_text(self, text):
        self.output_text.setPlainText(text)
        self.output_text.repaint()









def main():
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()
