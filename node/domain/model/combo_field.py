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

    def update_dependencies(self):
        for i, combo in self.all_combos.items():
            combo_dependents = combo.get_dependent()
            if self.key.tank_id not in combo_dependents:
                continue
            values = self.mikdata.get_values_from_key(combo.key.tank_id)
            combo.set_values(values)

    # PRIVATES
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
