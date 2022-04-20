import sys
import python_qt_binding.QtWidgets as QtWidgets
from python_qt_binding.QtCore import QMargins, Signal


class MultiplotWidget(QtWidgets.QWidget):
    _TITLE = 'Multiplot2'
    sig_sysmsg = Signal(str)
    sig_sysprogress = Signal(str)

    def __init__(self, context, node=None) -> None:
        super().__init__()
        self.setObjectName(self._TITLE)


if __name__ == "__main__":
    from rqt_gui.main import Main
    main = Main()
    sys.exit(main.main(sys.argv, standalone="rqt_multiplot2"))
