class FakeTemplate(object):
    def __init__(self, name=""):
        self._name = name

    def name(self):
        return self._name


class FakeTank(object):

    def __init__(self):
        pass

    def get_template(self, template):
        return FakeTemplate(template)

    def get_fields_from_path(self, path, template=None):
        fields_1 = {
            "Sequence": "sh",
            "name": "sh_010",
            "Shot": "sh_010",
            "Task": "cmp",
            "variant": "base",
            "write_node": "out",
            "version": 1,
            "colorspace": "acescg",
            "ext_render_nuke": "exr",
            "render_source": "nk",
        }
        fields_2 = {
            "Sequence": "sh",
            "name": "sh_010",
            "Shot": "sh_010",
            "Task": "cmp",
            "version": 1,
        }
        fields_3 = {
            "Sequence": "sh",
            "Shot": "sh_010",
            "Task": "src",
            "version": 1,
            "colorspace": "aces",
            "extension": "exr",
            "variant": "master01",
        }
        fields_4 = {
            "Sequence": "sh",
            "Shot": "sh_010",
            "Task": "cmp",
            "version": 1,
            "variant": "base",
        }
        if path in ["path/scene/path_v001.exr", "path/scene/path_test_publish.exr"]:
            return fields_1
        if path == "path/master/path_v001.exr":
            return fields_3
        if path == "path/scene/root.nk":
            return fields_4
        else:
            return fields_2

    def get_template_from_path(self, path):
        if path == "path/scene/path_v001.exr":
            template = FakeTemplate("Shot_NukeRender_Work_Sequence")
        elif path == "path/scene/path_test_publish.exr":
            template = FakeTemplate("Shot_NukeRender_Publish_Sequence")
        elif path == "path/master/path_v001.exr":
            template = FakeTemplate("Hiero_Footage_Sequence")
        else:
            template = FakeTemplate("Name_Work_Test")
        return template

    def build_path_from_template(self, template, fields):
        return "should_be"

    def get_template_keys(self, template):
        return ['Sequence', 'Shot', 'Task', 'name', 'Task', 'variant', 'render_source', 'write_node', 'version',
                'colorspace', 'ext_render_nuke', 'name', 'Task', 'variant', 'render_source', 'write_node', 'version',
                'colorspace', 'SEQ', 'ext_render_nuke']


class FakeTemplateKeyName(object):
    NAME_PUBLISH = 'publish'
    NAME_WORK = 'work'

    def __init__(self, defaultTemplate='', work='', publish=''):
        if not defaultTemplate and (not work or not publish):
            raise ValueError("TemplateKeyName invalid argument constructor: empty")
        self.work = defaultTemplate or work
        self.publish = defaultTemplate or publish


class FakeFieldsTemplate(object):

    def __init__(self, name, template, fields={}):
        self.name = name
        self.fields = fields
        self.tank_tpl = template

    def get_key(self, key):
        return self.fields.get(key, None)


class FakeFieldKey(object):

    def __init__(self, tank_id, label, values=None, preferencie=None):
        self.tank_id = tank_id
        self.label = label
        self.values = values
        self.preferencie = preferencie
