from PySide2 import QtWidgets, QtCore, QtGui

from node.domain import config
from node.domain.model.combo_field import FieldCombo


class FieldComboWidget(QtWidgets.QHBoxLayout):
    WRITE_KEYS_EDITABLE = [
        config.category,
        config.colorspace,
        config.extension,
    ]

    READ_KEYS_NOTEDITABLE = [
    ]

    def __init__(self, key, mikdata, node, combo_template, is_editable=False):
        super(self.__class__, self).__init__()

        self.key = key
        self.node = node
        self.combo_template = combo_template

        self.field_combo = FieldCombo(key, mikdata)
        self.values = self.field_combo.values

        self.combo_widget = QtWidgets.QComboBox()
        self.label_widget = QtWidgets.QLabel(self.key.label)

        self.label_widget.setMaximumWidth(100)
        if not is_editable and key not in self.WRITE_KEYS_EDITABLE or key in self.READ_KEYS_NOTEDITABLE:
            self.combo_widget.setEnabled(False)

        self.addWidget(self.label_widget)
        self.addWidget(self.combo_widget)

    @property
    def widget(self):
        return self.combo_widget

    @property
    def dependent(self):
        return self.field_combo.get_dependent()

    def initialize(self):
        self.set_default_value()
        self.set_template(self.combo_template.name)

        if self.key.tank_id not in [config.category.tank_id, config.status.tank_id]:
            self.set_values()

    def connect_dependencies(self, combos):
        self.field_combo.all_combos = combos

    def set_template(self, template_name):
        self.field_combo.set_template(template_name)

    def get_value(self):
        """
        :return:
        """
        return str(self.combo_widget.currentText())

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
        elif value not in self.values:
            return
        elif value in [self.combo_widget.itemText(i) for i in range(self.combo_widget.count())]:
            self.values = self.values + (value,)
            self.combo_widget.setCurrentIndex(self.values.index(value))
        # if not in Combobox and not in config FieldKey.values
        elif value is not None:
            self.combo_widget.addItems([value])

    def set_values(self, values=None):
        if self.key.tank_id == config.category.tank_id:
            return
        if values is None:
            values = self.field_combo.get_values()

        self.values = values
        self.combo_widget.clear()

        if len(values) == 0:
            return
        self.combo_widget.addItems(values)
        self.set_value()
