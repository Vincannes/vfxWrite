import os
from pprint import pprint

from node.domain import config
from node.domain.mikread import MikRead
from node.domain.model.combo_field import FieldCombo
from node.adapters.tank_wrapper import TankWrapper

PROD_PATH = "D:\Desk\python\Projects\sequence"
SEQUENCE = "sh"
SHOT = "sh_010"
TASK = "cmp"
IMAGE_WIP = "image\wip"

SHOT_PATH = os.path.join(PROD_PATH, SEQUENCE, SHOT)

root_path = os.path.join(SHOT_PATH, TASK, "nuke/wip", "sh_010-cmp-base-v001.nk")
image_path = os.path.join(SHOT_PATH, TASK, IMAGE_WIP,
                          "sh_010-cmp-base-nk-out-v001-aces-exr",
                          "sh_010-cmp-base-nk-out-v001-aces.%04d.exr")
master_path = os.path.join(SHOT_PATH, "common", "footage",
                           "sh_010-src-master01-v001-aces-exr",
                           "sh_010-src-master01-v001-aces.%04d.exr")

fields = {"Shot": "sh_010", "Task": "cmp", "version": "1", "Sequence": "sh", "render_source": "nk", "SEQ": "####",
          "write_node": "out", "variant": "base", "colorspace": "aces", "name": "sh_010", "ext_render_nuke": "exr"}

master_path_2 = "D:/Desk/python/Projects/sequence/sh/sh_010/common/footage/sh_010-src-master01-v001-aces-exr/sh_010-src-master01-v001-aces.1001.exr"

tk = TankWrapper()

class FakeFieldComboWidget(object):
    VALUES = {
        "Sequence": "sh",
        "Shot": "sh_010",
        "Task": "cmp",
        "variant": "base",
        "colorspace": "aces",
        "version": "1",
        "ext_render_nuke": "ext",
    }

    def __init__(self, key, mikdata, combo_template):
        self.key = key
        self.node = None
        self.combo_template = combo_template
        self.field_combo = FieldCombo(key, mikdata)
        self.values = self.field_combo.values

    def connect_dependencies(self, combos):
        self.field_combo.all_combos = combos

    def get_value(self):
        return self.VALUES.get(self.key.tank_id)

    def set_value(self, value):
        self.VALUES[self.key.tank_id] = value

    def set_values(self, values=None):
        if self.key.tank_id == config.category.tank_id:
            pass
        if values is None:
            values = self.field_combo.get_values()
        self.values = values

        if len(values) == 0:
            pass

    def set_template(self, template_name):
        self.field_combo.set_template(template_name)


# Set MikRead for selected path
mik_read = MikRead(path=image_path)

# Get FieldKey from selected Template
all_combo_field = {}
for tank_id, field in config.tpl_nuke_shot.tokens.items():
    combo = FakeFieldComboWidget(
        key=field,
        mikdata=mik_read,
        combo_template=config.tpl_nuke_shot
    )
    combo.connect_dependencies(all_combo_field)
    all_combo_field[tank_id] = combo

# test on Task FieldKey
test_field_combo = all_combo_field.get(config.version_nuke_element.tank_id)
variant_field_combo = all_combo_field.get(config.variant_nuke_element.tank_id)
print("")
print("MikRead Settings")
pprint(mik_read.get_settings())
print("")
print("template    : ", test_field_combo.field_combo.mikdata.get_template().name)
print("dependents  : ", test_field_combo.field_combo.get_dependent())
print("values      : ", test_field_combo.field_combo.get_values())
print("")
print("Change Template to Element")
test_field_combo.set_template(config.tpl_nuke_shot_element.name)
print("template    : ", test_field_combo.field_combo.mikdata.get_template().name)
print("dependents  : ", test_field_combo.field_combo.get_dependent())
print("values      : ", test_field_combo.field_combo.get_values())
test_field_combo.VALUES["variant"] = "test"
print(f"variant changed to '{test_field_combo.VALUES.get('variant')}'")
print("values      : ", test_field_combo.field_combo.get_values())

print("variant val : ", test_field_combo.field_combo.mikdata.get_values_from_key(
    key=test_field_combo.key.tank_id,
    fields={"Sequence": "sh", "Shot": "sh_010", "Task": "cmp",
            "render_source": "nkelem", "variant": "test"})
      )

print("")
# pprint(tk.get_abstract_path("Shot_NukeRender_Work_Sequence", fields))
print(master_path_2)
print(tk.get_template_from_path(master_path_2))
