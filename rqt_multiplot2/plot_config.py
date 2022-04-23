import enum
import os

# from python_qt_binding import loadUi
from ament_index_python import get_resource
# import python_qt_binding.QtCore
# from python_qt_binding import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
# from python_qt_binding import QtGui
from PyQt5.uic import loadUi


class Config(QtCore.QObject):
    """Base class for configurations"""
    changed = QtCore.pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)


class AxisScalingConfig(Config):
    """Object to hold the scaling configuration of an axis."""
    class ScalingType(enum.Enum):
        """Defines the different scaling types for an axis."""
        AUTO = enum.auto()
        ABSOLUTE = enum.auto()
        RELATIVE = enum.auto()

        def __str__(self):
            return f'{self.name.lower()}'

    scaling_type_changed = QtCore.pyqtSignal(object)
    lower_limit_changed = QtCore.pyqtSignal(float)
    upper_limit_changed = QtCore.pyqtSignal(float)

    _scaling_type: ScalingType

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._scaling_type = self.ScalingType.AUTO
        self._upper_limit = 10
        self._lower_limit = 0

    @QtCore.pyqtSlot(object)
    def set_scaling_type(self, scaling_type):
        """Set the scaling type.

        Args:
            scaling_type (AxisScalingConfig.ScalingType): Type of the scaling.
        """
        if isinstance(scaling_type, self.ScalingType):
            self._scaling_type = scaling_type
            self.scaling_type_changed.emit(self._scaling_type)
            self.changed.emit()

    @QtCore.pyqtSlot()
    def get_scaling_type(self):
        """Get the scaling type of an axis.

        Returns:
            AxisScalingConfig.ScalingType: Returns the scaling type.
        """
        return self._scaling_type

    @QtCore.pyqtSlot(float)
    def set_lower_limit(self, lower_limit: float):
        """Sets the lower limit of the axis.

        Args:
            lower_limit (float): Value of the lower limit.
        """
        self._lower_limit = lower_limit
        self.lower_limit_changed.emit(self._lower_limit)
        self.changed.emit()

    @QtCore.pyqtSlot()
    def get_lower_limit(self):
        """Gets the lower limit of the axis.

        Returns:
            float: Lower limit of the axis
        """
        return self._lower_limit

    @QtCore.pyqtSlot(float)
    def set_upper_limit(self, upper_limit: float):
        """Sets the upper limit of the axis.

        Args:
            lower_limit (float): Value of the lower limit.
        """
        self._upper_limit = upper_limit
        self.upper_limit_changed.emit(self._upper_limit)
        self.changed.emit()

    @QtCore.pyqtSlot()
    def get_upper_limit(self):
        """Gets the upper limit of the axis.

        Returns:
            float: Lower limit of the axis
        """
        return self._upper_limit

    def is_valid(self):
        """Checks if the scaling configuration is valid.

        Returns:
            Boolean: Return true iff scaling configuration for the axis is valid
        """
        if self._scaling_type is self.ScalingType.AUTO:
            return True
        else:
            if self._lower_limit < self._upper_limit:
                return True
        return False


class AxisConfig(Config):
    """Configuration of an axis."""
    axis_label_changed = QtCore.pyqtSignal(str)
    reverse_changed = QtCore.pyqtSignal(bool)
    relative_time_changed = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._axis_label = "Label"
        self._reverse = False
        self._relative_time = False

    @QtCore.pyqtSlot(str)
    def set_axis_label(self, label: str):
        """Set the label of the axis.

        Args:
            label (str): The axis' label.
        """
        self._axis_label = label
        self.axis_label_changed.emit(self._axis_label)
        self.changed.emit()

    @QtCore.pyqtSlot()
    def get_axis_label(self):
        """Get the label of the axis.

        Returns:
            str: Label of the axis.
        """
        return self._axis_label

    @QtCore.pyqtSlot(bool)
    def set_reverse(self, checked: bool):
        """Set the reverse axis configuration value.

        Args:
            checked (bool): True iff axis should be reversed.
        """
        self._reverse = checked
        self.reverse_changed.emit(self._reverse)
        self.changed.emit()

    @QtCore.pyqtSlot()
    def get_reverse(self):
        """Get the reverse axis configuration value.

        Returns:
            bool: True iff axis is reversed.
        """
        return self._reverse

    @QtCore.pyqtSlot(bool)
    def set_relative_time(self, checked: bool):
        """Set the relative time configuration value.

        Args:
            checked (bool): True iff relative time is to be used.
        """
        self._relative_time = checked
        self.relative_time_changed.emit(self._relative_time)
        self.changed.emit()

    @QtCore.pyqtSlot()
    def get_relative_time(self):
        """Get the relative time configuration value.

        Returns:
            bool: True iff relative time is used.
        """
        return self._relative_time


class AxisScalingWidget(QtWidgets.QWidget):
    """Widget to configure the axis scaling."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._config: AxisScalingConfig = None
        _, pkg_path = get_resource('packages', 'rqt_multiplot2')
        ui_file = os.path.join(pkg_path, 'share', 'rqt_multiplot2', 'resource',
                               'axis_scaling.ui')
        self.ui = loadUi(ui_file, self)
        self.set_config(AxisScalingConfig(self))

        validator = QtGui.QDoubleValidator(self)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.ui.min_edit.setValidator(validator)
        self.ui.min_edit.editingFinished.connect(self._min_edit_finished)

        validator = QtGui.QDoubleValidator(self)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.ui.max_edit.setValidator(validator)
        self.ui.max_edit.editingFinished.connect(self._max_edit_finished)
        self._init_type_combobox()

        self.ui.type_combobox.currentTextChanged.connect(
            self._type_combobox_changed)

    @QtCore.pyqtSlot(object)
    def set_config(self, config: AxisScalingConfig):
        """Set a new configuration for the axis.

        Args:
            config (AxisScalingConfig): The new configuration.
        """
        if self._config is config:
            return
        if isinstance(self._config, AxisScalingConfig):
            self._config.deleteLater()
        self._config = config
        self._config.scaling_type_changed.connect(self._config_type_changed)
        self._config.lower_limit_changed.connect(
            self._config_lower_limit_changed)
        self._config.upper_limit_changed.connect(
            self._config_upper_limit_changed)

    @QtCore.pyqtSlot()
    def get_config(self):
        return self._config

    def _select_type_combobox_item(self, value: AxisScalingConfig.ScalingType):
        index = self.ui.type_combobox.findText(str(value))
        if index < 0:
            return False
        self.ui.type_combobox.setCurrentIndex(index)
        return True

    def _init_type_combobox(self):
        self.ui.type_combobox.clear()
        items = []
        for scaling_type in AxisScalingConfig.ScalingType:
            items.append(str(scaling_type))
        self.ui.type_combobox.addItems(items)
        self._select_type_combobox_item(self._config.get_scaling_type())

    @QtCore.pyqtSlot(object)
    def _config_type_changed(self, value: AxisScalingConfig.ScalingType):
        self._select_type_combobox_item(value)

    @QtCore.pyqtSlot(float)
    def _config_upper_limit_changed(self, value: float):
        self.ui.max_edit.setText(f'{value}')

    @QtCore.pyqtSlot(float)
    def _config_lower_limit_changed(self, value: float):
        self.ui.min_edit.setText(f'{value}')

    @QtCore.pyqtSlot()
    def _min_edit_finished(self):
        try:
            val = float(self.ui.min_edit.text())
        except ValueError:
            val = 0.0
            self.ui.min_edit.setText(f'{val}')
        self._config.set_lower_limit(val)

    @QtCore.pyqtSlot()
    def _max_edit_finished(self):
        try:
            val = float(self.ui.max_edit.text())
        except ValueError:
            val = 0.0
            self.ui.max_edit.setText(f'{val}')
        self._config.set_upper_limit(val)

    @QtCore.pyqtSlot(str)
    def _type_combobox_changed(self, text: str):
        for scaling_type in AxisScalingConfig.ScalingType:
            if str(scaling_type) == text:
                self._config.set_scaling_type(scaling_type)


class AxisConfigWidget(QtWidgets.QWidget):
    """Widget to configure an axis of a plot."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        _, pkg_path = get_resource('packages', 'rqt_multiplot2')
        ui_file = os.path.join(pkg_path, 'share', 'rqt_multiplot2', 'resource',
                               'axis_config_widget.ui')
        self.ui = loadUi(ui_file, self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = AxisConfigWidget()
    w.show()
    app.exec()
