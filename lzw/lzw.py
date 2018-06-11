# Copyright (c) 2018, Abhinav Jauhri, Martin Griss, Hakan Erdogmus
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root

# Reference:http://www.cs.cmu.edu/~cil/lzw.and.gif.txt  
import sys
import string 
import extras.const as const
import extras.helpers as helpers
import numpy as np
from collections import defaultdict
char_set = map(lambda x: x, string.printable)

def encode(delta_str, base):
    """Encodes delta string as a big integer.

    Args:
        delta_str: A string with delta coordinates in reference to min_x and min_y, min_x and min_y also included

    Returns:
        encoding: big string encoding of delta_str 
    """
    current = ""
    encoding = ""
    d = {'0':'0', '1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9', ',':'A'}
    i = len(d)
    for k in delta_str:
        if current + k in d:
            current = current + k
        elif i >= base and not current + k in d:
            sub_s = current
            while True:
                if sub_s in d:
                    encoding += d[sub_s]
                    current = current[len(sub_s):] + k
                    break
                else:
                    sub_s = sub_s[:-1]
        elif not current + k in d:
            d[current + k] = const.encode_values[i]
            i += 1
            encoding += d[current]
            current = k
    encoding += d[current]
    return encoding
