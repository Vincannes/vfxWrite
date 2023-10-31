import nuke

from node.domain.ports.abs_mik_node import AbstractMikNode


class MikWriteNode(AbstractMikNode):
    TAB_KNOB_NAME = "mikWrite"
    GUI_WIDGET_NAME = TAB_KNOB_NAME + "UI"

    def __init__(self, out=False, inpanel=False):
        AbstractMikNode.__init__(self, nuke.createNode('Write', inpanel=inpanel))

        self.path = out
        self.module = AbstractMikNode.makeImportScript('node.domain.mikwrite.mik_write_widget')

    def create_custom_knob(self):
        path_str = "{}".format(self.path)
        return nuke.PyCustom_Knob(
            self.GUI_WIDGET_NAME,
            '',
            "{}.MikWriteNodeWidget(path='{}')".format(self.module, path_str)
        )
    def node_settings(self):
        if self.path:
            self.node.setName("out")
