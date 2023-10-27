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

    def generate_path(self):
        return self._tk.build_path_from_template(
            self.resolve_template(self._template.template),
            self._setting
        )

    def get_template(self):
        """
        Check if path template belong to READ_CONFIG
        :return: FieldsTemplate
        """
        path_template = self._tk.get_template_from_path(self._path)
        return self._get_template_from_config(path_template)

    def get_settings(self):
        return self._setting

    def get_values_from_key(self, key, fields=None):
        if fields is None:
            fields = self._setting.copy()

        match = []
        setting = {}

        # add custom token from field
        for token, value in fields.items():
            if value is None and token in setting.keys():
                setting.pop(token)
            else:
                if value is None:
                    continue
                setting[token] = self._setting[token]

        # remove key from setting because we look for this one
        if key in setting.keys():
            setting.pop(key)

        # get TemplateKeyName
        tank_template_key = self._template.get_key(key).template
        # get Tank Template name
        template = self.resolve_template(tank_template_key)

        # get all matching paths
        template_paths = self._tk.get_abstract_path(
            fields=setting,
            template=template
        )

        # filter and get matched keys from paths
        for path in template_paths:
            path_fields = self._tk.get_fields_from_path(path)
            value = path_fields.get(key)
            if value not in match:
                match.append(value)

        return match

    def is_publish(self):
        return self._publish

    def resolve_template(self, template):
        """
        :param template: [TemplateKeyName]
        :return: [str] Tank Template Name
        """
        if self._publish:
            return template.publish
        return template.work

    def set_status(self, is_publish=False):
        self._publish = is_publish

    def set_template(self, template_name):
        template = None
        for read_tpl in self.READ_CONFIG:
            if template_name != read_tpl.name:
                continue
            template = read_tpl

        if not template:
            raise ValueError("No template with name : {}".format(template_name))

        self._template = template

    def update_settings(self, fields):
        self._setting = fields

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

    def _get_template_from_config(self, tk_template):
        template = None
        for read_tpl in self.READ_CONFIG:
            if tk_template.name() == read_tpl.template.work or \
                    tk_template.name() == read_tpl.template.publish:
                template = read_tpl
                self._is_publish(tk_template)
        return template
