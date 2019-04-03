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

# Utilites
import sys, os, re, gzip, glob

def main():
    path = sys.argv[1]
    for gzipped in glob.glob(os.path.join(path, '*.gz')):
        uncompressed = re.sub('.gz$', '.json', gzipped)
        with gzip.open(gzipped, 'rb') as g:
            uncompressed_file_contents = g.read()
            with open(uncompressed, 'wb') as u:
                u.write(uncompressed_file_contents)

if __name__ == '__main__':
    sys.exit(main())