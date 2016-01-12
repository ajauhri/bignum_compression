
from __future__ import division
import sys, math
import cPickle as pickle
from fractions import Fraction

class DictOfDict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def cal_probs(k, lines):
    #fd = open(fname)
    #lines = fd.readlines()
    d = DictOfDict()
    d[0] = dict()
    d[0][''] = dict()
    d[0]['']['<$>'] = 0
    tot = 256
    entropy = 0

    for s in lines:
        # convert every symbol in line to bytes
        s_byte = ' '.join('{:08b}'.format(ord(c)) for c in s)
        arr_bytes = s_byte.split()
        ###print "byte array = ", arr_byte
        for j in xrange(0,len(arr_bytes)):
            start = j - k 
            if start < 0:
                start = 0
            end = j
            neg_rank = printed = False
            l = []
            while start <= end:
                s_prefix = ''.join(c for c in arr_bytes[start:end])
                len_prefix = int(len(s_prefix) / 8)

                # if length entry not in dictionary, make one
                if len_prefix not in d:
                    d[len_prefix] = dict()

                if s_prefix not in d[len_prefix]:
                    d[len_prefix][s_prefix] = dict()
                    d[len_prefix][s_prefix]['<$>'] = 1 
                    d[len_prefix][s_prefix][arr_bytes[j]] = 1

                elif s_prefix in d[len_prefix]:
                    # if the character already exists, then just increment the count
                    if arr_bytes[j] in d[len_prefix][s_prefix]:
                        num = den = 0
                        new_l = []
                        for key, value in d[len_prefix][s_prefix].iteritems():
                            if key not in l and key != '<$>':
                                den += value
                                new_l.append(key)

                        num = d[len_prefix][s_prefix][arr_bytes[j]] 
                        den += d[len_prefix][s_prefix]['<$>'] - len(l)
                        l = new_l + l
                        if den > 0 and not printed:
                            printed = True
                            entropy += (num/den)*math.log(1/(num/den), 2)
                        d[len_prefix][s_prefix][arr_bytes[j]] += 1
                        

                    elif arr_bytes[j] not in d[len_prefix][s_prefix]:
                        num = den = 0
                        new_l = []
                        for key, value in d[len_prefix][s_prefix].iteritems():
                            if key not in l and key != '<$>':
                                den += value
                                new_l.append(key)

                        num = d[len_prefix][s_prefix]['<$>'] - len(l)
                        den += d[len_prefix][s_prefix]['<$>'] - len(l)
                        l = new_l + l
                        if den > 0:
                            entropy += (num/den)*math.log(1/(num/den), 2)
                        d[len_prefix][s_prefix][arr_bytes[j]] = 1
                        d[len_prefix][s_prefix]['<$>'] += 1
                        if start == end:
                            neg_rank = True

                start += 1
            if neg_rank:
                entropy += (1/tot)*math.log(tot, 2)
                tot -= 1
    #print 'Total bits: %.1f' % entropy
    for p_l,v in d.iteritems():
        for p,j in v.iteritems():
            count = 0
            j.pop('<$>', None)
            for k,l in j.iteritems():
                if k != '<$>':
                    count += l
            for k,l in j.iteritems():
                d[p_l][p][k] = Fraction(l,count)#l/count
    return d
