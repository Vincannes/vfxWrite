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

    def is_publish(self):
        return self._publish

    def get_template(self):
        """
        Check if path template belong to READ_CONFIG
        :return: FieldsTemplate
        """
        template = None
        path_template = self._tk.get_template_from_path(self._path)

        for read_tpl in self.READ_CONFIG:
            if path_template.name() == read_tpl.template.work or \
                    path_template.name() == read_tpl.template.publish:
                template = read_tpl
                self._is_publish(path_template)
        return template

    def get_settings(self):
        return self._setting

    def get_values_from_key(self, key, fields=None):
        if fields is None:
            fields = {}
        match = []
        setting = self._setting.copy()

        # add custom token from field
        for token, value in fields.items():
            if value is None:
                setting.pop(token)
            else:
                setting[token] = value

        # remove key from setting because we look for this one
        if key in setting.keys():
            setting.pop(key)

        # get FieldsTemplate name
        tank_template_name = self._template.get_key(key).template
        # get TemplateKeyName
        template = self.resolve_template(tank_template_name)
        # get all matching paths
        template_paths = self._tk.get_abstract_path(
            fields=setting,
            template=template
        )

        # filter and get matched keys from paths
        for path in template_paths:
            fields = self._tk.get_fields_from_path(path)
            value = fields.get(key)
            if value not in match:
                match.append(value)

        return match

    def resolve_template(self, template):
        """
        :param template: [TemplateKeyName]
        :return: [str] Tank Template Name
        """
        if self._publish:
            return template.publish
        return template.work

    # PRIVATES
    def _generate_settings(self):
        fields = self._tk.get_fields_from_path(
            self._path,
            self.resolve_template(self._template.template)
        )
        return fields

    def _is_publish(self, template):
        self._publish = False
        if "publish" in template.name().lower():
            self._publish = True
