import os
import nuke
from node.domain import nukebricks

root_path = "/s/prods/test_dev/sequence/sq_alaurette_212/sq_alaurette_212_nuke/cmp/nuke/wip/sq_alaurette_212_nuke-cmp-caca-v001.nk"

if not os.path.exists(root_path):
    nuke.scriptSaveAs(root_path, 1)
nuke.scriptOpen(root_path)
nukebricks.create_write(root_path)
nuke.scriptSaveAs(root_path, 1)

