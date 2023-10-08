from node.domain.config.field import FieldKey

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

