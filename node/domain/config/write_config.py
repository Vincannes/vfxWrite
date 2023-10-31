from node.domain.config import nuke_shot_render_sequence
from node.domain.config.models import FieldKey, FieldsTemplate

# Config Write Node Interface
sequence = FieldKey("Sequence", "Sequence Name")
shot = FieldKey("Shot", "Shot Name")
task = FieldKey("Task", "Task")
variant = FieldKey("variant", "Scene variant")
category = FieldKey("render_source", "Category", values=('nk', 'nkmatte', 'nkelem'), preferencie='nk')
write = FieldKey("write_node", "Write Name")
version = FieldKey("version", "Version")
colorspace = FieldKey("colorspace", "Colorspace", values=("test", "aces", "acescg"), preferencie="aces")
extension = FieldKey("ext_render_nuke", "Extension", values=('jpg', 'dpx', 'exr', 'png', 'tiff', 'tga'), preferencie="exr")

tpl_write_nuke = FieldsTemplate(
    name="Nuke Shot Element",
    template=nuke_shot_render_sequence,
    tokens={
        sequence.tank_id: sequence,
        shot.tank_id: shot,
        task.tank_id: task,
        variant.tank_id: variant,
        category.tank_id: category,
        write.tank_id: write,
        version.tank_id: version,
        colorspace.tank_id: colorspace,
        extension.tank_id: extension,
    }
)

WRITE_CONFIGS = [
    sequence,
    shot,
    task,
    variant,
    category,
    write,
    version,
    colorspace,
    extension
]

