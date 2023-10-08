from PySide2 import QtWidgets, QtCore, QtGui

from node.domain import config


class FieldComboWidget(QtWidgets.QHBoxLayout):
    KEYS_EDITABLE = [config.category, config.colorspace, config.extension]

    def __init__(self, key, fields, node):
        super(self.__class__, self).__init__()

        self.key = key
        self.node = node
        self.fields = fields

        # default values from config
        self.values = self.key.values if self.key.values else ()

        self.combo = QtWidgets.QComboBox()
        label = QtWidgets.QLabel(self.key.label)

        label.setMaximumWidth(100)
        if key not in self.KEYS_EDITABLE:
            self.combo.setEnabled(False)

        self.addWidget(label)
        self.addWidget(self.combo)

        self.set_default_value()
        self.set_value()

    @property
    def widget(self):
        return self.combo

    def set_default_value(self):

        if self.key.tank_id == "write_node":
            self.combo.addItems([self.node.name()])
            pass

        # set defaults values
        self.combo.addItems(self.values)

        # set preferencies
        preferencies_value = self.key.preferencie if self.key.preferencie else None
        if preferencies_value:
            self.combo.setCurrentIndex(self.values.index(preferencies_value))

    def set_value(self, value=None):
        if not value:
            value = self.fields.get(self.key.tank_id, None)

        if value in self.values:
            self.combo.setCurrentIndex(self.values.index(value))
        elif value in [self.combo.itemText(i) for i in range(self.combo.count())]:
            self.values + (value,)
            self.combo.setCurrentIndex(self.values.index(value))
        elif value is not None:
            self.combo.addItems([value])

    def get_value(self):
        return str(self.combo.currentText())
