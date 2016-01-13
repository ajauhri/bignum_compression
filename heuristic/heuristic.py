import numpy as np
import extras.helpers as helpers
import extras.const as const
import math

def big_encode(delta_str, n_vertices, base, m=False):
    """Encodes delta string as a big integer.

    Args:
        delta_str: A string with delta coordinates in reference to min_x and min_y, min_x and min_y also included
        n_vertices: Number of vertices in the polygon
        base

    Returns:
        A dict mapping keys to corresponding compression results.
        big_str: big string encoding of delta_str in a particular base (current base 62)
        big_bit_len: length of binary representation of big_str
        shannon_bit_bound: Shannon bound of number of bits needed to encode the polygon
    """
    delta_arr = delta_str.split(',')
    n_to_skip = 2 #since the min and max are appended to the beginning of the polygon argument
    coords = map(int, delta_arr[n_to_skip:])
    d_x = [coords[2*i] for i in range(n_vertices)]
    d_y = [coords[2*i + 1] for i in range(n_vertices)]
    x_delta = max(d_x)# - min(d_x)
    y_delta = max(d_y)# - min(d_y)
    Dx_min  = int(delta_arr[0])
    Dy_min = int(delta_arr[1])
    big_num = 0
    M = max(x_delta, y_delta) + 2
    
    for i in xrange(n_vertices):
        if i == 0:
            big_num = big_num * M * M + (d_x[i] + 1) * M + d_y[i] + 1
        else:
            big_num = big_num * M * M + (d_x[i]) * M + d_y[i] 
    big_num = big_num*const.x_factor + Dx_min
    big_num = big_num*const.y_factor + Dy_min
    M_encode = helpers.base_encode(M-2, base)
    big_str = M_encode + helpers.base_encode(big_num, base) # prefix and postfix not appended
    if big_decode(big_str, coords, base, m):
        return {'big_str': big_str, 'big_num': big_num, 'SS': M, 'bit_len': big_num.bit_length() + M.bit_length(), 'len': len(big_str) - len(M_encode) + 2}
    else:
        return False

def big_decode(big_str, coords, base, m):
    """Decodes big number back to delta coordinates

    Args:
        big_str: Big string encoding as returned by heuristic.big_encode
        coords: Delta coordinates of the original polygon used for created big string 
        base

    Returns:
        True if the decoded list of delta coordinates matches original delta coordinates `coords`. 
        False otherwise.
    """
    for i in [1,2]:
        S = helpers.base_decode(big_str[:i], base)
        SS = S + 2
        big_num = helpers.base_decode(big_str[i:], base)
        z = big_num/const.y_factor
        Dy_min = big_num - const.y_factor * z 
        big_num = z
        z = big_num/const.x_factor
        Dx_min = big_num - const.x_factor * z
        big_num = z
        deltas = []
        flagged = False
        while big_num > 0:
            m = big_num % SS 
            big_num = big_num / SS
            deltas.append(int(m))
        deltas = deltas[::-1]
        deltas[0] -= 1
        deltas[1] -= 1
        if deltas == coords:
            return True

def poly_encode(delta_str, n_vertices, base):
    result = ''
    mins = []
    reserve_chars = ['%','@','!','+','=','^']
    deltas = np.array(delta_str.split(',')[2:], dtype='int')
    mins.append(int(delta_str.split(',')[0]))
    mins.append(int(delta_str.split(',')[1]))
    for i in range(2):
        q = mins[i]/base
        r = mins[i] - base*q
        if q > base:
            result += reserve_chars[int(q/base) - 1] + helpers.base_encode(q % base, base) + helpers.base_encode(r, base)
        else:
            result += helpers.base_encode(q, base) + helpers.base_encode(r, base)
    assert len(result) == 5
    big_num = 0
    delta_arr = delta_str.split(',')
    n_to_skip = 2 #since the min and max are appended to the beginning of the polygon argument
    coords = map(int, delta_arr[n_to_skip:])
    d_x = [coords[2*i] for i in range(n_vertices)]
    d_y = [coords[2*i + 1] for i in range(n_vertices)]
    x_delta = max(d_x) - min(d_x)
    y_delta = max(d_y) - min(d_y)
 
    Dx_min  = int(delta_arr[0])
    Dy_min = int(delta_arr[1])
    
    S = max(x_delta, y_delta)/10 + 1
    SS = 10*S + 1
    for i in xrange(n_vertices):
        big_num = big_num*SS*SS + (d_x[i] + 1)*SS + (d_y[i] + 1)
    big_str = result + helpers.base_encode(S, base) + helpers.base_encode(big_num, base)
    return big_str

def point_encode(poly_str, b):
    coords = poly_str.split(',')
    combs = []
    all_rems = []
    l = 0
    for i in xrange(0, len(coords), 2):
        lat = int(coords[i])
        longt = int(coords[i+1])
        combs.append(((lat + longt)* (lat + longt + 1)/2) + lat)
        n = combs[-1]
        rems = []
        if n == 0:
            rems = [0]
        while n:
            rems.append(n%32)
            n = n/32
        rems = map(lambda x: x+32, rems)
        rems[-1] = rems[-1] - 32
        if i == 0:
            l += 6
        else:
            if len(rems) < 3:
                l += len(rems) + 1
            else:
                l += 3
        all_rems.append(rems)
    return l
