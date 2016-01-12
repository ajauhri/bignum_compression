import sys
import string 
import extras.const as const
import extras.helpers as helpers
import numpy as np
import math
from collections import defaultdict

def var_del_trans(s, base, d=True):
    result = ''
    mins = []
    reserve_chars = []
    for i in xrange(base, 70):
        reserve_chars.append(const.encode_values[i])
    deltas = np.array(s.split(',')[2:], dtype='int')
    mins.append(int(s.split(',')[0]))
    mins.append(int(s.split(',')[1]))
    for i in range(2):
        q = mins[i]/base
        r = mins[i] - base*q
        if q >= base:
            result += reserve_chars[int(q/base) - 1] + helpers.base_encode(q % base, base) + helpers.base_encode(r, base)
        else:
            result += helpers.base_encode(q, base) + helpers.base_encode(r, base)
    for v in deltas:
        e = helpers.base_encode(int(v), base)
        if len(e) > 1:
            q = int(v) / base
            r = int(v) % base
            assert q<=8
            result += reserve_chars[q-1] + helpers.base_encode(r, base)
        else:
            result += e
    #if len(result2) < len(result):
    #    print len(result) - len(result2)
    #print len(string_base_conversion(s, base))- len(result)
    return result

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

def golomb_dynamic_trans(s, base):
    mins = []
    deltas = np.array(s.split(',')[2:], dtype='int')
    mins.append(int(s.split(',')[0]))
    mins.append(int(s.split(',')[1]))
    e = int(math.ceil(math.log(np.percentile(deltas, 80), 2)))
    return helpers.base_encode(e, base) + golomb_trans(s, base, e)

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

def encode_w_hh(s, d, step):
    encoding = ""
    i = 0
    while i < len(s):
        sub_str = s[i:i+step]
        if sub_str in d:
            encoding += '#' + d[sub_str]
            i += step
        else:
            encoding += sub_str[0]
            i += 1
    return encoding

def decode_w_hh(s, d):
    inv_d = {v: k for k, v in d.items()}
    result = ""
    i = 0
    while i < len(s):
        if s[i] != '#':
            result += s[i]
            i += 1
        else:
            result += inv_d[s[i+1]]
            i += 2
    return result

def invert_var_del_trans(s, base, d=True):
    reserve_chars = []
    for i in xrange(base, 70):
        reserve_chars.append(const.encode_values[i])
    result = []
    i = 0
    count = 0
    while count < 2:
        if s[i] not in reserve_chars:
            token = helpers.base_decode(s[i], base)  
            i += 1
        else:
            m = reserve_chars.index(s[i]) + 1
            token = helpers.base_decode(s[i+1:i+2], base)  
            token = m*base + token
            i += 2
        result += str(token*base + helpers.base_decode(s[i], base))
        result += ','
        i += 1
        count += 1

    while i < len(s):
        if s[i] not in reserve_chars:
            result += str(helpers.base_decode(s[i], base)) + ','
            i += 1
        else:
            m = reserve_chars.index(s[i]) + 1
            result += str(m*base + helpers.base_decode(s[i+1:i+2], base)) + ','
            i += 2
    result = result[:-1]
    return ''.join(result)


def heavy_hitters(data, size, step):
    result = []
    d = defaultdict(int)
    for line in data:
        for i in range(0, len(line) - (step-1)):
            sub_str = line[i:i+step]
            d[sub_str] += 1
    for i in range(size):
        v = max(d, key=d.get)
        result.append(v)
        d[v] = 0
    return result

def get_dict_elems():
    elements = []
    for i in range(10):
        c = chr(i + ord("0"))
        print i + ord('0'), chr(i + ord('0'))
        elements.append(c)

    for i in range(26):
        c=chr(i+ord("A"))
        elements.append(c)
        c=chr(i+ord("a"))
        elements.append(c)
    return elements

def golomb_diff_trans(s, base):
    result = '1'
    mins = []
    deltas = np.array(s.split(','), dtype='int')
    for v in deltas:
        if v >= base:
            q = int(v) / base
            r = int(v) % base
            result += '1'*int(q) +'0' + '{0:06b}'.format(r)
        else:
            result += '0' + '{0:06b}'.format(v)
    result = helpers.base_encode(int(result, 2), base)
    return result

def invert_golomb_diff_trans(s, base):
    result = ''
    d = helpers.base_decode(s, base)
    b = bin(d)[3:]
    while b:
        zi = b.find('0')
        b = b[zi+1:]
        result += str(zi*base + int(b[:6], 2)) + ','
        b = b[6:]
    return ''.join(result[:-1])

