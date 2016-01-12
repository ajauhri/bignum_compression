#! /usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import pandas 
from collections import defaultdict
from pylab import *
import sys
import helpers
import scipy.stats
import const

results_dir = "results/"

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%d'%int(height), fontsize=8,
                ha='center', va='bottom')

def plot_deltas_length(rows):
    d = defaultdict(int)
    for i in rows:
        t = i['trans_poly']
        penultimate_comma = t.rfind(',', 0, t.rfind(','))
        t = t[:penultimate_comma]
        d[len(t)] += 1
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel('length(in characters)')
    plt.ylabel('#count')
    plt.xlim([0, 350])
    plt.ylim([0, 3250])
    savefig(results_dir + 'polygon_del_c_length.png')
    plt.clf()

def plot_diff_length(rows):
    d = defaultdict(int)
    for i in range(len(rows)):
        orig_poly = rows[i]['orig_poly']
        orig_poly = orig_poly[:orig_poly.rfind(' ')]
        diff_polygon = helpers.transform(helpers.get_diff_polygon(orig_poly))
        d[len(diff_polygon)] += 1
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel('length(in characters)')
    plt.ylabel('#count')
    plt.xlim([0, 350])
    plt.ylim([0, 3250])
    savefig(results_dir + 'polygon_diff_c_length.png')
    plt.clf()

def plot_poly_length(rows):
    d = defaultdict(int)
    for i in rows:
        d[len(i['orig_poly'])] += 1
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel('length(in characters)')
    plt.ylabel('#count')
    plt.xlim([0, 350])
    plt.ylim([0, 1000])
    savefig(results_dir + 'polygon_length.png')
    plt.clf()

def plot_diff_y_w_negs(rows):
    d = defaultdict(int)
    for i in range(len(rows)):
        orig_poly = rows[i]['orig_poly']
        orig_poly = orig_poly[:orig_poly.rfind(' ')]
        diff_polygon = helpers.get_diff_polygon(orig_poly)
        diffs = np.array(diff_polygon.split(','), dtype='int')
        for v in range(2, len(diffs), 2):
            d[diffs[v+1]] += 1
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel(r'$\Delta$Y')
    plt.ylabel('#count')
    plt.xlim([-270, 270])
    plt.ylim([0, 11000])
    #print 'Skewness of ' + r'$\Delta$' + 'Y: %f' % scipy.stats.skew(d.values())
    #print 'Kurtosis of ' + r'$\Delta$' + 'Y: %f' % scipy.stats.kurtosis(d.values())
    #print 'count max: %d' % max(d.values())
    #print r'$\Delta$Y' + ' min: %d; max: %d' % (min(d.keys()), max(d.keys()))
    savefig(results_dir + 'polygon_diff_y_w_negs.png')
    plt.clf()


def plot_diff_x_w_negs(rows):
    d = defaultdict(int)
    for i in range(len(rows)):
        orig_poly = rows[i]['orig_poly']
        orig_poly = orig_poly[:orig_poly.rfind(' ')]
        diff_polygon = helpers.get_diff_polygon(orig_poly)
        diffs = np.array(diff_polygon.split(','), dtype='int')
        for v in range(2, len(diffs), 2):
            d[diffs[v]] += 1
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel(r'$\Delta$X')
    plt.ylabel('#count')
    plt.xlim([-270, 270])
    plt.ylim([0, 11000])

    #print 'Skewness of ' + r'$\Delta$' + 'X: %f' % scipy.stats.skew(d.values())
    #print 'Kurtosis of ' + r'$\Delta$' + 'X: %f' % scipy.stats.kurtosis(d.values())
    #print 'count max: %d' % max(d.values())
    #print r'$\Delta$X' + ' min: %d; max: %d' % (min(d.keys()), max(d.keys())) 
    savefig(results_dir + 'polygon_diff_x_w_negs.png')
    plt.clf()

def plot_diff_x(rows):
    d = defaultdict(int)
    count = 0
    for i in range(len(rows)):
        orig_poly = rows[i]['orig_poly']
        orig_poly = orig_poly[:orig_poly.rfind(' ')]
        diff_polygon = helpers.transform(helpers.get_diff_polygon(orig_poly))
        diffs = np.array(diff_polygon.split(','), dtype='int')
        for v in range(2, len(diffs), 2):
            if diffs[v] > 0:
                d[diffs[v]] += 1
            else:
                count += 1
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel(r'$\Delta X_i$', fontsize=22)
    plt.ylabel('#count', fontsize=22)
    plt.xlim([0, 530])
    plt.ylim([0, 5700])
    plt.tick_params(axis='both', which='major', labelsize=22)
    plt.tight_layout()
    print '***deltaXi***'
    print 'Skewness: %f' % scipy.stats.skew(d.values())
    print 'Kurtosis: %f' % scipy.stats.kurtosis(d.values())
    print 'count max: %d' % max(d.values())
    print 'count zero: %d' % count
    print 'min: %d; max: %d' % (min(d.keys()), max(d.keys()))
    print '***deltaXi***'
    savefig(results_dir + 'polygon_diff_x.png')
    plt.clf()

def plot_diff_y(rows):
    d = defaultdict(int)
    count = 0
    for i in range(len(rows)):
        orig_poly = rows[i]['orig_poly']
        orig_poly = orig_poly[:orig_poly.rfind(' ')]
        diff_polygon = helpers.transform(helpers.get_diff_polygon(orig_poly))
        diffs = np.array(diff_polygon.split(','), dtype='int')
        for v in range(2, len(diffs), 2):
            if diffs[v+1] > 0: 
                d[diffs[v+1]] += 1
            else:
                count += 1

    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel(r'$\Delta Y_i$', fontsize=22)
    plt.ylabel('#count', fontsize=22)
    plt.xlim([0, 530])
    plt.ylim([0, 5700])
    plt.tick_params(axis='both', which='major', labelsize=22)
    plt.tight_layout()
    print '***deltaYi***'
    print 'Skewness: %f' % scipy.stats.skew(d.values())
    print 'Kurtosis: %f' % scipy.stats.kurtosis(d.values())
    print 'count max: %d' % max(d.values())
    print 'zero count: %d' % count
    print 'min: %d; max: %d' % (min(d.keys()), max(d.keys())) 
    print '***deltaYi***'
    savefig(results_dir + 'polygon_diff_y.png')
    plt.clf()

def plot_deltas_x(rows):
    d = defaultdict(int)
    count = 0
    for i in rows:
        deltas = np.array(i['trans_poly'].split(',')[2:-2], dtype='int')
        for v in range(0, len(deltas), 2):
            if deltas[v] > 0:
                d[deltas[v]] += 1
            else:
                count += 1
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel(r'$dX_i$', fontsize=22)
    plt.ylabel('#count', fontsize = 22)
    plt.xlim([0, 530])
    plt.ylim([0, 5700])
    plt.tick_params(axis='both', which='major', labelsize=22)
    plt.tight_layout()
    print '***dXi***'
    print 'Skewness: %f' % scipy.stats.skew(d.values())
    print 'Kurtosis: %f' % scipy.stats.kurtosis(d.values())
    print 'count max: %d' % max(d.values())
    print 'zero count: %d' % count
    print 'min: %d; max: %d' % (min(d.keys()), max(d.keys())) 
    print '***dXi***'
    savefig(results_dir + 'polygon_deltas_x.png')
    plt.clf()


def plot_deltas_y(rows):
    d = defaultdict(int)
    count = 0
    for i in rows:
        deltas = np.array(i['trans_poly'].split(',')[2:-2], dtype='int')
        for v in range(0, len(deltas), 2):
            if deltas[v+1] > 0:
                d[deltas[v+1]] += 1
            else:
                count += 1
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel(r'$dY_i$', fontsize=22)
    plt.ylabel('#count', fontsize=22)
    plt.xlim([0, 530])
    plt.ylim([0, 5700])
    plt.tick_params(axis='both', which='major', labelsize=22)
    plt.tight_layout()
    print '***dYi***'
    print 'Skewness: %f' % scipy.stats.skew(d.values())
    print 'Kurtosis: %f' % scipy.stats.kurtosis(d.values())
    print 'count max: %d' % max(d.values())
    print 'zero count: %d' % count
    print 'dYi min: %d; max: %d' % (min(d.keys()), max(d.keys())) 
    print '***dYi***'
    savefig(results_dir + 'polygon_deltas_y.png')
    plt.clf()

def plot_xmin(rows):
    d = defaultdict(int)
    min = 1000
    max = 0
    for i in rows:
        deltas = np.array(i['trans_poly'].split(',')[:2], dtype='int')
        deltas[0] -= const.x_origin
        d[deltas[0]] += 1
        if deltas[0] < min:
            min = deltas[0]
        if deltas[0] > max:
            max = deltas[0]
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel(r'$dX_{min}$', fontsize=22)
    plt.ylabel('#count', fontsize=22)
    plt.xlim([0, 10000])
    plt.ylim([0, 60])
    plt.tick_params(axis='both', which='major', labelsize=22)
    plt.tight_layout()
    print 'Min dxmin: %d, max dxmin: %d' % (min, max)
    savefig(results_dir + 'xmin.png')
    plt.clf()

def plot_ymin(rows):
    d = defaultdict(int)
    min = 10000
    max = 0
    for i in rows:
        deltas = np.array(i['trans_poly'].split(',')[:2], dtype='int')
        deltas[1] -= const.y_origin
        d[deltas[1]] += 1
        if deltas[1] < min:
            min = deltas[1]
        if deltas[1] > max:
            max = deltas[1]
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel(r'$dY_{min}$', fontsize=22)
    plt.ylabel('#count', fontsize=22)
    plt.xlim([0, 10000])
    plt.ylim([0, 60])
    plt.tick_params(axis='both', which='major', labelsize=22)
    plt.tight_layout()
    print 'Min dymin: %d, max dymin: %d' % (min, max)
    savefig(results_dir + 'ymin.png')
    plt.clf()

def plot_x1(rows):
    d = defaultdict(int)
    min = 1000000
    max = 0
    for i in range(len(rows)):
        orig_poly = rows[i]['orig_poly']
        orig_poly = orig_poly[:orig_poly.rfind(' ')]
        diff_polygon = helpers.transform(helpers.get_diff_polygon(orig_poly))
        diffs = np.array(diff_polygon.split(','), dtype='int')
        d[diffs[0]] += 1
        if diffs[0] < min:
            min = diffs[0]
        if diffs[0] > max:
            max = diffs[0]
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel(r'$X_1$', fontsize=22)
    plt.ylabel('#count', fontsize=22)
    plt.xlim([0, 10000])
    plt.ylim([0, 60])
    plt.tick_params(axis='both', which='major', labelsize=22)
    plt.tight_layout()
    print 'Min X1: %d, max X1: %d' % (min, max)
    savefig(results_dir + 'x1.png')
    plt.clf()

def plot_y1(rows):
    d = defaultdict(int)
    min = 1000000
    max = 0
    for i in range(len(rows)):
        orig_poly = rows[i]['orig_poly']
        orig_poly = orig_poly[:orig_poly.rfind(' ')]
        diff_polygon = helpers.transform(helpers.get_diff_polygon(orig_poly))
        diffs = np.array(diff_polygon.split(','), dtype='int')
        d[diffs[1]] += 1
        if diffs[1] < min:
            min = diffs[1]
        if diffs[1] > max:
            max = diffs[1]
    plt.bar(d.keys(), d.values(), align='center', color='black')
    plt.xlabel(r'$Y_1$', fontsize=22)
    plt.ylabel('#count', fontsize=22)
    plt.xlim([0, 10000])
    plt.ylim([0, 60])
    plt.tick_params(axis='both', which='major', labelsize=22)
    plt.tight_layout()
    print 'Min Y1: %d, max Y1: %d' % (min, max)
    savefig(results_dir + 'y1.png')
    plt.clf()


def plot_poly_vertices_count(rows):
    d = defaultdict(int)
    for i in rows:
        v = int(i['vertices'])
        d[v] += 1
    rects = plt.bar(d.keys(), d.values(), align='center', color='black')
    autolabel(rects)
    plt.xlabel('no. of vertices')
    plt.ylabel('polygon count')
    savefig(results_dir + 'polygon_vertices_count.png')
    plt.clf()
