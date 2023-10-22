import unittest
from node.domain.model.combo_field import FieldCombo
from tests.fake_objects import *


class FakeMikRead(object):

    def __init__(self, path=None):
        pass

    def get_settings(self):
        return {"Shot": "sh_010", "Sequence": "sh"}

    def get_values_from_key(self, tank_id):
        if tank_id == "Sequence":
            return "sh"
        elif tank_id == "Shot":
            return "sh_010"
        elif tank_id == "Task":
            return ["cmp", "vzero"]
        elif tank_id == "version":
            return ["1", "2"]
        elif tank_id == "colorspace":
            return ["aces"]
        elif tank_id == "ext_render_nuke":
            return ["test", "exr"]


class TestFieldComboWidget(unittest.TestCase):

    def setUp(self) -> None:
        mik_read = FakeMikRead()
        self.seq_combo = FieldCombo(seq, mik_read)
        self.shot_combo = FieldCombo(shot, mik_read)
        self.task_combo = FieldCombo(task, mik_read)
        self.vers_combo = FieldCombo(version, mik_read)
        self.color_combo = FieldCombo(colorspace, mik_read)
        self.ext_combo = FieldCombo(extension, mik_read)

        all_combos = {
            "Sequence": self.seq_combo,
            "Shot": self.shot_combo,
            "Task": self.task_combo,
            "version": self.vers_combo,
            "colorspace": self.color_combo,
            "ext_render_nuke": self.ext_combo,
        }

        self.seq_combo.all_combos = all_combos
        self.shot_combo.all_combos = all_combos
        self.task_combo.all_combos = all_combos
        self.vers_combo.all_combos = all_combos
        self.color_combo.all_combos = all_combos
        self.ext_combo.all_combos = all_combos

    def test_get_shot_dependencies(self):
        expected = [
            "Sequence"
        ]
        self.assertEqual(expected, self.shot_combo.get_dependent())

    def test_get_colorspace_dependencies(self):
        expected = ['version', 'Task', 'Sequence', 'Shot']
        self.assertEqual(
            sorted(expected),
            sorted(self.color_combo.get_dependent())
        )

    def test_get_extension_dependencies(self):
        expected = ['version', 'Task', 'Sequence', 'Shot', 'colorspace']
        self.assertEqual(
            sorted(expected),
            sorted(self.ext_combo.get_dependent())
        )

    def test_update_dependencies_value(self):
        self.shot_combo.update_dependencies()
