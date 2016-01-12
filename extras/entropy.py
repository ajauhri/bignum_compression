# http://www.cs.berkeley.edu/~jrs/170/lec/compression.pdf 
# http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html 
import sys, math, string
import operator

'''
def H(data, iterator=range_printable):
    if not data:
        return 0
    entropy = 0
    for x in iterator():
        p_x = float(data.count(chr(x)))/len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return len(data) * entropy
    '''
def H(data):
    entropy = 0
    for x in set(data):
        p_x = float(data.count(x))/len(data)
        entropy += - p_x * math.log(p_x, 2)
    return entropy


def cal_probs(data):
    d = {}
    for x in set(data):
        p_x = float(data.count(x))/len(data)
        d[x] = p_x
    d = sorted(d.items(), key=operator.itemgetter(1), reverse=True) 
    return d



