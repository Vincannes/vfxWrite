from node.domain import config


class FieldCombo(object):

    def __init__(self, key, mikdata):
        self.key = key
        self.mikdata = mikdata

        self.fields = self.mikdata.get_settings()

        # default values from config
        self.values = self.key.values if self.key.values else ()
        self.preferencies = self._get_preferencies_value()
        self.all_combos = {}

    def get_dependent(self):
        return self._get_combo_all_dependent(self.key)

    def get_values(self):
        self._get_status_combo()
        new_fields = {}
        combo_dependents = self.all_combos.get(self.key.tank_id).field_combo.get_dependent()
        if not combo_dependents:
            new_fields[self.key.tank_id] = self.mikdata.get_settings().get(self.key.tank_id)
        else:
            new_fields = self._get_value_from_combo(combo_dependents)
        return self.mikdata.get_values_from_key(self.key.tank_id, new_fields)

    def update_dependencies(self):
        self._get_status_combo()
        for i, combo in self.all_combos.items():
            combo_dependents = combo.field_combo.get_dependent()
            if i in [config.category.tank_id, config.status.tank_id]:
                continue
            if not combo_dependents or self.key.tank_id not in combo_dependents:
                continue
            # get new fields with value from combo
            new_fields = self._get_value_from_combo(combo_dependents)
            values = self.mikdata.get_values_from_key(combo.key.tank_id, new_fields)
            combo.set_values(values)

    def set_template(self, template_name):
        self.mikdata.set_template(template_name)

    # PRIVATES
    def _get_status_combo(self):
        status = False
        if "status" in self.all_combos.keys():
            status = True if self.all_combos.get("status") == "publish" else False
        self.mikdata.set_status(is_publish=status)

    def _get_preferencies_value(self):
        return self.key.preferencie if self.key.preferencie else None

    def _find_field_key_by_name(self, name):
        for key, combo in self.all_combos.items():
            if key == name:
                return combo.key
        return None

    def _get_combo_all_dependent(self, key):
        all_deps = set()

        if key.dependencies is not None:
            for dep_name in key.dependencies:
                dep = self._find_field_key_by_name(dep_name)
                if dep is None:
                    continue
                all_deps.add(dep_name)
                all_deps.update(self._get_combo_all_dependent(dep))

        return list(all_deps)

    def _get_value_from_combo(self, combos_dependent):
        _fields = {}
        for i, combo in self.all_combos.items():
            if i == config.status.tank_id:
                continue
            elif i not in combos_dependent:
                value = None
            else:
                value = combo.get_value() if combo.get_value() else None
            _fields[i] = value
        return _fields
