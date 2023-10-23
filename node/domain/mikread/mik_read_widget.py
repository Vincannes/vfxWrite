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
        self._build_settings()
        self.mainLayout.addSpacing(self.SPACE_WIDGET_SIZE)
        self._build_foot()
        self.setLayout(self.mainLayout)

    def makeUI(self):
        return self

    def updateValue(self):
        pass

    def set_connections(self):
        self.source_combo.currentIndexChanged.connect(self.update_setting_fields)
        self.pathChanged.connect(self.update_write_path_widget)

    # CONNECTIONS

    @QtCore.Slot()
    def update_write_path_widget(self):
        new_fields = {}
        for tank_id, combo in self._combo_fields.items():
            new_fields[tank_id] = combo.get_value()
        pprint(new_fields)
        # self.mikwrite.update_settings(new_fields)
        # path = self.mikread.generate_path()
        # self.computedPath.setText(path)

    @QtCore.Slot(object)
    def update_combo_widget(self, index, combo_box):
        combo_box.field_combo.update_dependencies()

    @QtCore.Slot(int)
    def update_setting_fields(self, index):
        template = self.source_combo.itemData(index)
        # print(template)
        self._clear_layout(self.setting_layout)
        self._build_settings()

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
        self._build_source_combo()

    def _build_source_combo(self):
        for key in config.READ_CONFIGS:
            self.source_combo.addItem(key.name, key)

    def _build_settings(self):
        template_fields = self.source_combo.currentData()
        for key_name, key in template_fields.tokens.items():
            combo = FieldComboWidget(key, self.mikread, self.node, True)
            combo.widget.activated.connect(
                lambda index, cb=combo: self.update_combo_widget(index, cb)
            )
            # combo.
            self._combo_fields[key.tank_id] = combo
            self.setting_layout.addLayout(combo)
        self.mainLayout.addLayout(self.setting_layout)

        for combo in self._combo_fields.values():
            combo.connect_dependencies(self._combo_fields)

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

    def _clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child is not None:
                child.combo_widget.deleteLater()
                child.label_widget.deleteLater()
            elif child.layout() is not None:
                self._clear_layout(child.layout())
