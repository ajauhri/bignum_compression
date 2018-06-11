# Copyright (c) 2018, Abhinav Jauhri, Martin Griss, Hakan Erdogmus
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root

import sys
import string 
import extras.const as const
import extras.helpers as helpers
import numpy as np
import math
from collections import defaultdict

def golomb_trans(s, base, e):
    bs = '{0:0%db}' % e
    result = '1'
    mins = []
    deltas = np.array(s.split(',')[2:], dtype='int')
    mins.append(int(s.split(',')[0]))
    mins.append(int(s.split(',')[1]))
    m = 2**e
    for i in range(2):
        q = mins[i]/m
        r = mins[i] - m*q
        if q >= m:
            result += '1'*int(q/m) +'0' + bs.format(q%m) + bs.format(r)
        else:
            result += '0' + bs.format(q) + bs.format(r)
    for v in deltas:
        if v >= m:
            q = int(v) / m
            r = int(v) % m
            result += '1'*int(q) +'0' + bs.format(r)
        else:
            result += '0' + bs.format(v)
    bits = len(result)
    result = helpers.base_encode(int(result, 2), base)
    return {'encoding': result, 'bit_len': bits}

def invert_golomb_trans(s, base, e):
    bs = e
    result = ''
    count = 0
    m = 2**e
    d = helpers.base_decode(s, base)
    b = bin(d)[3:]
    while count < 2:
        zi = b.find('0')
        if zi:
            b = b[zi+1:]
            v = (zi*m + int(b[:bs], 2)) * m
            v += int(b[bs:2*bs], 2)
        else:
            b = b[zi+1:]
            v = int(b[:bs], 2) * m
            v += int(b[bs:2*bs], 2)
        b = b[2*bs:]
        result += str(v) + ','
        count += 1
    while b:
        zi = b.find('0')
        b = b[zi+1:]
        result += str(zi*m + int(b[:bs], 2)) + ','
        b = b[bs:]
    return ''.join(result[:-1])
