
import nuke

import importlib
from node.domain.mikread import mik_read_node
importlib.reload(mik_read_node)

from node.domain.mikread import MikReadNode
from node.domain.mikwrite import MikWriteNode

def create_read(path=""):
    write = MikReadNode(path).createNode()
    return write

def create_write(path=""):
    if not path:
        path = nuke.root().name()
    write = MikWriteNode(path).createNode()
    return write

