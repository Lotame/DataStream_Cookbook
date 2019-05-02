# The first bake...
#### ...or how I started to make sense of all these DataStream files...

So I've got some DataStream files downloaded. 

That's neat. It would be neater if I could do something with them.

Before I can do some neat stuff, I've got to get these files into some kind of format I can work with. 

Looks like these files are all `.gz`... compressed gzipped files. I'll need to uncompress them before I can see what the data looks like and decide how to do neat things.

#### ~30 minutes and a few ingredients...
1. Python version
    
    `2.7` or `3.6`

2. Python modules 
    
    `sys`, `os`, `re`, `gzip`, `glob`, `json`, `argparse`

3. A sense of adventure and awe of the unknown


#### ...will yield...
* A python-based extractor for gzip compressed Lotame Data Stream files
* A python-based json-to-csv convertor for uncompressed Lotame Data Stream files 


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
{"id":{"val":"abc123","type":"mobile","sub_type":"GAID"},"country":"US","region":"na","events":[{"tap":"DEVICE","c":1234,"ts":1552640493,"add":[987,81283712]}]}
{"id":{"val":"abc456","type":"mobile","sub_type":"SHA1"},"country":"US","region":"na","events":[{"tap":"DEVICE","c":1234,"ts":1552640637,"add":[987,718237,18283]}]}
{"id":{"val":"abc789","type":"mobile","sub_type":"SHA1"},"country":"US","region":"na","events":[{"tap":"DEVICE","c":1234,"ts":1552640775,"add":[718213,987,3462]}]}
{"id":{"val":"def123","type":"mobile","sub_type":"IDFA"},"country":"US","region":"na","events":[{"tap":"DEVICE","c":1234,"ts":1552640876,"remove":[9971238]}]}
{"id":{"val":"def456","type":"mobile","sub_type":"GAID"},"country":"US","region":"na","events":[{"tap":"DEVICE","c":1234,"ts":1552643600,"add":[987,87123,3218738,2758912]}]}
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


## JsonToCsvConverter.py
`.json` grandeur... who am I kidding. I mean, don't get me wrong... JSON is a pretty cool guy. He's organized, explains himself well, and is pretty flexible at handling a lot of different scenarios thrown at him.

But, and this is a pretty big BUT, I cannot lie...  a lot of the basic analysis tools these days run on SQL, and SQL doesn't play nicely with JSON. Don't blame JSON though, it's not his fault.

There's a solution, though. I just have to reach out to JSON's grandfather, CSV. He's not as flexible, sometimes harder to understand, and a bit rougher around the edges. That said, when it comes to loading data into relational databases, he's typically the one you want around.

So, I'm going to take a crack at converting this JSON to CSV. The handoff isn't entirely without decisions, though, because JSON is a nested structure and CSV is inherently flat unless you want to embed some potentially messy fields into the mix like arrays or, even, JSON again. 

I don't want to do that, so I'm going to take the approach of flattening the data out completely. It'll create more duplication, but I can easily use my query engines to aggregate what I want later on.

OK, enough already with the attempted elocution, I'm going to start writing some of that code stuff.

---
Just like before, I can use Python's `glob` to operate on a set of files in a directory. 

First, I'll want to open and read each `.json` file, and, at the same time, create a new file so I can write the `.csv` output. For now, I'll just print out all the fields I find from a couple of lines of each file, so I can make a plan with how to handle each one.

```python
path="/directory/containing/my/json/files/"
for json_file in glob.glob(os.path.join(path, '*.json')):
        csv_file = re.sub('.json$', '.csv', json_file)
        with open(json_file, 'rb') as jf:
            with open(csv_file, 'a') as cf:
                for i,line in enumerate(jf):
                    if i>=2:
                        break
                    json_line = json.loads(line)
                    print(json_line)
```

```python
{u'country': u'US', u'region': u'na', u'id': {u'type': u'cookie', u'val': u'abc123'}, u'events': [{u'c': 1234, u'add': [187293, 1872, 987, 612729, 9184], u'tap': u'DEVICE', u'ts': 1552646987}]}
{u'country': u'CA', u'region': u'na', u'id': {u'type': u'cookie', u'val': u'abc456'}, u'events': [{u'c': 1234, u'add': [817263, 7765, 987, 918264, 14198343, 38496, 9184], u'tap': u'DEVICE', u'ts': 1552646990}]}
{u'country': u'US', u'region': u'na', u'id': {u'type': u'mobile', u'sub_type': u'GAID', u'val': u'abc789'}, u'events': [{u'c': 1234, u'add': [987], u'tap': u'DEVICE', u'ts': 1552639810}]}
{u'country': u'US', u'region': u'na', u'id': {u'type': u'mobile', u'sub_type': u'SHA1', u'val': u'def123'}, u'events': [{u'c': 1234, u'add': [987, 540, 776152], u'tap': u'DEVICE', u'ts': 1552639882}]}
{u'country': u'US', u'region': u'na', u'id': {u'type': u'cookie', u'val': u'def456'}, u'events': [{u'c': 1234, u'add': [13387, 129873, 7829734, 23484, 23984, 8127347, 1237], u'tap': u'DEVICE', u'ts': 1552657490}]}
{u'country': u'CA', u'region': u'na', u'id': {u'type': u'cookie', u'val': u'def789'}, u'events': [{u'c': 1234, u'add': [2174678, 623748, 2438975, 2348, 918264, 38496, 81283], u'tap': u'DEVICE', u'ts': 1552657702}]}
```

Nice, OK, good stuff. 

I'll need to deal with those array fields in order to make a flat CSV file. I'll concentrate on those first.

---

Looks like the only arrays I can find are contained in the `events` field, so I'm going to unpack that a bit... multiple events per line, each with a `c` and `ts` (i.e. client and timestamp), and each with potentially multiple `add`'s or `remove`'s. 

This calls for the mighty for loop, and so for loop I shall.

```python
path="/directory/containing/my/json/files/"
for json_file in glob.glob(os.path.join(path, '*.json')):
        csv_file = re.sub('.json$', '.csv', json_file)
        with open(json_file, 'rb') as jf:
            with open(csv_file, 'a') as cf:
                for i,line in enumerate(jf):
                    if i>=2:
                        break
                    json_line = json.loads(line)
                    for event in json_line['events']:
                        client=event['c']
                        timestamp=event['ts']
                        if 'add' in event:
                            print("Found an Add")
                        if 'remove' in event:
                            print("Found a Remove")
```

```python
Found an Add
Found a Remove
Found an Add
Found an Add
Found an Add
Found a Remove
```

Well, it seems good at finding things. Maybe not Nemo, but certainly `add`'s and `remove`'s. And, in this particular case, finding actionable data is better than finding fish.

---

Now, in order to flatten this out to a `.csv`, I'll want to generate a line for every add and remove. There's also a host of other fields I want to write out to `.csv`, so I'll need to save those off as I go, like I've done before, so I can write them out later.

```python
for json_file in glob.glob(os.path.join(path, '*.json')):
        csv_file = re.sub('.json$', '.csv', json_file)
        with open(json_file, 'rb') as jf:
            with open(csv_file, 'a') as cf:
                for i,line in enumerate(jf):
                    if i>=2:
                        break
                    json_line = json.loads(line)
                    profile_id = json_line['id']['val']
                    profile_type = json_line['id']['type']
                    country = json_line['country']
                    region = json_line['region']
                    for event in json_line['events']:
                        client=event['c']
                        timestamp=event['ts']
                        if 'add' in event:
                            csv_file.write(str(profile_id)+","+str(profile_type)+","+str(region)+","+str(country)+","+str(client)+","+str(behavior)+","+str(timestamp)+","+"add")
                        if 'remove' in event:
                            csv_file.write(str(profile_id)+","+str(profile_type)+","+str(region)+","+str(country)+","+str(client)+","+str(behavior)+","+str(timestamp)+","+"remove")
```

OK, now we're talking CSV's language. This gives me a nice, flattened set of data organized into rows that pretty much any data storage solution can import straight out of the box.

---

There's some code duplication in there though, and it'd be nice to write a CSV header in case I don't remember which field is what. 

I also really want to wrap this in yet another bash executable, just so I can run it with cron, or automate it in some other fashionable style.

```python
#!/usr/bin/python
#
# Filename: 
#
#     JsonToCsvConverter.py
#
#
# Basic Usage:
#
#     python JsonToCsvConverter.py /directory/containing/datastream/json/files
#

# Utilities
import sys, os, re, glob, json

def writeCsvHeader(csv_file=None):
    csv_file.write("id,type,region,country,client_id,behavior_id,timestamp,action")
    csv_file.write("\n")

def writeCsvLine(csv_file=None,wrote_header=False,profile_id="",profile_type="",region="",country="",client="",behavior="",timestamp="",add=True):
    if not wrote_header:
        writeCsvHeader(csv_file)
    add_string = "add" if add is True else "remove"
    csv_file.write(str(profile_id)+","+str(profile_type)+","+str(region)+","+str(country)+","+str(client)+","+str(behavior)+","+str(timestamp)+","+add_string)
    csv_file.write("\n")
    return True

def main():
    path = sys.argv[1]
    for json_file in glob.glob(os.path.join(path, '*.json')):
        csv_file = re.sub('.json$', '.csv', json_file)
        with open(json_file, 'rb') as jf:
            with open(csv_file, 'a') as cf:
                wrote_header=False
                for line in jf:
                    json_line = json.loads(line)
                    profile_id = json_line['id']['val']
                    profile_type = json_line['id']['type']
                    country = json_line['country']
                    region = json_line['region']
                    for event in json_line['events']:
                        client = event['c']
                        timestamp = event['ts']
                        if 'add' in event:
                            for behavior in event['add']:
                                wrote_header = writeCsvLine(csv_file=cf,wrote_header=wrote_header,profile_id=profile_id,profile_type=profile_type,region=region,country=country,client=client,behavior=behavior,timestamp=timestamp,add=True)
                        if 'remove' in event:
                            for behavior in event['remove']:
                                wrote_header = writeCsvLine(csv_file=cf,wrote_header=wrote_header,profile_id=profile_id,profile_type=profile_type,region=region,country=country,client=client,behavior=behavior,timestamp=timestamp,add=False)

if __name__ == '__main__':
    sys.exit(main())
```

There, that's much better. Now I have a self-documenting CSV that I can use pretty much anywhere I like. 

Onto the same thing I do every night- using this data to conquer the world...

...on second thought, maybe something simpler, like an Excel sheet. 

Or, maybe something fun, like a streaming data dashboard. 

Or... possibilities being their endless selves, now that I have usable Datastream data, I can concentrate on whatever maybes may come.

