import sys
from datetime import timedelta
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel,
                             QPlainTextEdit, QCheckBox, QStatusBar)



def timedelta_from_str(strtime):
    sp = strtime.split(":")
    seconds = int(sp[-1])
    minutes = int(sp[-2]) if len(sp) > 1 else 0
    hours = int(sp[-3]) if len(sp) > 2 else 0
    t = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return t



def timedelta_to_str(td):
    s = str(td).lstrip("0").lstrip(":")
    return s[1:] if s[0] == "0" else s



def calc_time_stamps(text, preserve_text):
    # TODO: regex only accepts mm:ss and not hh:mm:ss
    new_text = []
    running_time = timedelta()
    start_i = 0
    pattern = "[0-5]?\d:[0-5]\d"
    for match in re.finditer(pattern, text):
        if preserve_text:
            new_text.append(text[start_i:match.start()])
        new_text.append(timedelta_to_str(running_time))
        td = timedelta_from_str(text[match.start():match.end()])
        running_time += td
        start_i = match.end()
    new_text.append(text[start_i:])
    return "".join(new_text) if preserve_text else "\n".join(new_text)



class View(QMainWindow):

    def __init__(self):
        super().__init__()
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
        self.calc_btn.clicked.connect(self.calc_btn_handler)

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

    def calc_btn_handler(self):
        text = self.input_text.toPlainText()
        preserve_text = self.preserve_checkbox.isChecked()
        try:
             output = calc_time_stamps(text, preserve_text)
        except:
            self.status_bar.showMessage("An unknown error occurred")
        else:
            self.status_bar.clearMessage()
            self.output_text.setPlainText(output)
            self.output_text.repaint()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec())
