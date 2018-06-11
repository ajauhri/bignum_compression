#! /usr/bin/env python
# Copyright (c) 2018, Abhinav Jauhri, Martin Griss, Hakan Erdogmus
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import pandas 
from collections import defaultdict
from pylab import *
import sys
import os

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
        if t == 'delta_min':
            arr_len = row['points'] * 2
            x.append(row['points']*2)
        elif t == 'delta':
            arr_len = (row['points']-1) * 2
            x.append(arr_len)
        big.append(row['big_' + t + '_bits'])
        big_dict[arr_len].append(big[-1])
        golomb.append(row['golomb_' + t + '_bits'])
        golomb_dict[arr_len].append(golomb[-1])
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

plot_best('delta', (r'$BIG^{\Delta}$', r'$GOL^{\Delta}$', r'$VSimple^{\Delta}$', r'$SIMDPackFPF^{\Delta}$'))
plot_best('delta_min', (r'$BIG^{\Delta min}$', r'$GOL^{\Delta min}$', r'$VSimple^{\Delta min}$', r'$SIMDPackFPF^{\Delta min}$'))
