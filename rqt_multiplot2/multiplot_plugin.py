from rqt_gui_py.plugin import Plugin
import rqt_gui.ros2_plugin_context
from rqt_py_common.plugin_container_widget import PluginContainerWidget
from rqt_multiplot2.multiplot_widget import MultiplotWidget


class MultiplotPlugin(Plugin):
    """RQt plugin to create multiple plots
    """
    def __init__(self, context: rqt_gui.ros2_plugin_context.PluginContext):
        super().__init__(context)
        self.setObjectName('MultiplotPlugin')
        self._plugin_widget = MultiplotWidget(context=context)
        self._widget = PluginContainerWidget(self._plugin_widget,
                                             on_sysprogress_bar=False)
        context.add_widget(self._widget)
        if context.serial_number() > 0:
            self._widget.setWindowTitle(f'{self._widget.windowTitle()}'
                                        f'{context.serial_number()}')

    def shutdown_plugin(self):
        return super().shutdown_plugin()

    def save_settings(self, plugin_settings, instance_settings):
        return super().save_settings(plugin_settings, instance_settings)

    def restore_settings(self, plugin_settings, instance_settings):
        return super().restore_settings(plugin_settings, instance_settings)
