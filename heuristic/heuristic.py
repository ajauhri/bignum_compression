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
        M = helpers.base_decode(big_str[:i], base)
        M = M + 2
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
            m = big_num % M
            big_num = big_num / M
            deltas.append(int(m))
        deltas = deltas[::-1]
        deltas[0] -= 1
        deltas[1] -= 1
        if deltas == coords:
            return True
