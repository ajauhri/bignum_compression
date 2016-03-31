#! /usr/bin/env python
''' 
To run with all WEAs:  ./main.py -i <foobar>.csv 
To run with first `n` WEAs:  ./main.py -i <foobar>.csv -n <number_of_WEAs_to_be_read>
'''

from __future__ import division
from optparse import OptionParser
import extras.helpers as helpers
import extras.const as const
import heuristic.heuristic as heuristic
import std_methods.gzip as gzip
import math
import lzw.lzw as lzw
import vle.vle as vle
import matplotlib.pyplot as plt
import numpy as np
#import golomb 

const.chars = {'0': 0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, ',':10}

const.x_origin = 1600
const.y_origin = 6000
const.x_factor = 3500
const.y_factor = 10000
const.base = 70

def main():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='ifile', help='input file')
    parser.add_option('-n', '--number', dest='num_to_read', help='number of polygongs to read', type='int')
    (options, args) = parser.parse_args()

    if not options.ifile:
        print 'all options not provided'
        exit(0)

    helpers.setup_base()
    data_rows = helpers.get_polygons_w_deltas(options.ifile)
    del_polygons = []
    diff_polygons = []
    for i in range(len(data_rows)):
        verts = data_rows[i]['trans_poly'].split(',')
        orig_poly = data_rows[i]['orig_poly']
        verts[0] = str(int(verts[0]) - const.x_origin)
        verts[1] = str(int(verts[1]) - const.y_origin)
        verts = ','.join(verts)
        penultimate_comma = verts.rfind(',', 0, verts.rfind(','))
        del_polygons.append(verts[:penultimate_comma])
        orig_poly = orig_poly[:orig_poly.rfind(' ')]
        diff_polygons.append(helpers.transform(helpers.get_diff_polygon(orig_poly)))
        
        #create a separate file for each polygon
        fd = file('diff_polygons/' + str(i+1), 'w')
        for val in diff_polygons[-1].split(','):
            fd.write(val + '\n')
        fd.close()

        #create a separate file for each polygon
        fd = file('del_polygons/' + str(i+1), 'w')
        for val in del_polygons[-1].split(','):
            fd.write(val + '\n')
        fd.close()


    if not options.num_to_read:
        options.num_to_read = len(del_polygons)
    if options.num_to_read > len(data_rows):
        options.num_to_read = len(data_rows)
    all_out = file('./results/all.csv', 'w')
    all_out.write('id,' + \
            'points,' + \
            'orig_len,' + \
            'del_len,' + \
            'diff_len,' + \
            'lzw_del_len,' + \
            'big_del_len,' + \
            'golomb_del_len,' + \
            'lzw_diff_len,' + \
            'big_diff_len,' + \
            'golomb_diff_len,' + \
            'big_diff_bits,' + \
            'golomb_diff_bits,' + \
            'big_del_bits,' + \
            'golomb_del_bits\n')
 
    
    golomb_del_encodings = []
    golomb_diff_encodings = []
    for i in range(len(data_rows)):
        golomb_del_encodings.append(vle.golomb_trans(del_polygons[i], const.base, 5))
        golomb_diff_encodings.append(vle.golomb_trans(diff_polygons[i], const.base, 5))
    
    algos = ['big_factor', 'gzip', 'golomb', 'lzw', 'trans', 'o_bar']
    stats = {}
    for algo in algos:
        for t in ['_diff', '_del']:
            stats[algo + t + '_len'] = []
            stats[algo + t + '_cr'] = []
    bigwin = 0
    golwin = 0
    for i in range(options.num_to_read):
        assert del_polygons[i] == vle.invert_golomb_trans(golomb_del_encodings[i]['encoding'], 
                                                          const.base, 5)
        big_del_encoding = heuristic.big_encode(del_polygons[i], 
                                                data_rows[i]['vertices'] - 1, const.base)
        assert big_del_encoding != False
        gzip_del_encoding = gzip.encode(del_polygons[i])
        lzw_del_encoding = lzw.encode(del_polygons[i], base)
                 
        #Consecutive delta based i.e. x1, y1, x2-x1, y2-y1, x3-x2, y3-y2...  on the original coordinates
        gzip_diff_encoding = gzip.encode(diff_polygons[i])
        assert diff_polygons[i] == vle.invert_golomb_trans(golomb_diff_encodings[i]['encoding'], 
                                                           const.base, 5)
        big_diff_encoding = heuristic.big_encode(diff_polygons[i], 
                                                 data_rows[i]['vertices']  - 2,
                                                 base, True)
        assert big_diff_encoding != False
        lzw_diff_encoding = lzw.encode(diff_polygons[i], base)
         
        orig_len = len(data_rows[i]['orig_poly'])
        o_bar_len = data_rows[i]['o_bar_len']
        del_len = len(del_polygons[i])
        diff_len = len(diff_polygons[i])

        stats['big_factor' + '_del_' + 'len'].append(big_del_encoding['len'])
        stats['big_factor' + '_del_' + 'cr'].append(big_del_encoding['len']/orig_len)
        stats['golomb' + '_del_' + 'len'].append(len(golomb_del_encodings[i]['encoding']))
        stats['golomb' + '_del_' + 'cr'].append(len(golomb_del_encodings[i]['encoding'])/orig_len)
        stats['lzw' + '_del_' + 'len'].append(len(lzw_del_encoding))
        stats['lzw' + '_del_' + 'cr'].append(len(lzw_del_encoding)/orig_len)
        stats['gzip' + '_del_' + 'len'].append(len(gzip_del_encoding))
        stats['gzip' + '_del_' + 'cr'].append(len(gzip_del_encoding)/orig_len)
        stats['trans' + '_del_' + 'len'].append(len(del_polygons[i]))
        stats['trans' + '_del_' + 'cr'].append(len(del_polygons[i])/orig_len)
        stats['o_bar' + '_del_' + 'len'].append(o_bar_len)
        stats['o_bar' + '_del_' + 'cr'].append(o_bar_len/orig_len)

        stats['lzw' + '_diff_' + 'len'].append(len(lzw_diff_encoding))
        stats['lzw' + '_diff_' + 'cr'].append(len(lzw_diff_encoding)/orig_len)
        stats['gzip' + '_diff_' + 'len'].append(len(gzip_diff_encoding))
        stats['gzip' + '_diff_' + 'cr'].append(len(gzip_diff_encoding)/orig_len)
        stats['golomb' + '_diff_' + 'len'].append(len(golomb_diff_encodings[i]['encoding']))
        stats['golomb' + '_diff_' + 'cr'].append(len(golomb_diff_encodings[i]['encoding'])/orig_len)
        stats['big_factor' + '_diff_' + 'len'].append(big_diff_encoding['len'])
        stats['big_factor' + '_diff_' + 'cr'].append(big_diff_encoding['len']/orig_len)
        stats['trans' + '_diff_' + 'len'].append(len(diff_polygons[i]))
        stats['trans' + '_diff_' + 'cr'].append(len(diff_polygons[i])/orig_len)
        stats['o_bar' + '_diff_' + 'len'].append(o_bar_len)
        stats['o_bar' + '_diff_' + 'cr'].append(o_bar_len/orig_len)
        points = (data_rows[i]['vertices'] - 1)*2
        all_out.write("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%.2f,%.2f,%.2f,%.2f\n" % (data_rows[i]['id'], data_rows[i]['vertices'], orig_len, del_len, diff_len, len(lzw_del_encoding), len(big_del_encoding['big_str']), len(golomb_del_encodings[i]['encoding']), len(lzw_diff_encoding), len(big_diff_encoding['big_str']), len(golomb_diff_encodings[i]['encoding']), big_diff_encoding['bit_len']/points, golomb_diff_encodings[i]['bit_len']/points, big_del_encoding['bit_len']/(points+2), golomb_del_encodings[i]['bit_len']/(points+2)))
        if big_del_encoding['bit_len']/points <= golomb_del_encodings[i]['bit_len']/points:
            bigwin += 1
        else:
            golwin += 1
    print '#instances BIG bettter: %d, #instances Golomb better: %d' % (bigwin, golwin)
    all_out.close()
    helpers.write_summary('./results/delta_summary', stats, algos, '_del_') 
    helpers.write_summary('./results/diff_summary', stats, algos, '_diff_') 

if __name__ == "__main__":
    main()
