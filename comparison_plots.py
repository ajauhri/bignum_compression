from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import pandas 
from collections import defaultdict
from pylab import *
import sys

def plot_all(t, labels):
    df = pandas.read_csv('results/all.csv', skiprows=[1])
    varrsd = []
    var = []
    big = []
    orig = []
    lzw = []
    golomb = []
    huffman = []
    x = []
    for count, row in df.iterrows():
        x.append(row['points'])
        big.append(row['big_' + t + '_len'])
        varrsd.append(row['varrsd_' + t + '_len'])
        var.append(row['var_' + t + '_len'])
        lzw.append(row['lzw_' + t + '_len'])
        golomb.append(row['golomb_' + t + '_len'])
        huffman.append(row['huffman_' + t + '_len'])
        orig.append(row['orig_len'])

    x = np.array(x)
    ind = np.argsort(x)
    big = np.array(big)[ind]
    varrsd = np.array(varrsd)[ind]
    var = np.array(var)[ind]
    lzw = np.array(lzw)[ind]
    golomb = np.array(golomb)[ind]
    huffman = np.array(huffman)[ind]
    orig = np.array(orig)[ind]
    x = x[ind]
    colors = cm.rainbow(np.linspace(0, 1, 6))
    huffman_l = plt.scatter(x-.4, huffman, color=colors[2], alpha=1, marker='*')
    golomb_l = plt.scatter(x-.1, golomb, color='green', alpha=1, marker='*')
    lzw_l = plt.scatter(x+.1, lzw, color=colors[3], alpha=1, marker='*')
    big_l = plt.scatter(x-.2, big, color=colors[0], alpha=1, marker='+')
    varrsd_l = plt.scatter(x+.4, varrsd, color=colors[1], alpha=1)
    var_l = plt.scatter(x+.2, var, color=colors[5], alpha=1, marker='*')
    orig_l = plt.scatter(x, orig, color=colors[4])
    plt.legend((big_l, varrsd_l, var_l, orig_l, lzw_l, golomb_l, huffman_l), labels, loc='upper left')
    plt.ylim(0, 350)
    plt.xlim(0, 28)
    plt.xlabel('# of points')
    plt.ylabel('Length')
    savefig('results/all_' + t + '.png')
    plt.clf()

def plot_best(t, labels):
    df = pandas.read_csv('results/all.csv', skiprows=[1])
    big = []
    golomb = []
    vsimple = []
    simd = []
    x = []
    golomb_dict = defaultdict(list)
    big_dict = defaultdict(list)
    vsimple_dict = defaultdict(list)
    simd_dict = defaultdict(list)

    for count, row in df.iterrows():
        if t == 'del':
            arr_len = row['points'] * 2
            x.append(row['points']*2)
        elif t == 'diff':
            arr_len = (row['points']-1) * 2
            x.append(arr_len)
        big.append(row['big_' + t + '_bits'])
        big_dict[arr_len].append(big[-1])
        golomb.append(row['golomb_' + t + '_bits'])
        golomb_dict[arr_len].append(golomb[-1])
        import os
        if os.path.isfile('results/' + t + '_state_of_art/' + str(count+1) + '.out'):
            fd = file('results/' + t + '_state_of_art/' + str(count+1) + '.out', 'r')
            for line in fd.readlines():
                if 'VSimple' in line:
                    vsimple.append(float(line.split()[3]))
                if 'SIMDPackFPF' in line:
                    simd.append(float(line.split()[3]))

            fd.close()
            vsimple_dict[arr_len].append(vsimple[-1])
            simd_dict[arr_len].append(simd[-1])
        else:
            print 'error'
            break


    x = np.array(x)
    big = np.array(big)
    golomb = np.array(golomb)
    vsimple = np.array(vsimple)
    simd = np.array(simd)
    ind = np.argsort(x)
    x = x[ind]
    big = big[ind]
    golomb = golomb[ind]
    simd = simd[ind]
    vsimple = vsimple[ind]
    colors = cm.rainbow(np.linspace(0, 1, 5))
    big_l = plt.scatter(x, big, color=colors[3], alpha=1, marker='d', s=10)
    golomb_l = plt.scatter(x+.4, golomb, color='green', alpha=1, marker='+', s=10)
    vsimple_l = plt.scatter(x-.4, vsimple, color=colors[0], alpha=1, marker='s', s =10)
    simd_l = plt.scatter(x-.8, simd, color=colors[4], alpha=1, marker='v', s=10)
    plt.legend((big_l, golomb_l, vsimple_l, simd_l), labels, loc='upper left')
    plt.ylim(0, 25)
    plt.xlim(0, 50)
    plt.xlabel('number of integers', fontsize=22)
    plt.ylabel('bits/integer', fontsize=22)
    plt.tight_layout()
    savefig('results/best_' + t + '.png')
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.ylim(0, 25)
    plt.xlim(0, 50)
    plt.xlabel('number of integers', fontsize=22)
    plt.ylabel('bits/integer', fontsize=22)
    plt.tight_layout()
    for k,v in big_dict.iteritems():
        ax.errorbar(k, np.mean(big_dict[k]), np.std(big_dict[k]), linestyle='None', marker='d', color=colors[3], label=labels[0])
        ax.errorbar(k+.4, np.mean(golomb_dict[k]), np.std(golomb_dict[k]), linestyle='None', marker='+', color='green', label=labels[1])
        ax.errorbar(k-.4, np.mean(vsimple_dict[k]), np.std(vsimple_dict[k]), linestyle='None', marker='s', color=colors[0], label=labels[2])
        ax.errorbar(k-.8, np.mean(simd_dict[k]), np.std(simd_dict[k]), linestyle='None', marker='v', color=colors[4], label=labels[3])

    handles, _ = ax.get_legend_handles_labels()
    handles = [h[0] for h in handles]
    ax.legend(handles, labels, loc='upper left')
    savefig('results/best2_' + t + '.png')
    plt.clf()

def plot_diff(t, labels):
    df = pandas.read_csv('results/all.csv', skiprows=[1])
    big = []
    golomb = []
    x = []
    for count, row in df.iterrows():
        x.append(count)
        big.append(row['big_' + t + '_bits'])
        golomb.append(row['golomb_' + t + '_bits'])

    x = np.array(x)
    big = np.array(big)
    golomb = np.array(golomb)
    ind = np.argsort(x)
    x = x[ind]
    big = big[ind]
    golomb = golomb[ind]
    colors = cm.rainbow(np.linspace(0, 1, 5))
    big_l = plt.scatter(x-.2, big, color=colors[3], alpha=1, marker='+')
    golomb_l = plt.scatter(x+.2, golomb, color='green', alpha=1, marker='*')
    #huffman_l = plt.scatter(x-.4, huffman, color=colors[0], alpha=1, marker='*')
    plt.legend((big_l, golomb_l), labels, loc='upper left')
    plt.ylim(0, 15)
    plt.xlim(-100, 11500)
    plt.xlabel('# of vertices', fontsize=22)
    plt.ylabel('bits/integer', fontsize=22)
    plt.tight_layout()
    savefig('results/diff_' + t + '.png')
    plt.clf()


plot_best('diff', (r'$BIG^{\Delta}$', r'$GOL^{\Delta}$', r'$VSimple^{\Delta}$', r'$SIMDPackFPF^{\Delta}$'))
plot_best('del', (r'$BIG^{\Delta min}$', r'$GOL^{\Delta min}$', r'$VSimple^{\Delta min}$', r'$SIMDPackFPF^{\Delta min}$'))
#plot_diff('del', (r'$BIG^{\Delta min}$', r'$GOL^{\Delta min}$'))
#plot_foo()
