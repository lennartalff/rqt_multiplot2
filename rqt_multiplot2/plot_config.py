import os

from PyQt5 import QtWidgets
# from python_qt_binding import QtWidgets
from PyQt5 import QtCore
# import python_qt_binding.QtCore
from PyQt5 import QtGui
# from python_qt_binding import QtGui
from PyQt5.uic import loadUi
# from python_qt_binding import loadUi
from ament_index_python import get_resource


class AxisScalingWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        _, pkg_path = get_resource('packages', 'rqt_multiplot2')
        ui_file = os.path.join(pkg_path, 'share', 'rqt_multiplot2', 'resource',
                               'axis_scaling.ui')
        self.ui = loadUi(ui_file, self)

        # self.ui.min_edit.setValidator(QtGui.QDoubleValidator(self))
        self.ui.min_edit.editingFinished.connect(self.min_edit_finished)
        # self.ui.max_edit.setValidator(QtGui.QDoubleValidator(self))
        self.ui.max_edit.editingFinished.connect(self.max_edit_finished)

    @QtCore.pyqtSlot()
    def min_edit_finished(self):
        try:
            val = float(self.ui.min_edit.text())
        except ValueError:
            val = 0
            self.ui.min_edit.setText(f'{val}')
        # TODO: save the value in our config

    @QtCore.pyqtSlot()
    def max_edit_finished(self):
        try:
            val = float(self.ui.max_edit.text())
        except ValueError:
            val = 0
            self.ui.max_edit.setText(f'{val}')
        # TODO: save the value in our config


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = AxisScalingWidget()
    w.show()
    app.exec()
