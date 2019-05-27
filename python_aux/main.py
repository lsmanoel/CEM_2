#!/usr/bin/env python3.7
import sys

from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

# Register Foo and use it in QML
import Comparison
import Axes


def main():
    sys.argv += ['--style', 'Fusion']
    app = QApplication(sys.argv)

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    engine = QQmlApplicationEngine('main.qml')

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
