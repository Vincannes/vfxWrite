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
        if path in ["sh_010", "sh_020", "sh_030"]:
            return {"Sequence": "sh", "Shot": path}
        if path in ["/path/sequence/sh", "/path/sequence/seq", "/path/sequence/test"]:
            return {"Sequence": path.split("/")[-1]}
        if path in ["/path/task/cmp", "/path/task/vzero"]:
            return {"Sequence": "test", "Shot": "Test", "Task": path.split("/")[-1]}
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

    def get_abstract_path(self, template, fields):
        if template == "sequence_root":
            return ["/path/sequence/sh", "/path/sequence/seq", "/path/sequence/test"]
        if template == "shot_root":
            return ["sh_010", "sh_020", "sh_030"]
        if template == "shot_task_root":
            return ["/path/task/cmp", "/path/task/vzero"]


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
        self.template = template

    def get_key(self, key):
        return self.fields.get(key, None)


class FakeFieldKey(object):

    def __init__(self, tank_id, label, values=None, dependencies=None, preferencie=None, template=None):
        self.tank_id = tank_id
        self.label = label
        self.values = values
        self.template = template
        self.dependencies = dependencies
        self.preferencie = preferencie


nuke_shot_render_sequence = FakeTemplateKeyName(
    work="Shot_NukeRender_Work_Sequence",
    publish="Shot_NukeRender_Publish_Sequence"
)
seq_tpl = FakeTemplateKeyName("sequence_root")
shot_tpl = FakeTemplateKeyName("shot_root")
task_tpl = FakeTemplateKeyName("shot_task_root")
version_tpl = FakeTemplateKeyName("shot_task_root")

seq = FakeFieldKey("Sequence", "", template=seq_tpl)
shot = FakeFieldKey("Shot", "", template=shot_tpl, dependencies=["Sequence"])
task = FakeFieldKey("Task", "", template=task_tpl, dependencies=["Shot"])
version = FakeFieldKey("version", "", template=version_tpl, dependencies=["Task"])
colorspace = FakeFieldKey("colorspace", "", template=version_tpl, dependencies=["version"])
extension = FakeFieldKey("ext_render_nuke", "", template=version_tpl, dependencies=["version", "colorspace"])


read1 = FakeFieldsTemplate(
    name="Nuke Shot",
    template=nuke_shot_render_sequence,
    fields={
        "Sequence": seq,
        "Shot": shot,
        "Task": task,
    }
)

read2 = FakeFieldsTemplate(
    name="Plate",
    template=FakeTemplateKeyName("Hiero_Footage_Sequence"),
    fields={
        "Sequence": seq,
        "Shot": shot,
        "Task": task,
        "variant": task,
        "version": version,
        "colorspace": colorspace,
        "ext_render_nuke": extension,
    }
)

FAKE_CONFIGS = [
    read1,
    read2
]
