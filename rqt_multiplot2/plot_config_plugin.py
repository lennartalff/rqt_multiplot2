from python_qt_binding.QtDesigner import QPyDesignerCustomWidgetPlugin
from python_qt_binding.QtGui import QIcon
from rqt_multiplot2.plot_config import AxisScalingWidget, AxisConfigWidget


class AxisScalingPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return AxisScalingWidget(parent=parent)

    def name(self):
        return "AxisScalingWidget"

    def group(self):
        return "Multiplot Custom Widgets"

    def icon(self):
        return QIcon()

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def includeFile(self):
        return "plot_config"


class AxisConfigPlugin(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return AxisConfigWidget(parent=parent)

    def name(self):
        return "AxisConfigWidget"

    def group(self):
        return "Multiplot Custom Widgets"

    def icon(self):
        return QIcon()

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def isContainer(self):
        return False

    def includeFile(self):
        return "plot_config"
