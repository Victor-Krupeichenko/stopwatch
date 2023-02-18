import time
import datetime
import sys
from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from timer_form import Ui_MainWindow


class Work(QThread):
    finish_signal = QtCore.pyqtSignal()

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def run(self):
        """Запускает таймер в отдельном потоке"""
        start_time = datetime.datetime.now()
        while True:
            current_time = datetime.datetime.now()
            elapsed_time = current_time - start_time
            hours, remainder = divmod(elapsed_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = int(elapsed_time.microseconds / 10000)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:02d}"
            self.main_window.ui.Time.setText(time_str)
            time.sleep(.1)
            if hours > 99:
                self.finish_signal.emit()


class MyTimer(QWidget):
    def __init__(self):
        super(MyTimer, self).__init__(parent=None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.ProgressThread_instance = Work(main_window=self)
        self.ui.start_btn.clicked.connect(self.starting_a_thread)
        self.ui.stop_btn.clicked.connect(self.stop_a_thread)
        self.ui.reset_btn.clicked.connect(self.reset_a_thread)
        self.ProgressThread_instance.finish_signal.connect(self.stop_a_thread)

    def starting_a_thread(self):
        """Запускаем отдельный поток"""
        self.ProgressThread_instance.start()
        self.ui.stop_btn.show()
        self.ui.reset_btn.hide()

    def stop_a_thread(self):
        """Останавливает поток"""
        self.ui.stop_btn.hide()
        self.ui.reset_btn.show()
        self.ProgressThread_instance.terminate()

    def reset_a_thread(self):
        """Сбрасывает таймер"""
        self.ui.stop_btn.show()
        self.ui.reset_btn.hide()
        time_str = '00:00:00:00'
        self.ui.Time.setText(time_str)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_prog = MyTimer()
    main_prog.show()
    sys.exit(app.exec_())
