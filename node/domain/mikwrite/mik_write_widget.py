import nuke
from pprint import pprint
from PySide2 import QtWidgets, QtCore, QtGui

from node.domain import config
from node.domain.mikwrite.mik_write import MikWrite
from node.domain.model.combo_field_widget import FieldComboWidget


class MikWriteNodeWidget(QtWidgets.QWidget):
    SPACE_WIDGET_SIZE = 10

    pathChanged = QtCore.Signal()

    def __init__(self, is_out=False, path=None, node=None):
        super(self.__class__, self).__init__()

        if not node:
            node = nuke.thisNode()
        if not path:
            path = nuke.root().name()

        self.node = node
        self.path = path
        is_shot_node = True if not is_out else False
        self._combo_fields = {}

        self.mikwrite = MikWrite(self.path)
        self.mikwrite.set_element(is_shot_node)
        self.fields_scene = self.mikwrite.get_settings()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setting_layout = QtWidgets.QVBoxLayout()
        self.stackedWidgets = QtWidgets.QStackedWidget()
        self.computedPath = QtWidgets.QTextEdit()

        self.elementButton = QtWidgets.QRadioButton('Element')
        self.shotButton = QtWidgets.QRadioButton('Shot' if self.isCompShot() else 'Asset')

        self.build_ui()
        self.set_connections()
        self.update_type_source_buttons(is_out)
        self.update_write_path_widget()

    def isCompShot(self):
        return self.fields_scene.get("Shot", False)

    def build_ui(self):
        titleWidget = QtWidgets.QLabel('Write version synchronized with current comp or with an existing version')
        self.mainLayout.addWidget(titleWidget)
        self._build_head()
        self.mainLayout.addSpacing(self.SPACE_WIDGET_SIZE)
        self._build_settings()
        self.mainLayout.addSpacing(self.SPACE_WIDGET_SIZE)
        self._build_foot()
        self.setLayout(self.mainLayout)

    def makeUI(self):
        return self

    def updateValue(self):
        pass

    def set_connections(self):
        self.elementButton.pressed.connect(lambda: self.update_type_source_buttons(isShot=False))
        self.shotButton.pressed.connect(lambda: self.update_type_source_buttons(isShot=True))
        # self.elementButton.toggled.connect(self.pathChanged)
        # self.shotButton.toggled.connect(self.pathChanged)
        self.pathChanged.connect(self.update_write_path_widget)

    # CONNECTIONS

    @QtCore.Slot()
    def update_type_source_buttons(self, isShot):
        if not isShot:
            self.elementButton.setChecked(True)
        else:
            self.shotButton.setChecked(True)

        combo_element = self._combo_fields.get(config.category.tank_id)
        combo_value = 'nkelem' if not isShot else combo_element.values[0]
        combo_element.set_value(combo_value)
        self.update_write_path_widget()

    @QtCore.Slot()
    def update_write_path_widget(self):
        new_fields = {}
        self.mikwrite.set_element(self.elementButton.isChecked())
        for tank_id, combo in self._combo_fields.items():
            new_fields[tank_id] = combo.get_value()
        self.mikwrite.update_settings(new_fields)
        path = self.mikwrite.generate_path()
        self.computedPath.setText(path)

    # PRIVATES

    def _build_head(self):
        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setAlignment(QtCore.Qt.AlignHCenter)
        hlayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addSpacing(self.SPACE_WIDGET_SIZE)
        hlayout.addWidget(self.shotButton)
        hlayout.addWidget(self.elementButton)
        vlayout.addLayout(hlayout)

        self.mainLayout.addLayout(vlayout)

    def _build_settings(self):
        for key in config.WRITE_CONFIGS:
            combo = FieldComboWidget(key, self.fields_scene, self.node)
            combo.widget.activated.connect(self.pathChanged)
            self._combo_fields[key.tank_id] = combo
            self.setting_layout.addLayout(combo)
        self.mainLayout.addLayout(self.setting_layout)

    def _build_foot(self):
        self.computedPath.setReadOnly(True)
        self.computedPath.setMaximumHeight(60)
        self.mainLayout.addWidget(QtWidgets.QLabel('Computed path'))
        self.mainLayout.addWidget(self.computedPath)
        self.mainLayout.addWidget(self._read_tools())

    def _read_tools(self):
        group = QtWidgets.QGroupBox("Tools")
        hlayout = QtWidgets.QHBoxLayout()
        rvButton = QtWidgets.QPushButton('View in RV')
        fRangeFS = QtWidgets.QPushButton('Update frame range from FS')
        fRangeShotgun = QtWidgets.QPushButton('Update frame range from Shotgun')
        hlayout.addWidget(rvButton)
        hlayout.addWidget(fRangeFS)
        hlayout.addWidget(fRangeShotgun)
        group.setLayout(hlayout)
        return group

