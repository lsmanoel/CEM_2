#!/usr/bin/env python3.7
import sys

from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtQml import qmlRegisterType

# Register Foo and use it in QML
import Comparison
import Axes


def main():
    sys.argv += ['--style', 'Fusion']
    app = QApplication(sys.argv)

    qmlRegisterType(Comparison.Comparison, 'Comparison', 1, 0, 'Comparison')
    qmlRegisterType(Axes.PlotAxes, 'PlotAxes', 1, 0, 'PlotAxes')

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    engine = QQmlApplicationEngine('main.qml')
    engine.quit.connect(app.quit)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
