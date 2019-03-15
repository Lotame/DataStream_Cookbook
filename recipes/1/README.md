# Recipe 1
#### ...or how I started to make sense of all these DataStream files...

So I've got some DataStream files downloaded. 

That's neat. It would be neater if I could do something with them.

Before I can do some neat stuff, I've got to get these files into some kind of format I can work with. 

Looks like these files are all `.gz`... compressed gzipped files. I'll need to uncompress them before I can see what the data looks like and decide how to do neat things.

## GzipExtractor.py

Thankfully trusty ol' Python includes some utilities to do just this, so I'ma launch it and gather my ingredients.

```bash
python
```


```python
import os, glob, re, gzip
```

`os` and `glob` give me some tools to access the file system

`re` gives me some regex tools for easy text wrangling

`gzip` lets me deal with gzipped files easily

---
I think I'm going to just test a file first to make sure this idea works.

`gzip.open()` reads a gzipped file and gives me back the uncompressed contents, so I'm going to try that and print out the result.
```python
gzipped = "/path/to/my/file.gz"
with gzip.open(gzipped, 'rb') as g:
    uncompressed_file_contents = g.read()
    print(uncompressed_file_contents)
```
```python
{"id":{"val":"e53a64e8-c7bb-46e4-a470-ff47d79dbaba","type":"mobile","sub_type":"GAID"},"country":"US","region":"na","events":[{"tap":"DEVICE","c":2215,"ts":1552640493,"add":[13114472,18832363]}]}
{"id":{"val":"1b82b3b5988944dcde9dee71bb1163a9082adbd2","type":"mobile","sub_type":"SHA1"},"country":"US","region":"na","events":[{"tap":"DEVICE","c":2215,"ts":1552640637,"add":[13114472,648193,24729421]}]}
{"id":{"val":"148fc1d44c1c4940fe1456e6cafc439fec88cc48","type":"mobile","sub_type":"SHA1"},"country":"US","region":"na","events":[{"tap":"DEVICE","c":2215,"ts":1552640775,"add":[648391,13114472,24729326]}]}
{"id":{"val":"9B85B613-84DA-42A6-9EEE-9ABF38528C28","type":"mobile","sub_type":"IDFA"},"country":"US","region":"na","events":[{"tap":"DEVICE","c":2215,"ts":1552640876,"remove":[62900413]}]}
{"id":{"val":"df4b3e44-e58f-4ccb-9789-241c4e2d87a9","type":"mobile","sub_type":"GAID"},"country":"US","region":"na","events":[{"tap":"DEVICE","c":2215,"ts":1552643600,"add":[13114472,18832363,648103,24729283]}]}
```
That worked... Cool, now onto making it useful.

self.note="Looks like JSON. I'll have to convert that into something more useful after I'm finished extracting all this gzipped goodness."

---
I really want to uncompress a bunch of files at once to save me time, so I'm going to tell Python to read all the `.gz` files in a directory.

`glob.glob()` will give me a list of file paths to iterate over, and `os.path.join()` lets me specify file paths with a directory and a wildcard, so I think I can use them both together to iterate over all the files in a directory.

```python
path="/directory/containing/my/files/"
for gzipped in glob.glob(os.path.join(path, '*.gz')):
    with gzip.open(gzipped, 'rb') as g:
        uncompressed_file_contents = g.read()
```

Nice, now Python can just read all the gzipped files in a directory without relying on me to find each and every one beforehand.

---
*Reading* is only half the battle, though... I still need to *write* the uncompressed text files somewhere, preferably with a new filename for each gzipped file that ends in `.json` to indicate the latent json power within.

I'll work on renaming the file with the `re` package. I can use the `re.sub()` method to easily replace parts of strings and get a new filename string I'll call `uncompressed`.

```python
path="/directory/containing/my/files/"
for gzipped in glob.glob(os.path.join(path, '*.gz')):
    uncompressed = re.sub('.gz$', '.json', gzipped)
    with gzip.open(gzipped, 'rb') as g:
        uncompressed_file_contents = g.read()
```

Now I just need to create that new `uncompressed` file and write the `uncompressed_file_contents` to it. 

```python
path="/directory/containing/my/files/"
for gzipped in glob.glob(os.path.join(path, '*.gz')):
        uncompressed = re.sub('.gz$', '.json', gzipped)
        with gzip.open(gzipped, 'rb') as g:
            uncompressed_file_contents = g.read()
            with open(uncompressed, 'w') as u:
                u.write(uncompressed_file_contents)
```
Sweet. This seems to be all Functional, Fine, and Good. 

---
But...

I'd like to just run this from the command line and give it a directory to work on, just so I can say I'm being productive while I stare out the window sipping on my 10th cup of coffee before 10am. 

I know, I'll wrap it in a bash executable python function.

```python
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

import sys, os, re, gzip, glob

def main():
    path = sys.argv[1]
    for gzipped in glob.glob(os.path.join(path, '*.gz')):
        uncompressed = re.sub('.gz$', '.json', gzipped)
        with gzip.open(gzipped, 'rb') as g:
            uncompressed_file_contents = g.read()
            with open(uncompressed, 'w') as u:
                u.write(uncompressed_file_contents)

if __name__ == '__main__':
    sys.exit(main())
```

There, now I can just do this
```bash
python GzipExtractor.py /directory/containing/my/files/
```
... and all that `.gz` goodness is now `.json` grandeur.
