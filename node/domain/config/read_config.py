"""
Tank Templates config.

tank - templates.yml contains intermediate templates such as Generic_Name i.e Sequence folders.
This is done in order to speed up the path searching request. This is represented by template_folder in this file.
"""

from node.domain.config.fields import *
from node.domain.config.models import FieldsTemplate, FieldKey

## KEYS

sequence = FieldKey("Sequence", "Sequence Name", template=sequence_root)
shot = FieldKey("Shot", "Shot Name", template=shot_root, dependencies=["Sequence"])
task = FieldKey("Task", "Task", template=step_root, dependencies=["Shot"])
variant = FieldKey("variant", "Scene variant", template=nuke_shot_render_folder, dependencies=["Task"])
category = FieldKey("render_source", "Category", values=('nk', 'nkmatte', 'nkelem'), preferencie='nk') #TODO
write = FieldKey("write_node", "Write Name", template=nuke_shot_render_folder, dependencies=["version", "colorspace"])
version = FieldKey("version", "Version", template=nuke_shot_render_folder, dependencies=["variant", "status"])
colorspace = FieldKey("colorspace", "Colorspace", values=("test", "aces", "acescg"), preferencie="aces",
                      template=nuke_shot_render_folder, dependencies=["version", "render_source"])
extension = FieldKey("ext_render_nuke", "Extension", values=('jpg', 'dpx', 'exr', 'png', 'tiff', 'tga'),
                     preferencie="exr", template=nuke_shot_render_sequence, dependencies=["version", "write_node", "colorspace"])

## TEMPLATES

nuke_shot = FieldsTemplate(
    name="Nuke Shot",
    template=nuke_shot_render_sequence,
    tokens={
        "Sequence": sequence,
        "Shot": shot,
        "Task": task,
        "variant": variant,
        "version": version,
        "colorspace": colorspace,
        "write_node": write,
        "ext_render_nuke": extension,
    }
)

nuke_master = FieldsTemplate(
    name="Plate Master",
    template=footage_root,
    tokens={
        "Sequence": sequence,
        "Shot": shot,
        "Task": task,
        "variant": variant,
        "version": version,
        "colorspace": colorspace,
        "ext_render_nuke": extension,
    }
)

READ_CONFIGS = [
    nuke_shot,
    nuke_master,
]
