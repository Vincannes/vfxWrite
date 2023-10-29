"""
Tank Templates config.

tank - templates.yml contains intermediate templates such as Generic_Name i.e Sequence folders.
This is done in order to speed up the path searching request. This is represented by template_folder in this file.
"""

from node.domain.config.fields import *
from node.domain.config.models import FieldsTemplate, FieldKey

## KEYS

sequence = FieldKey("Sequence", "Sequence Name", template=sequence_root, is_mandatory=True)
shot = FieldKey("Shot", "Shot Name", template=shot_root, dependencies=["Sequence"], is_mandatory=True)

task = FieldKey("Task", "Task", template=step_root, dependencies=["Shot"], is_mandatory=False)
status = FieldKey("status", "Status", values=('wip', 'publish'), preferencie="wip", is_mandatory=True)

# "Footage - Plate" specific fields
task_plate = FieldKey("Task", "Task", template=footage_root, dependencies=["Shot"])
variant_plate = FieldKey("variant", "Scene variant", template=footage_root, dependencies=["Task"])
version_plate = FieldKey("version", "Version", template=footage_root, dependencies=["variant"])
colorspace_plate = FieldKey(tank_id='colorspace', label='Colorspace', template=footage_render_sequence,
                            dependencies=['version'])
extension_seq = FieldKey("extension", "Extension", values=('jpg', 'dpx', 'exr', 'png', 'tiff', 'tga'),
                          preferencie="exr", template=footage_render_sequence, dependencies=["version", "colorspace"])

# "2D - Nuke Shot" specific fields
category_nuke_shot = FieldKey("render_source", "Category", values=('nk', 'nkmatte'), preferencie='nk') #TODO
variant_nuke_shot = FieldKey("variant", "Scene variant", template=nuke_shot_render_folder,
                             dependencies=["status", "Task", "render_source"])
version_nuke_shot = FieldKey("version", "Version", template=nuke_shot_render_folder, dependencies=["variant", "status"])
colorspace_nuke_shot = FieldKey("colorspace", "Colorspace", values=("test", "aces", "acescg"), preferencie="aces",
                                template=nuke_shot_render_folder, dependencies=["version", "render_source"])
write_nuke_shot = FieldKey("write_node", "Write Name", template=nuke_shot_render_folder,
                           dependencies=["version", "colorspace"])
extension_nuke_shot = FieldKey("ext_render_nuke", "Extension", values=('jpg', 'dpx', 'exr', 'png', 'tiff', 'tga'),
                                preferencie="exr", template=nuke_shot_render_sequence,
                                dependencies=["version", "write_node", "colorspace"])

# "2D - Nuke Shot Elements" specific fields
category_nuke_element = FieldKey("render_source", "Category", values=('nkelem', ), preferencie='nkelem') #TODO
colorspace_nuke_element = FieldKey("colorspace", "Colorspace", values=("test", "aces", "acescg"), preferencie="aces",
                                    template=nuke_shot_element_render_folder, dependencies=["variant"])
write_nuke_element = FieldKey("write_node", "Write Name", template=nuke_shot_element_render_root,
                              dependencies=["Task"])
extension_nuke_element = FieldKey("ext_render_nuke", "Extension", values=('jpg', 'dpx', 'exr', 'png', 'tiff', 'tga'),
                                   preferencie="exr", template=nuke_shot_element_render_folder,
                                   dependencies=["version"])
version_nuke_element = FieldKey("version", "Version", template=nuke_shot_element_render_folder,
                                dependencies=["variant"])
variant_nuke_element = FieldKey(tank_id='variant', label='Scene variant', template=nuke_shot_element_render_sequence,
                                dependencies=["write_node"])


## TEMPLATES

tpl_nuke_master = FieldsTemplate(
    name="Plate Master",
    template=footage_root,
    tokens={
        sequence.tank_id: sequence,
        shot.tank_id: shot,
        task_plate.tank_id: task_plate,
        variant_plate.tank_id: variant_plate,
        version_plate.tank_id: version_plate,
        colorspace_plate.tank_id: colorspace_plate,
        extension_seq.tank_id: extension_seq,
    }
)

tpl_nuke_shot = FieldsTemplate(
    name="Nuke Shot",
    template=nuke_shot_render_sequence,
    tokens={
        sequence.tank_id: sequence,
        shot.tank_id: shot,
        task.tank_id: task,
        status.tank_id: status,
        variant_nuke_shot.tank_id: variant_nuke_shot,
        version_nuke_shot.tank_id: version_nuke_shot,
        category_nuke_shot.tank_id: category_nuke_shot,
        colorspace_nuke_shot.tank_id: colorspace_nuke_shot,
        write_nuke_shot.tank_id: write_nuke_shot,
        extension_nuke_shot.tank_id: extension_nuke_shot,
    }
)

tpl_nuke_shot_element = FieldsTemplate(
    name="Nuke Shot Element",
    template=nuke_shot_element_render_folder,
    tokens={
        sequence.tank_id: sequence,
        shot.tank_id: shot,
        task.tank_id: task,
        write_nuke_element.tank_id: write_nuke_element,
        variant_nuke_element.tank_id: variant_nuke_element,
        category_nuke_element.tank_id: category_nuke_element,
        version_nuke_element.tank_id: version_nuke_element,
        colorspace_nuke_element.tank_id: colorspace_nuke_element,
        extension_nuke_element.tank_id: extension_nuke_element,
    }
)

READ_CONFIGS = [
    tpl_nuke_master,
    tpl_nuke_shot,
    tpl_nuke_shot_element,
]
