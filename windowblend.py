#!/usr/bin/env python

#from __future__ import print_function
import numpy as np
from PIL import Image
import glob
import argparse
from collections import deque
import subprocess as sp

ap = argparse.ArgumentParser()

ap.add_argument('--inglob', help = 'input files glob', type = str)
ap.add_argument('--windowsize', help = 'window size', type = int)
ap.add_argument('--attack', help = 'attack and release length', type = int)
ap.add_argument('--ffmpegoutopts', help = 'ffmpeg output options, like c:v. comma-separated.', type = str)
ap.add_argument('outfile', help = 'output file', type = str)

ap.set_defaults(
    inglob = './*',
    windowsize = 10,
    attack = 0,
    ffmpegoutopts = '-c:v,libx264rgb,-qp,18,-preset,veryfast'
    )
args = ap.parse_args()

infiles = sorted(glob.glob(args.inglob))

firstimg = Image.open(infiles[0])
w, h = firstimg.size
firstimg.close()
del firstimg

print('size: %d x %d' % (w, h))

args.attack = args.attack if args.attack >= 0 else round(args.windowsize/(-args.attack))
weights = [(x + 1) / args.attack if x < args.attack else (args.windowsize - x) / args.attack if x > args.windowsize - args.attack else 1 for x in range(args.windowsize)]


print('weights', weights)

command = [ 'ffmpeg',
    #'-y', # (optional) overwrite output file if it exists
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-s', '%dx%d' % (w, h),
    '-pix_fmt', 'rgb24',
    '-r', '25',
    '-i', '-', '-an'
    ]
command.extend(args.ffmpegoutopts.split(','))
command.extend([args.outfile])

print('command', command)

ffpipe = sp.Popen(command, stdin = sp.PIPE)#, stderr = sp.PIPE)

window = deque([])

for infile in infiles:
    try:
        pilimg = Image.open(infile)
        iw, ih = pilimg.size
        if iw != w or ih != h:
            print('sizes dont match %dx%d, excepted %dx%d' % (iw, ih, w, h))
            continue
        img = np.asarray(pilimg)
        if img.shape != (h, w, 3):
            print('numpy convert error', img.shape, infile)
            continue
    except IOError:
        print('read error', infile)
        continue
    if len(window) == args.windowsize:
        try:
            avgimg = np.average(window, 0, weights)
            ffpipe.stdin.write(avgimg.astype('uint8').tostring())
        except TypeError:
            #for sw in window: print(type(sw))
            print('average type error', infile)
            print(type(window[-1]), window[-1].shape)
            del window[-1]
    window.append(img)
    if len(window) > args.windowsize:
        popped = window.popleft()
        del popped

        
