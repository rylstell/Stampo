import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QPlainTextEdit, QCheckBox, QStatusBar)




class InvalidTimeFormat(Exception):
    ...



class Time:

    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __str__(self):
        if self.hours:
            return f"{self.hours}:{self.minutes:0>2}:{self.seconds:0>2}"
        elif self.minutes:
            return f"{self.minutes}:{self.seconds:0>2}"
        else:
            return f"0:{self.seconds:0>2}"

    def __add__(self, other):
        ret = Time()
        minutes, ret.seconds = divmod(self.seconds + other.seconds, 60)
        hours, ret.minutes = divmod(self.minutes + other.minutes + minutes, 60)
        ret.hours = self.hours + other.hours + hours
        return ret

    @classmethod
    def from_str(cls, strtime):
        try:
            ret = cls()
            sp = strtime.split(":")
            ret.seconds = int(sp[-1])
            if len(sp) > 1:
                ret.minutes = int(sp[-2])
            if len(sp) > 2:
                ret.hours = int(sp[-3])
            return ret
        except:
            raise InvalidTimeFormat




class Model:

    def calc_time_stamps(self, text, preserve_text):
        text = text.strip()
        time_stamps = [Time()]
        output = ""
        for line in text.split("\n"):
            line = line.strip()
            time_i = line.rfind(" ") + 1
            strtime = line[time_i:]
            time = Time.from_str(strtime)
            time += time_stamps[-1]
            time_stamps.append(time)
            time_stamp = str(time_stamps[-2])
            if preserve_text:
                time_stamp = line[:time_i] + time_stamp
            output += time_stamp + "\n"
        return output




class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.calc_btn.clicked.connect(self.calc_btn_handler)

    def start(self):
        self.view.show()

    def calc_btn_handler(self):
        text = self.view.get_input_text()
        preserve_text = self.view.get_preserve_text_state()
        try:
            output = self.model.calc_time_stamps(text, preserve_text)
        except InvalidTimeFormat:
            self.view.status_bar.showMessage("Invalid time format")
        except:
            self.view.status_bar.showMessage("An unknown error occurred")
        else:
            self.view.status_bar.clearMessage()
            self.view.set_output_text(output)




class View(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Stampo")
        self.status_bar = QStatusBar(self)

        self.central_widget = QWidget(parent=self)
        self.input_label = QLabel("Input song lengths:", parent=self.central_widget)
        self.output_label = QLabel("Output:", parent=self.central_widget)
        self.input_text = QPlainTextEdit(parent=self.central_widget)
        self.output_text = QPlainTextEdit(parent=self.central_widget)
        self.preserve_checkbox = QCheckBox("Preserve text", parent=self.central_widget)
        self.calc_btn = QPushButton("Calculate", parent=self.central_widget)

        self.output_text.setReadOnly(True)

        vlayout1 = QVBoxLayout()
        vlayout1.addWidget(self.input_label)
        vlayout1.addWidget(self.input_text)

        vlayout2 = QVBoxLayout()
        vlayout2.addWidget(self.output_label)
        vlayout2.addWidget(self.output_text)

        hlayout = QHBoxLayout()
        hlayout.addLayout(vlayout1)
        hlayout.addLayout(vlayout2)

        main_vlayout = QVBoxLayout()
        main_vlayout.addLayout(hlayout)
        main_vlayout.addWidget(self.preserve_checkbox)
        main_vlayout.addWidget(self.calc_btn)

        self.setStatusBar(self.status_bar)
        self.central_widget.setLayout(main_vlayout)
        self.setCentralWidget(self.central_widget)

    def get_input_text(self):
        return self.input_text.toPlainText()

    def get_preserve_text_state(self):
        return self.preserve_checkbox.isChecked()

    def set_output_text(self, text):
        self.output_text.setPlainText(text)
        self.output_text.repaint()





def main():
    app = QApplication(sys.argv)
    controller = Controller(Model(), View())
    controller.start()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()
