import re
import os
import sys

# sys.path.append("D:\\Desk\\python\\Tank\\python")
import sgtk
if sys.platform == "linux":
    from tank_vendor.shotgun_authentication import ShotgunAuthenticator  

REGEX_FRAME = r"\.(\d+)\."


class TankWrapper(object):

    def __init__(self):
        prod_root = "D:/Desk/python/Projects"
        if sys.platform == "linux":
            user = ShotgunAuthenticator(sgtk.util.CoreDefaultsManager()).create_script_user('Toolkit',os.environ.get('SHOTGUN_API_KEY'),)         
            sgtk.set_authenticated_user(user)
            self._tk = sgtk.sgtk_from_path(os.environ.get("PROD_ROOT"))
            self.templates = self._tk.templates
        else:
            self._tk = sgtk.tank(prod_root)
            self.templates = self._tk.templates()

    def get_template(self, name):
        return self.templates[name]

    def get_template_from_path(self, path):
        if sys.platform == "windows":
            try:
                path = re.sub(REGEX_FRAME, '.%04d.', path)
            except Exception as e:
                print(e)
                pass
            path = path.replace("%04d", "####")
            path = path.replace("\\", "/")  # thank you Windobe
        return self._tk.template_from_path(path)

    def get_template_keys(self, template):
        if isinstance(template, str):
            template = self.get_template(template)
        if sys.platform == "linux":
            ordered_keys = template.ordered_keys
        else:
            ordered_keys = template.ordered_keys()
        return set(ordered_keys)

    def get_fields_from_path(self, path, template=None):
        if not template:
            template = self.get_template_from_path(path)
        if isinstance(template, str):
            template = self.get_template(template)
        result_string = path
        if sys.platform == "windows":
            result_string = path.replace("\\", "/")  # thank you Windobe
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
