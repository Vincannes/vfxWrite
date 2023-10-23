import nuke

from node.domain.ports.abs_mik_node import AbstractMikNode


class MikReadNode(AbstractMikNode):
    TAB_KNOB_NAME = "mikRead"
    GUI_WIDGET_NAME = TAB_KNOB_NAME + "UI"

    def __init__(self, path, inpanel=False):
        AbstractMikNode.__init__(self, nuke.createNode('Read', inpanel=inpanel))

        self.path = path
        self.module = AbstractMikNode.makeImportScript('node.domain.mikread.mik_read_widget')

    def create_custom_knob(self):
        return nuke.PyCustom_Knob(
            self.GUI_WIDGET_NAME,
            '',
            "{}.MikReadNodeWidget(path='{}')".format(self.module, self.path)
        )

    def node_settings(self):
        pass
