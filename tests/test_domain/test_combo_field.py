import unittest
from node.domain.model.combo_field import FieldCombo
from tests.fake_objects import *


class TestFieldComboWidget(unittest.TestCase):

    def setUp(self) -> None:
        mik_read = FakeMikRead()

        self.seq_combo = FieldCombo(seq, mik_read)
        self.shot_combo = FieldCombo(shot, mik_read)
        self.task_combo = FieldCombo(task, mik_read)
        self.vers_combo = FieldCombo(version, mik_read)
        self.color_combo = FieldCombo(colorspace, mik_read)
        self.ext_combo = FieldCombo(extension, mik_read)

        seqWidget = FakeFieldComboWidget(seq)
        seqWidget.field_combo = self.seq_combo
        shotWidget = FakeFieldComboWidget(shot)
        shotWidget.field_combo = self.shot_combo
        taskWidget = FakeFieldComboWidget(task)
        taskWidget.field_combo = self.task_combo
        versionWidget = FakeFieldComboWidget(version)
        versionWidget.field_combo = self.vers_combo
        colorWidget = FakeFieldComboWidget(colorspace)
        colorWidget.field_combo = self.color_combo
        extWidget = FakeFieldComboWidget(extension)
        extWidget.field_combo = self.ext_combo

        all_combos = {
            "Sequence": seqWidget,
            "Shot": shotWidget,
            "Task": taskWidget,
            "version": versionWidget,
            "colorspace": colorWidget,
            "ext_render_nuke": extWidget,
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
