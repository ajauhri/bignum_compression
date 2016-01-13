import const
import numpy as np

def setup_base():
    encode_values=[0]*256
    decode_values=[0]*256
    
    for i in range(10):
        c = chr(i + ord("0"))
        encode_values[i] = c

    for i in range(26):
        c=chr(i+ord("A"))
        encode_values[i+10]=c
        c=chr(i+ord("a"))
        encode_values[i+36]=c
    encode_values[62]="+"
    encode_values[63]="`"
    encode_values[64]="*"
    encode_values[65]="/"

    encode_values[66]="("
    encode_values[67]=")"
    encode_values[68]="["
    encode_values[69]="]"

    encode_values[70]="{"
    encode_values[71]="}"
    encode_values[72]="!"
    encode_values[73]="|"

    encode_values[74]="\\"
    encode_values[75]="$"
    encode_values[76]="@"
    encode_values[77]="%"

    encode_values[78]="^"
    encode_values[79]="&"
    encode_values[80]="_"
    encode_values[81]="="

    encode_values[82]=":"
    encode_values[83]=";"
    encode_values[84]="."
    encode_values[85]="'"

    encode_values[86]='"'
    encode_values[87]="~"
    encode_values[88]="<"
    encode_values[89]=">"

    encode_values[90]="?"

# cant have a "'" or "#" in it
    for i in range(91):
        c = encode_values[i]
        decode_values[ord(c)] = i
    const.encode_values = encode_values
    const.decode_values = decode_values
     
def base_encode(n, base):
# more efficient than previous; handles "-"
# doesnt truncate to "digits"
# returns variable length; can do a pad_zero(...)if need fixed width
    if n == 0:
        return "0"
    if n < 0:
        return "-" + const.base_encode(-n, base)
    res = ""
    nn = n
    while n > 0:
        nb = int(n/base)
        dig = n-nb*base
        n = nb
        c = const.encode_values[dig]
        res = c + res
    return res

def base_decode(nb, base):
    if len(nb) <= 0:
        return 0
    if nb[0] == '-':
        return -base_decode(nb[1:], base)
    result = 0
    for i in range(len(nb)):
        result *= base
        dig = ord(nb[i])
        c = const.decode_values[dig]
        result += c
    return result

# returns array of rows; each row in the form of - <id>|<# of points>|<orig len of polygon>|<polygon>|<orig bar len>
def get_polygons_w_deltas(ifile):
    fd = file(ifile, 'r')
    results = []
    for line in fd.readlines():
        columns = line.split('|')
        min_x = 999999
        min_y = 999999
        max_x = 0
        max_y = 0
        o_bar = ""
        for i in columns[8].split():
            c = [int(float(x) * 100) for x in i.split(',')]
            if c[0] < 0:
                c[0] = c[0] - 2*c[0]
            if c[1] < 0:
                c[1] = c[1] - 2*c[1]
            o_bar += ','.join([str(x) for x in c])

            if c[0] < min_x:
                min_x = c[0]
            if c[1] < min_y:
                min_y = c[1]

            if c[0] > max_x:
                max_x = c[0]
            if c[1] > max_y:
                max_y = c[1]
            o_bar += ','
        o_bar = o_bar[:-1]
        pc = o_bar.rfind(',', 0, o_bar.rfind(','))
        o_bar = o_bar[:pc]

        cs = ''
        n = 0
        for i in columns[8].split():
            c = [int(float(x)* 100) for x in i.split(',')]
            if c[0] < 0:
                c[0] = c[0] - 2*c[0]
            if c[1] < 0:
                c[1] = c[1] - 2*c[1]
            c[0] = c[0] - min_x
            c[1] = c[1] - min_y
            cs += str(c[0]) + ',' + str(c[1]) + ','
            n += 1
        if n > 0:
            cs = str(min_x) + ',' + str(min_y) + ',' + cs
            cs = cs[:-1]
            results.append({'id': int(columns[0]), 'vertices': n, 'trans_poly': cs, 'max_x': max_x, 'max_y': max_y, 'orig_poly': columns[8], 'o_bar_len': len(o_bar)})
    fd.close()
    return results

def get_polygons(ifile):
    fd = file(ifile, 'r')
    results = []
    for line in fd.readlines():
        columns = line.split('|')
        cs = ''
        n = 0
        for i in columns[8].split():
            c = i.split(',')
            cs += str(c[0]) + ',' + str(c[1]) + ',' 
            n += 1
        if n > 0:
            cs = cs[:-1]
            results.append(columns[0] + '|' + str(n) + '|' + str(len(columns[8])) + '|' + str(len(cs)) + '|' + cs)
    fd.close()
    return results

def get_diff_polygon(orig):
    coords_arr = map(lambda x: map(lambda y: int(float(y)*100), x.split(',')), orig.split())
    for i in range(len(coords_arr)):
        if coords_arr[i][1] < 0:
            coords_arr[i][1] = -1*coords_arr[i][1]
    cons_delta_arr = []
    cons_delta_arr.append(coords_arr[0])
    for i in range(1, len(coords_arr)):
        cons_delta_arr.append([coords_arr[i][0] - coords_arr[i-1][0], coords_arr[i][1] - coords_arr[i-1][1]])
    s = '' 
    for v in cons_delta_arr:
        s += str(v[0]) + ',' + str(v[1]) + ','
    s = s[:-1]
    return s

def transform(s):
    a = map(int, s.split(','))
    r = str(a[0] - const.x_origin) + ','
    r += str(a[1] - const.y_origin) + ','
    for i in a[2:]:
        if i < 0:
            i = abs(i)
            r += str(2*i - 1) + ','
        else:
            r += str(2*i) + ','
    return r[:-1]


def write_summary(fname, d, algos, trans):
    len = 'len'
    cr = 'cr'
    fd = file(fname + '.csv', 'w')
    fd.write("technique,min_len,mean_len,max_len,stddev_len,95th_percentile_len,min_ratio,mean_ratio,max_ratio,stddev_ratio,95th_percentile_ratio\n")
    for algo in algos:
        algo += trans
        fd.write("%s & %d & %.1f & %d & %.1f & %.1f & %.1f & %.1f & %.1f & %.1f & %.1f\n" % (algo, np.min(d[algo+len]), np.mean(d[algo+len]), np.max(d[algo+len]), np.std(d[algo+len]), np.percentile(d[algo+len], 95), np.min(d[algo+cr])*100, np.mean(d[algo+cr])*100, np.max(d[algo+cr])*100, np.std(d[algo+cr])*100, np.percentile(d[algo+cr], 95)*100))
    fd.close()
