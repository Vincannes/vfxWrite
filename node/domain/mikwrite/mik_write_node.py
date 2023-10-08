import os

from node.domain.ports.abs_mik_node import AbstractMikNode


class MikWriteNode(AbstractMikNode):
    TAB_KNOB_NAME = "mikWrite"
    GUI_WIDGET_NAME = TAB_KNOB_NAME + "UI"

    def __init__(self, out=False, inpanel=False):
        AbstractMikNode.__init__(self, nuke.createNode('Write', inpanel=inpanel))

        self._out = out
        self.module = AbstractMikNode.makeImportScript('node.domain.mikwrite.mik_write_widget')

    def create_custom_knob(self):
        return nuke.PyCustom_Knob(
            self.GUI_WIDGET_NAME,
            '',
            "{}.MikWriteNodeWidget({})".format(self.module, self._out)
        )

    def node_settings(self):
        if self._out:
            self.node.setName("out")
