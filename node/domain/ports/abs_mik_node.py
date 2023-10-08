import nuke
from abc import ABC, abstractmethod


class AbstractMikNode(ABC):
    TAB_KNOB_NAME = ""
    GUI_WIDGET_NAME = ""

    def __init__(self, node):
        self.node = node

    @abstractmethod
    def node_settings(self):
        pass

    @abstractmethod
    def create_custom_knob(self):
        pass

    def createNode(self):
        self.node.setName('Mik'+self.node.Class())

        tabKnob = nuke.Tab_Knob(self.TAB_KNOB_NAME)
        self.node.addKnob(tabKnob)

        mikCustomKnob = self.create_custom_knob()
        assert mikCustomKnob is not None
        self.node.addKnob(mikCustomKnob)
        self.node.addKnob(self.node['first'])
        self.node.addKnob(self.node['last'])

        self.node_settings()

        return self.node

    @staticmethod
    def makeImportScript(pyModule):
        """ Build a script string to import & use modules with __import__ function.
        This is useful in nuke knobs to avoid importing the module in the global
        python interpreter scope.

        Example:
            makeImportScript("mikIO.ui") => '__import__("mikIO.ui").ui'

        Usage:
            execScript = (makeImportScript("minuk.farm.puli.submit_ui") + ".launch_submit_dialog_within_nuke()")

        :param pyModule: <str> - module path (dotted or not)
        :return: <str> - script that can be evaluated or exec'd
        """
        importScript = "__import__('%s')" % pyModule

        modSplit = pyModule.split(".", 1)
        if len(modSplit) > 1:
            importScript = "__import__('%s').%s" % (pyModule, modSplit[1])
        return importScript