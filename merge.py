#! /usr/bin/env python

import montage_wrapper
import sys,os


if '/' in sys.argv[1]:
    montage_wrapper.mosaic(sys.argv[1][:-1],'mosaic')
    os.system('mv mosaic/mosaic.fits ../{}.fits'.format(sys.argv[1][:-1]))
else:
    montage_wrapper.mosaic(sys.argv[1],'mosaic')
    os.system('mv mosaic/mosaic.fits {}.fits'.format(sys.argv[1]))

os.system('rm -r mosaic')
