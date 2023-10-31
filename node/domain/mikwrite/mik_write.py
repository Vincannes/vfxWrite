from pprint import pprint

import importlib
from node.adapters import tank_wrapper
importlib.reload(tank_wrapper)


from node.adapters.tank_wrapper import TankWrapper
from node.domain.ports.abs_mik import AbstractMik


class MikWrite(AbstractMik):
    tank_wrapper = TankWrapper
    RENDER_WIP_SEQUENCE = "Shot_NukeRender_Work_Sequence"
    RENDER_ELE_SEQUENCE = "Shot_Element_NukeRender_Sequence"

    def __init__(self, path=None):
        AbstractMik.__init__(self, path)

        self._build_path = None
        self._is_element = False

        self._tk = self.tank_wrapper()
        self._build_settings_from_path()

    def is_element(self):
        return self._is_element

    def get_values_from_key(self, key, fields=None):
        pass

    def generate_path(self):
        self._build_path = self._build_path_from_fields()
        return self._build_path

    def get_settings(self):
        return self._setting

    def update_settings(self, fields):
        for tank_id, value in fields.items():
            self._setting[tank_id] = value

    def resolve_template(self):
        if self._is_element:
            _template = self.RENDER_ELE_SEQUENCE
        else:
            _template = self.RENDER_WIP_SEQUENCE
        return self._tk.get_template(_template)

    def set_element(self, status=True):
        self._is_element = status

    # PRIVATES
    def _build_settings_from_path(self):
        template_name = self.resolve_template()
        template_keys = list(
            set(
                self._tk.get_template_keys(template_name)
            )
        )
        fields = self._tk.get_fields_from_path(
            self._path,
        )
        print(fields)

        for key in template_keys:
            if key not in fields.keys():
                continue
            self._setting[key] = fields.get(key)

        self._setting["SEQ"] = "%04d"

    def _build_path_from_fields(self):
        path = self._tk.build_path_from_template(
            self.resolve_template(),
            self._setting
        )
        return path
