# Copyright (c) 2018, Abhinav Jauhri, Martin Griss, Hakan Erdogmus
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root

import zlib
def encode(s):
    #obj = zlib.compressobj(9, zlib.DEFLATED, 8, zlib.DEF_MEM_LEVEL, 0)
    encoding = zlib.compress(s, 9)
    return encoding
