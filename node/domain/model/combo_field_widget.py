from PySide2 import QtWidgets, QtCore, QtGui

from node.domain import config
from node.domain.model.combo_field import FieldCombo


class FieldComboWidget(QtWidgets.QHBoxLayout):
    WRITE_KEYS_EDITABLE = [
        config.category,
        config.colorspace,
        config.extension
    ]

    def __init__(self, key, mikdata, node, is_editable=False):
        super(self.__class__, self).__init__()

        self.key = key
        self.node = node

        self.field_combo = FieldCombo(key, mikdata)
        self.values = self.field_combo.values

        self.combo_widget = QtWidgets.QComboBox()
        self.label_widget = QtWidgets.QLabel(self.key.label)

        self.label_widget.setMaximumWidth(100)
        if not is_editable and key not in self.WRITE_KEYS_EDITABLE:
            self.combo.setEnabled(False)

        self.addWidget(self.label_widget)
        self.addWidget(self.combo_widget)

        self.set_default_value()
        self.set_values()
        self.set_value()

    @property
    def widget(self):
        return self.combo_widget

    @property
    def dependent(self):
        return self.field_combo.get_dependent()

    def connect_dependencies(self, combos):
        self.field_combo.all_combos = combos

    def set_default_value(self):
        """
        :return:
        """
        if self.key.tank_id == "write_node":
            self.combo_widget.addItems([self.node.name()])
            pass

        # set defaults values
        if not self.values:
            return
        self.combo_widget.addItems(self.field_combo.values)

        # set preferencies
        preferencies_value = self.field_combo.preferencies
        if preferencies_value:
            self.combo_widget.setCurrentIndex(self.values.index(preferencies_value))

    def set_value(self, value=None):
        """
        :return:
        """
        if not value:
            value = self.field_combo.fields.get(self.key.tank_id, None)

        # if value in config FieldKey.values
        if value in self.values:
            self.combo_widget.setCurrentIndex(self.values.index(value))
        # if value already in Combobox
        elif value in [self.combo_widget.itemText(i) for i in range(self.combo_widget.count())]:
            self.values = self.values + (value,)
            self.combo_widget.setCurrentIndex(self.values.index(value))
        # if not in Combobox and not in config FieldKey.values
        elif value is not None:
            self.combo_widget.addItems([value])

    def set_values(self, values=None):
        if values is None:
            values = self.field_combo.get_values()
        self.values = values
        self.combo_widget.clear()
        if len(values) == 0:
            pass
        self.combo_widget.addItems(values)

    def get_value(self):
        """
        :return:
        """
        return str(self.combo_widget.currentText())

