import unittest
from node.domain.mikread import MikRead
from tests.fake_objects import FakeTank, FakeTemplate, FakeTemplateKeyName, FakeFieldsTemplate

nuke_shot_render_sequence = FakeTemplateKeyName(
    work="Shot_NukeRender_Work_Sequence",
    publish="Shot_NukeRender_Publish_Sequence"
)
seq = FakeTemplateKeyName("sequence_root")
shot = FakeTemplateKeyName("shot_root")
task = FakeTemplateKeyName("shot_task_root")

read1 = FakeFieldsTemplate(
    "Nuke Shot",
    nuke_shot_render_sequence,
    fields={
        "Sequence": seq,
        "Shot": shot,
        "Task": task,
    }
)

read2 = FakeFieldsTemplate(
    "Plate",
    FakeTemplate("Hiero_Footage_Sequence")
)

FAKE_CONFIGS = [
    read1,
    read2
]


class TestMikRead(unittest.TestCase):

    def setUp(self) -> None:
        self.image_path = "path/scene/path_v001.exr"
        self.image_master_path = "path/master/path_v001.exr"
        self.image_publish_path = "path/scene/path_test_publish.exr"
        self.mikread = MikRead
        self.mikread.READ_CONFIG = FAKE_CONFIGS
        self.mikread.tank_wrapper = FakeTank

    def test_resolve_template_WORK(self):
        read = self.mikread(self.image_path)
        self.assertEqual(nuke_shot_render_sequence.work, read.resolve_template(nuke_shot_render_sequence))

    def test_resolve_template_PUBLISH(self):
        read = self.mikread(self.image_publish_path)
        self.assertEqual(nuke_shot_render_sequence.publish, read.resolve_template(nuke_shot_render_sequence))

    # def test_get_template_from_path(self):
    #     read = self.mikread(self.image_path)
    #     self.assertEqual(read1, read.get_template())
    #
    # def test_get_settings(self):
    #     read = self.mikread(self.image_path)
    #     expected = {
    #         "Sequence": "sh",
    #         "name": "sh_010",
    #         "Shot": "sh_010",
    #         "Task": "cmp",
    #         "variant": "base",
    #         "write_node": "out",
    #         "version": 1,
    #         "colorspace": "acescg",
    #         "ext_render_nuke": "exr",
    #         "render_source": "nk",
    #     }
    #     self.assertEqual(expected, read.get_settings())
    #
    # def test_get_template_from_path_OTHER_PATH(self):
    #     read = self.mikread(self.image_master_path)
    #     self.assertEqual(read2, read.get_template())
    #
    # def test_get_settings_OTHER_PATH(self):
    #     read = self.mikread(self.image_master_path)
    #     expected = {
    #         "Sequence": "sh",
    #         "Shot": "sh_010",
    #         "Task": "src",
    #         "version": 1,
    #         "colorspace": "aces",
    #         "extension": "exr",
    #         "variant": "master01",
    #     }
    #     self.assertEqual(expected, read.get_settings())
    #
    # def test_get_sequences(self):
    #     read = self.mikread(self.image_path)
    #     expected = ["sh", "seq", "test"]
    #     self.assertEqual(expected, read.get_values_from_key(key="Sequence"))
