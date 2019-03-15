#!/usr/bin/python
#
# Filename: 
#
#     GzipExtractor.py
#
#
# Basic Usage:
#
#     python GzipExtractor.py /directory/containing/datastream/gzip/files
#

# System Path
import sys
sys.path.append('../')

# Lotame
from lib import Lotame

# AWS

# Utilities
import os, re, gzip, glob

def main():
    path = sys.argv[1]
    for gzipped in glob.glob(os.path.join(path, '*.gz')):
        uncompressed = re.sub('.gz$', '.json', gzipped)
        with gzip.open(gzipped, 'rb') as g:
            file_content = g.read()
            with open(uncompressed, 'w') as u:
                u.write(file_content)

if __name__ == '__main__':
    sys.exit(main())