#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 13:31:59 2018

@author: chinwei
"""

import urllib
import cPickle as pickle
import gzip
import os
import numpy as np
import zipfile
import scipy.ndimage


final_size = 64


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--savedir', type=str, default='datasets', 
                        help='directory to save the dataset')
    args = parser.parse_args()

    if not os.path.exists(args.savedir):
        os.makedirs(args.savedir)

    urlpath = 'https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip'
    filename  = 'train.zip'
    filepath = os.path.join(args.savedir, filename)
    print "Downloading..."
    urllib.urlretrieve(urlpath, filepath)

    print "Extracting file..."
    zip_ref = zipfile.ZipFile(filepath, 'r')
    zip_ref.extractall(args.savedir)
    zip_ref.close()

    train_data = os.path.join(args.savedir, 'train')
    train_proc_data = os.path.join(args.savedir, 'train_64x64')
    if not os.path.exists(train_proc_data):
        os.makedirs(train_proc_data)

    for pic_file in os.listdir(train_data):
        pic_path = os.path.join(train_data, pic_file)
        img = scipy.ndimage.imread(pic_path)
        side_dim = min(img.shape[0], img.shape[1])
        start_height = (img.shape[0] - side_dim) // 2
        start_width = (img.shape[1] - side_dim) // 2
        img = img[start_height: start_height + side_dim,
                  start_width: start_width + side_dim]
        img = scipy.misc.imresize(
            img,
            size=(final_size, final_size),
            interp='bilinear'
        )


        #if (img.shape[0] > final_size or
        #    img.shape[1] > final_size):
        #    img = img[:final_size, :final_size]
        assert(img.shape[0] == final_size and
               img.shape[1] == final_size)



        scipy.misc.imsave(
            os.path.join(train_proc_data, pic_file),
            img
        )

