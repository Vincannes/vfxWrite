import unittest
from node.domain.mikwrite import MikWrite
from tests.fake_objects import FakeTank

"""
['Sequence', 'Shot', 'Task', 'name', 'Task', 
'variant', 'render_source', 'write_node', 
'version', 'colorspace', 'ext_render_nuke', 
'name', 'Task', 'variant', 'render_source', 
'write_node', 'version', 'colorspace', 'SEQ', 
'ext_render_nuke']
"""


class TestMikWrite(unittest.TestCase):

    def setUp(self) -> None:
        self.image_path = "path/scene/path_v001.nk"
        self.mikwrite = MikWrite
        self.mikwrite.tank_wrapper = FakeTank

    def test_create_write(self):
        write = self.mikwrite(self.image_path)
        expected = {
            "Sequence": "sh",
            "Shot": "sh_010",
            "name": "sh_010",
            "Task": "cmp",
            "version": 1,
            'SEQ': '%04d'
        }
        self.assertEqual(expected, write.get_settings())

    def test_write_is_shot(self):
        write = self.mikwrite(self.image_path)
        self.assertFalse(write.is_element())

    def test_write_is_element(self):
        write = self.mikwrite(self.image_path)
        write.set_element(True)
        self.assertTrue(write.is_element())

    def test_build_path(self):
        write = self.mikwrite(self.image_path)
        expected = "should_be"
        self.assertEqual(expected, write.generate_path())
