import sys

from rqt_gui.main import Main
from rqt_multiplot2.multiplot_plugin import MultiplotPlugin


def main(argv=sys.argv):
    plugin = 'rqt_reconfigure.param_plugin.ParamPlugin'
    main = Main(filename=plugin)
    sys.exit(main.main(argv, standalone=plugin))


if __name__ == '__main__':
    main()
