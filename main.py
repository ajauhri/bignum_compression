#! /usr/bin/env python
''' 
To run with all WEAs:  ./main.py -i <foobar>.csv 
To run with first `n` WEAs:  ./main.py -i <foobar>.csv -n <number_of_WEAs_to_be_read>
'''

from __future__ import division
from optparse import OptionParser
import extras.helpers as helpers
import extras.const as const
import bignum.bignum as bignum
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
    # del -> delta_min
    # diff -> delta
    delta_min_polygons = []
    delta_polygons = []
    for i in range(len(data_rows)):
        verts = data_rows[i]['trans_poly'].split(',')
        orig_poly = data_rows[i]['orig_poly']
        verts[0] = str(int(verts[0]) - const.x_origin)
        verts[1] = str(int(verts[1]) - const.y_origin)
        verts = ','.join(verts)
        penultimate_comma = verts.rfind(',', 0, verts.rfind(','))
        delta_min_polygons.append(verts[:penultimate_comma])
        orig_poly = orig_poly[:orig_poly.rfind(' ')]
        delta_polygons.append(helpers.transform(helpers.get_delta_polygon(orig_poly)))
        
        #create a separate file for each polygon
        fd = file('delta_polygons/' + str(i+1), 'w')
        for val in delta_polygons[-1].split(','):
            fd.write(val + '\n')
        fd.close()

        #create a separate file for each polygon
        fd = file('delta_min_polygons/' + str(i+1), 'w')
        for val in delta_min_polygons[-1].split(','):
            fd.write(val + '\n')
        fd.close()


    if not options.num_to_read:
        options.num_to_read = len(delta_min_polygons)
    if options.num_to_read > len(data_rows):
        options.num_to_read = len(data_rows)
    all_out = file('./results/all.csv', 'w')
    all_out.write('id,' + \
            'points,' + \
            'orig_len,' + \
            'delta_min_len,' + \
            'delta_len,' + \
            'lzw_delta_min_len,' + \
            'big_delta_min_len,' + \
            'golomb_delta_min_len,' + \
            'lzw_delta_len,' + \
            'big_delta_len,' + \
            'golomb_delta_len,' + \
            'big_delta_bits,' + \
            'golomb_delta_bits,' + \
            'big_delta_min_bits,' + \
            'golomb_delta_min_bits\n')
 
    
    golomb_delta_min_encodings = []
    golomb_delta_encodings = []
    for i in range(len(data_rows)):
        golomb_delta_min_encodings.append(vle.golomb_trans(delta_min_polygons[i], const.base, 5))
        golomb_delta_encodings.append(vle.golomb_trans(delta_polygons[i], const.base, 5))
    
    algos = ['big_factor', 'gzip', 'golomb', 'lzw', 'trans', 'o_bar']
    stats = {}
    for algo in algos:
        for t in ['_delta', '_delta_min']:
            stats[algo + t + '_len'] = []
            stats[algo + t + '_cr'] = []
    bigwin = 0
    golwin = 0
    for i in range(options.num_to_read):
        assert delta_min_polygons[i] == vle.invert_golomb_trans(golomb_delta_min_encodings[i]['encoding'], const.base, 5)
        big_delta_min_encoding = bignum.encode(delta_min_polygons[i], 
                                                      data_rows[i]['vertices'] - 1, const.base)
        assert big_delta_min_encoding != False
        gzip_delta_min_encoding = gzip.encode(delta_min_polygons[i])
        lzw_delta_min_encoding = lzw.encode(delta_min_polygons[i], const.base)
                 
        #Consecutive delta based i.e. x1, y1, x2-x1, y2-y1, x3-x2, y3-y2...  on the original coordinates
        gzip_delta_encoding = gzip.encode(delta_polygons[i])
        assert delta_polygons[i] == vle.invert_golomb_trans(golomb_delta_encodings[i]['encoding'], const.base, 5)
        big_delta_encoding = bignum.encode(delta_polygons[i], 
                                                 data_rows[i]['vertices']  - 2,
                                                 const.base, True)
        assert big_delta_encoding != False
        lzw_delta_encoding = lzw.encode(delta_polygons[i], const.base)
         
        orig_len = len(data_rows[i]['orig_poly'])
        o_bar_len = data_rows[i]['o_bar_len']
        delta_min_len = len(delta_min_polygons[i])
        delta_len = len(delta_polygons[i])

        stats['big_factor' + '_delta_min_' + 'len'].append(big_delta_min_encoding['len'])
        stats['big_factor' + '_delta_min_' + 'cr'].append(big_delta_min_encoding['len']/orig_len)
        stats['golomb' + '_delta_min_' + 'len'].append(len(golomb_delta_min_encodings[i]['encoding']))
        stats['golomb' + '_delta_min_' + 'cr'].append(len(golomb_delta_min_encodings[i]['encoding'])/orig_len)
        stats['lzw' + '_delta_min_' + 'len'].append(len(lzw_delta_min_encoding))
        stats['lzw' + '_delta_min_' + 'cr'].append(len(lzw_delta_min_encoding)/orig_len)
        stats['gzip' + '_delta_min_' + 'len'].append(len(gzip_delta_min_encoding))
        stats['gzip' + '_delta_min_' + 'cr'].append(len(gzip_delta_min_encoding)/orig_len)
        stats['trans' + '_delta_min_' + 'len'].append(len(delta_min_polygons[i]))
        stats['trans' + '_delta_min_' + 'cr'].append(len(delta_min_polygons[i])/orig_len)
        stats['o_bar' + '_delta_min_' + 'len'].append(o_bar_len)
        stats['o_bar' + '_delta_min_' + 'cr'].append(o_bar_len/orig_len)

        stats['lzw' + '_delta_' + 'len'].append(len(lzw_delta_encoding))
        stats['lzw' + '_delta_' + 'cr'].append(len(lzw_delta_encoding)/orig_len)
        stats['gzip' + '_delta_' + 'len'].append(len(gzip_delta_encoding))
        stats['gzip' + '_delta_' + 'cr'].append(len(gzip_delta_encoding)/orig_len)
        stats['golomb' + '_delta_' + 'len'].append(len(golomb_delta_encodings[i]['encoding']))
        stats['golomb' + '_delta_' + 'cr'].append(len(golomb_delta_encodings[i]['encoding'])/orig_len)
        stats['big_factor' + '_delta_' + 'len'].append(big_delta_encoding['len'])
        stats['big_factor' + '_delta_' + 'cr'].append(big_delta_encoding['len']/orig_len)
        stats['trans' + '_delta_' + 'len'].append(len(delta_polygons[i]))
        stats['trans' + '_delta_' + 'cr'].append(len(delta_polygons[i])/orig_len)
        stats['o_bar' + '_delta_' + 'len'].append(o_bar_len)
        stats['o_bar' + '_delta_' + 'cr'].append(o_bar_len/orig_len)
        points = (data_rows[i]['vertices'] - 1)*2
        all_out.write("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%.2f,%.2f,%.2f,%.2f\n" % (data_rows[i]['id'], data_rows[i]['vertices'], orig_len, delta_min_len, delta_len, len(lzw_delta_encoding), len(big_delta_min_encoding['big_str']), len(golomb_delta_min_encodings[i]['encoding']), len(lzw_delta_encoding), len(big_delta_encoding['big_str']), len(golomb_delta_encodings[i]['encoding']), big_delta_encoding['bit_len']/points, golomb_delta_encodings[i]['bit_len']/points, big_delta_min_encoding['bit_len']/(points+2), golomb_delta_min_encodings[i]['bit_len']/(points+2)))
        if big_delta_min_encoding['bit_len']/points <= golomb_delta_min_encodings[i]['bit_len']/points:
            bigwin += 1
        else:
            golwin += 1
    print '#instances BIGNUM bettter: %d, #instances Golomb better: %d' % (bigwin, golwin)
    all_out.close()
    helpers.write_summary('./results/delta_min_summary', stats, algos, '_delta_min_') 
    helpers.write_summary('./results/delta_summary', stats, algos, '_delta_') 

if __name__ == "__main__":
    main()
