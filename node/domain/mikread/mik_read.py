from pprint import pprint

from node.domain.config import READ_CONFIGS
from node.domain.ports.abs_mik import AbstractMik
from node.adapters.tank_wrapper import TankWrapper


class MikRead(AbstractMik):
    tank_wrapper = TankWrapper
    READ_CONFIG = READ_CONFIGS

    def __init__(self, path=None):
        AbstractMik.__init__(self, path)
        self._tk = self.tank_wrapper()

        self._publish = False

        self._template = self.get_template()
        self._setting = self._generate_settings()
        self._is_publish()

    def is_publish(self):
        return self._publish

    def get_template(self):
        template = None
        path_template = self._tk.get_template_from_path(self._path)
        for read_tpl in self.READ_CONFIG:
            read_tpl_name = self.resolve_template(read_tpl)
            if path_template.name() != read_tpl_name.name:
                continue
            template = read_tpl
        return template

    def get_settings(self):
        return self._setting

    def get_values_from_key(self, key):
        template = self._template
        return self._tk.get_abstract_path(
            fields=self._setting,
            template=template.get_key(key)
        )

    def resolve_template(self, template):
        if self._publish:
            return template.publish
        return template.work

    # PRIVATES
    def _generate_settings(self):
        fields = self._tk.get_fields_from_path(
            self._path,
            self._template
        )
        return fields

    def _is_publish(self):
        self._publish = False
        if "publish" in self._template.name.lower():
            self._publish = True