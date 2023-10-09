import nuke
from pprint import pprint
from PySide2 import QtWidgets, QtCore, QtGui

from node.domain import config
from node.domain.mikread import MikRead
from node.domain.model.combo_field_widget import FieldComboWidget


class MikReadNodeWidget(QtWidgets.QWidget):
    SPACE_WIDGET_SIZE = 10

    pathChanged = QtCore.Signal()

    def __init__(self, path=None, node=None):
        super(self.__class__, self).__init__()

        if not node:
            node = nuke.thisNode()
        if not path:
            path = nuke.root().name()

        self.node = node
        self.path = path

        self._combo_fields = {}

        self.mikread = MikRead(self.path)
        self.fields_scene = self.mikread.get_settings()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setting_layout = QtWidgets.QVBoxLayout()
        self.stackedWidgets = QtWidgets.QStackedWidget()
        self.computedPath = QtWidgets.QTextEdit()

        self.source_combo = QtWidgets.QComboBox()
        self.refresh_button = QtWidgets.QPushButton("Refresh")

        self.build_ui()
        self.set_connections()
        # self.update_type_source_buttons(is_out)
        # self.update_write_path_widget()

    def isCompShot(self):
        return self.fields_scene.get("Shot", False)

    def build_ui(self):
        titleWidget = QtWidgets.QLabel("Browse disk with filters")
        self.mainLayout.addWidget(titleWidget)
        self._build_head()
        self.mainLayout.addSpacing(self.SPACE_WIDGET_SIZE)
        # self._build_settings()
        self.mainLayout.addSpacing(self.SPACE_WIDGET_SIZE)
        self._build_foot()
        self.setLayout(self.mainLayout)

    def makeUI(self):
        return self

    def updateValue(self):
        pass

    def set_connections(self):
        self.pathChanged.connect(self.update_write_path_widget)

    # CONNECTIONS

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
        label = QtWidgets.QLabel("Source")
        hlayout.addWidget(label)
        hlayout.addWidget(self.source_combo)
        vlayout.addLayout(hlayout)
        vlayout.addSpacing(self.SPACE_WIDGET_SIZE)
        vlayout.addWidget(self.refresh_button)
        self.mainLayout.addLayout(vlayout)

    def _build_settings(self):
        for key in config.READ_CONFIGS:
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

