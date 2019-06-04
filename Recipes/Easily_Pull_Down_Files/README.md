# Opening the pantry
#### ...or how I learned to stop worrying and love the Lotame API.........

I have access to this thing all the cool kids are talking about. 

It's called the Lotame API.

But I'm a programmer. And a pragmatist. So, to me, it's only cool if I can do cool things with it.

I also like Data. Like, like Data. Like, Big Data. 

This DataStream thing seems like a good place to start. 

Like all my Big Data projects, I'm going to finish Big by starting Small.

I think I'll start by trying to download some of these DataStream files, see what's what, and go from there.

#### ~30 minutes and a few ingredients...
1. Python version
    >`2.7` or `3.6`

2. Python modules 
    >`sys`, `boto3`, `botocore`
   
3. A tolerance for poor humor


#### ...will yield...
A python-based download utility for Lotame Data Stream files stored in s3.

- - -

NOTE: If this is the first recipe you're following make sure you have completed the [set up instructions](https://github.com/Lotame/DataStream_Cookbook/tree/master/Recipes/lib) found in the lib directory read me. You need to add your Lotame credentials to the lotame.properties file and put that file in the root of your home directory, ~/. You only need to do this step once in order to run all these recipes. 

If you get an error stating: `No section: 'default'` then you probably didn't take care of the lotame.properties file first. 

- - - 




## DataStreamDownloader.py

First, I need to access the LotameAPI. 

From the documentation [here](https://api.lotame.com/docs/), looks like it's a [REST service](https://en.wikipedia.org/wiki/Representational_state_transfer).

Also looks like there's a Python module called `Lotame` with a class called `FirehoseService` already built to help me access the Lotame DataStream, so I'll use that and see where it takes me.

```python
>>> import sys
>>> sys.path.append('../')
>>> from lib import Lotame
>>> firehose = Lotame.FirehoseService()
```

One of the methods in this class is called```getUpdates()```, and includes some time options. This looks promising, so I'll try to get the updates for the last hour and print them out.

```python
>>> updates = firehose.getUpdates(hours=1)
>>> print(updates)
```
```
[{u'feeds': [{u'files': [u'7d873ef1-8a03-4184-98e1-215095b28a89.gz', u'f7c09eaa-088a-48fc-9659-341df5de920d.gz', u'd95dff17-5932-4aa5-9ad5-584871e267a8.gz', u'009fda44-f681-4bed-8951-3bd0e08b5f6c.gz', u'9c5a66b5-a2a3-4841-8b75-bfd4f085553d.gz', u'0c1af5ce-1447-409c-a6b9-1a659a67b20c.gz', u'f260eede-967d-40ca-943e-b2268187d8a7.gz'], u'id': 112233, u'location': u's3://lotame-firehose/1234/na/cookie'}], u's3creds': {u'secretAccessKey': u'blah', u'sessionToken': u'blah', u'expiration': 1552700788000, u'accessKeyId': u'ASIAUQ6Z75CF2KID75GG'}}, {u'feeds': [{u'files': [u'7fb1c995-d3ac-4c68-b089-ce1847df886c.gz', u'259874b1-3114-427f-bef7-41ed23f95299.gz', u'e7453b95-a9bc-48dc-985f-a5b999697a83.gz', u'895e2ed9-3152-4c9b-893f-7ffd27710724.gz', u'cd15fd3e-fc36-4d48-b661-b74bc7d8ca72.gz', u'a5bb2f83-24a1-4433-8ed9-37203f64a30f.gz', u'2d558578-fa3f-4304-b3a6-e133a6964aeb.gz'], u'id': 446688, u'location': u's3://lotame-firehose/1234/na/mobile'}], u's3creds': {u'secretAccessKey': u'blah', u'sessionToken': u'blah', u'expiration': 1552700799000, u'accessKeyId': u'ASIAUQ6Z75CF4IAUVTUE'}}]
```

Looks like a list, so I'll iterate over it and print out each update individually.

```python
>>> for update in updates:
...     print(update)
```
```
{u'feeds': [{u'files': [u'7d873ef1-8a03-4184-98e1-215095b28a89.gz', u'f7c09eaa-088a-48fc-9659-341df5de920d.gz', u'd95dff17-5932-4aa5-9ad5-584871e267a8.gz', u'009fda44-f681-4bed-8951-3bd0e08b5f6c.gz', u'9c5a66b5-a2a3-4841-8b75-bfd4f085553d.gz', u'0c1af5ce-1447-409c-a6b9-1a659a67b20c.gz', u'f260eede-967d-40ca-943e-b2268187d8a7.gz'], u'id': 112233, u'location': u's3://lotame-firehose/1234/na/cookie'}], u's3creds': {u'secretAccessKey': u'blah', u'sessionToken': u'blah', u'expiration': 9999999999999, u'accessKeyId': u'blah'}}
{u'feeds': [{u'files': [u'7fb1c995-d3ac-4c68-b089-ce1847df886c.gz', u'259874b1-3114-427f-bef7-41ed23f95299.gz', u'e7453b95-a9bc-48dc-985f-a5b999697a83.gz', u'895e2ed9-3152-4c9b-893f-7ffd27710724.gz', u'cd15fd3e-fc36-4d48-b661-b74bc7d8ca72.gz', u'a5bb2f83-24a1-4433-8ed9-37203f64a30f.gz', u'2d558578-fa3f-4304-b3a6-e133a6964aeb.gz'], u'id': 446688, u'location': u's3://lotame-firehose/1234/na/mobile'}], u's3creds': {u'secretAccessKey': u'blah', u'sessionToken': u'blah', u'expiration': 9999999999999, u'accessKeyId': u'blah'}}
```

Wow, lots of stuff in here. Looks like there's a couple of `feeds`, each with a `id` and S3 bucket `location`. Also a list of `files`. Also looks like some `s3creds` specified for each `update`: an `accessKeyId`, a `secretAccessKey`, and a `sessionToken`.

So, I'll need to download some files from S3, and the Lotame API very kindly tells me where to find them and how to access them. 

No problemo, but it'd be better to just automate it.


---
If I want to automate this stuff, I'll need to iterate over each `update` and each `feed` and store off the values I need as I go. 

Also might as well iterate over all the `files` in each `feed`, since I know I need to process them one by one at some point. I'll print out everything as I go so I know it's working for now.
```python
>>> for update in updates:
...     s3creds = update['s3creds']
...     print(s3creds)
...     
...     feeds = update['feeds']
...     for feed in feeds:
...         feed_id = feed['id']
...         feed_location = feed['location']
...         print(feed_id)
...         print(feed_location)
...         
...         file_objects = feed['files']
...         for file_object in file_objects:
...             print(file_object)
```
```
{u'secretAccessKey': u'blah', u'sessionToken': u'blah', u'expiration': 9999999999999, u'accessKeyId': u'blah'}
112233
s3://lotame-firehose/1234/na/cookie
7d873ef1-8a03-4184-98e1-215095b28a89.gz
f7c09eaa-088a-48fc-9659-341df5de920d.gz
d95dff17-5932-4aa5-9ad5-584871e267a8.gz
009fda44-f681-4bed-8951-3bd0e08b5f6c.gz
9c5a66b5-a2a3-4841-8b75-bfd4f085553d.gz
0c1af5ce-1447-409c-a6b9-1a659a67b20c.gz
f260eede-967d-40ca-943e-b2268187d8a7.gz
{u'secretAccessKey': u'blah', u'sessionToken': u'blah', u'expiration': 9999999999999, u'accessKeyId': u'blah'}
446688
s3://lotame-firehose/1234/na/mobile
7fb1c995-d3ac-4c68-b089-ce1847df886c.gz
259874b1-3114-427f-bef7-41ed23f95299.gz
e7453b95-a9bc-48dc-985f-a5b999697a83.gz
895e2ed9-3152-4c9b-893f-7ffd27710724.gz
cd15fd3e-fc36-4d48-b661-b74bc7d8ca72.gz
a5bb2f83-24a1-4433-8ed9-37203f64a30f.gz
2d558578-fa3f-4304-b3a6-e133a6964aeb.gz
```

Awesome, that functioned swellingly. 

Now I need to make sense of all this and do Something Useful.

---


If I need to automate download files from S3, I'd like to use Python. Seems like Amazon folks like the idea of using Python too, because there's an AWS SDK for Python called `boto3`.

I'm going to import it and use it later for downloading the DataStream files.
```python
>>> import boto3, botocore
```

`boto3` uses this thing called a `Session` to manage credentials and state. Each `update` has a different set of AWS credentials, so I'll start by setting up a `boto3.Session` for each `update`. Then, I'll setup a `boto3.Resource` for S3, and use that to access the files. 

Looking at the documentation, I'll need to extract the bucket name and file prefixes from the feed `location` returned from the Lotame API. Regex is really good at pattern matching for strings so you can extract only the text you actually care about, so I'll try that on for size.

Also, I'm going to remove most of those `print` lines 'cause that's going to get annoying really fast, and I'm going to limit the number of `files` returned to only 2 in case the information gets overwhelming before I'm finished automating.

```python
>>> for update in updates:
...     s3creds = update['s3creds']
...     aws_session = boto3.Session(aws_access_key_id=s3creds['accessKeyId'],aws_secret_access_key=s3creds['secretAccessKey'],aws_session_token=s3creds['sessionToken'])
...     print(aws_session)
...     s3 = aws_session.resource('s3')
...     print(s3)
...     feeds = update['feeds']
...     for feed in feeds:
...         feed_id = feed['id']
...         feed_location = feed['location']
...         file_objects = feed['files']
...         bucket_name = str(re.search("(?<=s3:\/\/)([\w-]+)",feed_location).group(0))
...         prefix = str(re.search("(?<="+bucket_name+"\/)([\/\w-]+)",feed_location).group(0))
...         for i,file_object in enumerate(file_objects):
...             if i>=2:
...                 break
...             key = prefix+"/"+file_object
...             print(s3.Object(bucket_name,key).get())
```
```
Session(region_name='us-east-1')
s3.ServiceResource()
{u'Body': <botocore.response.StreamingBody object at 0x110a05fd0>, u'AcceptRanges': 'bytes', u'ContentType': 'binary/octet-stream', 'ResponseMetadata': {'HTTPStatusCode': 200.........
{u'Body': <botocore.response.StreamingBody object at 0x110165450>, u'AcceptRanges': 'bytes', u'ContentType': 'binary/octet-stream', 'ResponseMetadata': {'HTTPStatusCode': 200.........
Session(region_name='us-east-1')
s3.ServiceResource()
{u'Body': <botocore.response.StreamingBody object at 0x110a3c890>, u'AcceptRanges': 'bytes', u'ContentType': 'binary/octet-stream', 'ResponseMetadata': {'HTTPStatusCode': 200.........
{u'Body': <botocore.response.StreamingBody object at 0x10fce62d0>, u'AcceptRanges': 'bytes', u'ContentType': 'binary/octet-stream', 'ResponseMetadata': {'HTTPStatusCode': 200.........
```

Cool, so I've automated the creation of a `boto3.Session` for each `update`, created a `boto3.Resource` for S3 to access the files, and then used that to access the files and print out some details. So far, so good.

---
In reality, I'm kind of done... kind of. 

Really though, I just need to change that last line from
```python
print(s3.Object(bucket_name,key).get())
```
to
```python
s3.Object(bucket_name,key).download_file("/Desktop/")
```
...in order to take advantage of the built-in `boto3` method to copy the file to my local machine.

But, that's not my style. I want to run this straight from the command line and specify an output location each time I run it, so I can automate the whole thing via cron or something to run when I want and write to where I want.

Also, I'd like to print out the downloading status in case I need to check on the automated jobs doing the downloading. I found some code for a progress bar called, quite ingeniously I might add, `ProgressBay.py`, so as usual, I'll give it a shot and see if it behaves like I want.

```python
#!/usr/bin/python
#
# Filename: 
#
#     DataStreamDownloader.py
#
#
# Basic Usage:
#
#     python DataStreamDownloader.py /output/directory/for/datastream/gzip/files
#


import sys
sys.path.append('../')

# Lotame
from lib import Lotame

# AWS
import boto3, botocore

# Utilities
import time, re, json

# Fun
import ProgressBar

def main():

    print("")
    print("searching for firehose feed updates")

    output_dir = sys.argv[1]

    firehose = Lotame.FirehoseService()
    updates = firehose.getUpdates(hours=1)

    print("found "+str(len(updates))+"\n")

    if len(updates) == 0:
        sys.exit()

    for update in updates:

        s3creds = update['s3creds']
        feeds = update['feeds']

        aws_session = boto3.Session(
            aws_access_key_id=s3creds['accessKeyId'],
            aws_secret_access_key=s3creds['secretAccessKey'],
            aws_session_token=s3creds['sessionToken']
        )
        s3 = aws_session.resource('s3')

        for feed in feeds:
            feed_id = feed['id']
            feed_location = feed['location']
            file_objects = feed['files']
            total_objects = len(file_objects)
            bucket_name = str(re.search("(?<=s3:\/\/)([\w-]+)",feed_location).group(0))
            prefix = str(re.search("(?<="+bucket_name+"\/)([\/\w-]+)",feed_location).group(0))
            print ("processing feed "+str(feed_id))
            # print str(total_objects)+" new files"
            ProgressBar.print_progress(0, total_objects, prefix = '\tprogress:', suffix = 'complete', bar_length = 50)
            for i,file_object in enumerate(file_objects):
                key = prefix+"/"+file_object
                output = output_dir+file_object
                # print "\tdownloading "+output+"\n"
                s3.Object(bucket_name,key).download_file(output)
                ProgressBar.print_progress(i+1, total_objects, prefix = '\tprogress:', suffix = 'complete', bar_length = 50)
            print ("\t"+str(total_objects)+" files transferred from s3://"+bucket_name+"/"+prefix+" to "+output_dir+"\n")

if __name__ == '__main__':
    sys.exit(main())
```

So here goes nothin'. Or something. Hopefully Something, cause this all ain't Nothing.

```bash
python DataStreamDownloader.py ~/Desktop/
```

```bash

searching for firehose feed updates
found 2

processing feed 112233
    progress: |██████████████████████████████████████████████████| 100.0% complete
    5 files transferred from s3://lotame-firehose/1234/na/cookie to /Users/me/Desktop/

processing feed 446688
    progress: |██████████████████████████████████████████████████| 100.0% complete
    5 files transferred from s3://lotame-firehose/1234/na/mobile to /Users/me/Desktop/
```

Very slick, if I do say so myself. Which, well, I do.

"Put 'em together and what do ya got? Bibbidi-Bobbidi..." automated datastream file downloader.

I know, not as catchy. 

But, if I'm honest, way more pragmatic than a pumpkin carriage. 

And genuinely useful... now I can finally get to working on my waltz skillz for my dance with Prince(ss) Charming while Python works to automatically download all my sweet, sweet data.

