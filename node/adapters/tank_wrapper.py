import re
import sys

sys.path.append("D:\\Desk\\python\\Tank\\python")
import sgtk

REGEX_FRAME = r"\.(\d+)\."

class TankWrapper(object):

    def __init__(self):
        self._tk = sgtk.tank("D:/Desk/python/Projects")
        self.templates = self._tk.templates()

    def get_template(self, name):
        return self.templates[name]

    def get_template_from_path(self, path):
        try:
            path = re.sub(REGEX_FRAME, '.%04d.', path)
        except:
            pass
        path = path.replace("%04d", "####")
        return self._tk.template_from_path(path)

    def get_template_keys(self, template):
        if isinstance(template, str):
            template = self.get_template(template)
        return set(template.ordered_keys())

    def get_fields_from_path(self, path, template=None):
        if not template:
            template = self.get_template_from_path(path)
        if isinstance(template, str):
            template = self.get_template(template)
        result_string = path.replace("\\", "/")# thank you Windobe
        try:
            result_string = re.sub(REGEX_FRAME, '.%04d.', result_string)
        except:
            pass
        result_string = result_string.replace("%04d", "####")
        return template.get_fields(result_string)

    def get_abstract_path(self, template, fields):
        if isinstance(template, str):
            template = self.get_template(template)
        return self._tk.abstract_paths_from_template(template, fields)

    def build_path_from_template(self, template, fields):
        if isinstance(template, str):
            template = self.get_template(template)
        return template.apply_fields(fields)
