#! /usr/bin/env python
from __future__ import division
import extras.helpers as helpers 
import extras.const as const
from optparse import OptionParser
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

def generate_indexes():
   ind=[]
   lower="abcdefghijklmnopqrstuvwxyz"
   upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
   digits="0123456789"
   special="!@$%^&*(){}[]|:;<>,.?/_-+=\\"
   for x in lower+upper+special :
       ind.append(x)
   for x in digits :
      for y in lower+upper+special:
       ind.append(x+y)
   for x in digits :
      for y in digits :
        for z in lower+upper+special :
          ind.append(x+y+z)
   return ind
 
def create_dictionary(data, size, step):
    hh = {}
    d = defaultdict(int)
    if type(step) is not list:
        step = [step]
    for s in step:
        for line in data:
            words = line.split()
            wc = len(words)
            for i in range(0, len(words) - (s - 1)):
                sub_str = ' '.join(words[i:i+s])
                d[sub_str] += 1
    i = 0
    while i < min(size, len(d)):
        v = max(d, key=d.get)
        # if v is a substrings then omit
        if any(v in x and d[v] <= c for x,c in hh.iteritems()):
            d[v] = 0
        # if v is longer then replace
        elif any(x in v and c <= d[v] for x,c in hh.iteritems()):
            for x,c in hh.iteritems():
                if x in v and c <= d[v]:
                    hh.pop(x, 0)
                    hh[v] = d[v]
                    d[v] = 0
                    break
        # otherwise simply add
        else:
            hh[v] = d[v]
            d[v] = 0
            i += 1
    result = {}
    #dict_elems = const.encode_values[:size]
    dict_elems = generate_indexes()
    i = 0
    for k,v in hh.iteritems():
        result[k] = dict_elems[i]
        #print k, v
        i += 1
    return result 

def fixed_compress(ifile):
    data = helpers.get_cmam_text(ifile)
    cmam = [x[1] for x in data]
    assert len(data) == len(cmam)
    x = []
    means = []
    errs = []
    for step in [1,2,3,4,5,6]: 
        d = create_dictionary(cmam, base, step)
        per = []
        for i in range(len(cmam)):
            msg = cmam[i]
            comp_str = ""
            words = msg.split()
            for j in xrange(0, len(words), step):
                sub_str = ' '.join(words[j:j+step])
                if sub_str in d:
                    comp_str += d[sub_str]
                else:
                    if len(comp_str) and comp_str[-1] == '#':
                        comp_str = comp_str[:-1] + " " + sub_str + "#"
                    else:
                        comp_str += "#" + sub_str + '#'
            per.append(len(comp_str)/len(msg))
            #print "id:%d, comp_len:%d, orig_len:%d, comp_per:%.4f " % (data[i][0], len(comp_str), len(msg), len(comp_str)/len(msg))
        print step, np.mean(per), np.std(per)
        x.append(step)
        means.append(np.mean(per))
        errs.append(np.std(per))
    plt.bar(x, means, .35, alpha=.4, yerr = errs, color = 'b')
    plt.xlabel('step size')
    plt.ylabel('mean compressed length')
    plt.savefig('text_comp_results.png')

def variable_compress(ifile, base):
    data = helpers.get_cmam_text(ifile)
    cmam = [x[1] for x in data]
    assert len(data) == len(cmam)
    steps = [1,2, 3]#, 4, 5, 6, 7, 8]
    d = create_dictionary(cmam, base, steps)
    inv_d = {v:k for k,v in d.items()}
    per = []
    lens = []
    #print "id_orig_compr_origlen_comprlen_ratio" 
    for i in range(len(cmam)):
        msg = cmam[i]
        comp_str = ""
        words = msg.split()
        j = 0
        while j < len(words):
            found = False
            for s in reversed(steps):
                sub_str = ' '.join(words[j:j+s])
                if sub_str in d:
                    found = True
                    comp_str += d[sub_str]
                    j = j + s
                    break
            if not found:
                if len(comp_str) and comp_str[-1] == '#':
                    comp_str = comp_str[:-1] + " " + sub_str + "#"
                else:
                    comp_str += "#" + sub_str + '#'
                j += 1
        #print "%d_%s_%s_%d_%d_%.4f" % (data[i][0], msg, comp_str, len(msg), len(comp_str), len(comp_str)/len(msg))
        #decoded_str = decode(comp_str, inv_d)
        #assert decoded_str == msg
        per.append(len(comp_str)/len(msg))
        lens.append(len(comp_str))
    print base, np.mean(per), np.std(per), np.min(lens), np.max(lens)
    return (np.mean(per), np.std(per))

def decode(c_str, inv_d):
    result = ""
    i = 0
    while i < len(c_str):
        if c_str[i] in inv_d:
            result += inv_d[c_str[i]] + ' '
            i += 1
        elif c_str[i] == '#':
            e = c_str[i+1:].find('#')
            result += c_str[i+1:e+i+1] + ' '
            i += e + 2
        elif c_str[i].isdigit():
            result += inv_d[c_str[i:i+2]] + ' '
            i += 2
    return result[:-1]

def start():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='ifile', help='input file')
    parser.add_option('-f', action='store_true', dest='fixed', help='fixed step size')
    parser.add_option('-v', action='store_true', dest='variable', help='variable step size')
    (options, args) = parser.parse_args()
    if not options.ifile:
        print 'all options not provided'
        exit(0)
    if not options.fixed and not options.variable:
        print 'should specify either fixed or variable step size'
        exit(0)
    helpers.setup_base()
    if options.fixed:
        fixed_compress(options.ifile)
    elif options.variable:
        r = variable_compress(options.ifile, 1000)

if __name__ == "__main__":
    start()
