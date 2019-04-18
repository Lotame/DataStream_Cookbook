# Opening the pantry
#### ...or how I learned to stop worrying and love the Lotame API.........

I have access to this thing all the cool kids are talking about. 

It's called the Lotame API.

But I'm a programmer. And a pragmatist. So, to me, it's only cool if I can do cool things with it.

I also like Data. Like, like Data. Like, Big Data. 

This DataStream thing seems like a good place to start. 

Like all my Big Data projects, I'm going to finish Big by starting Small.

I think I'll start by trying to download some of these DataStream files, see what's what, and go from there.

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
[{u'feeds': [{u'files': [u'007d5141-e61e-4a38-9b78-5b146936a98c.gz', u'36ede3dd-5bf6-43ff-b7be-30fbac371e92.gz', u'3a263be0-421c-4401-a8fe-b8e3dcb62cf6.gz', u'662d52e7-e4d4-4593-87cd-368f66cfeed5.gz', u'6bae4aa3-8e76-4168-81cf-d60542754f46.gz', u'787b2776-feb0-49a2-8d41-798adbd6e33f.gz', u'bb142eec-8381-4d48-9230-9b1fdbfb61b9.gz'], u'id': 240, u'location': u's3://lotame-firehose/2215/na/cookie'}], u's3creds': {u'secretAccessKey': u'tGlSclMEw8Oah4I679qalwQ3AhuplN4vham2b3CY', u'sessionToken': u'FQoGZXIvYXdzEFcaDC41gUVs7b5tQQlDDyKTArnEJQPxDy4ZOce4bOebQ/3+C7DtjOkCxP1uUJlBImpaurGkmLUHjuYE1Tz2IbbYEIZcvUcrRGX+6txJ7ptZX2UuWBe4fJbPRE7JwwmWWftViqT2bq5KLGHRjklZGq2pgE6vUSk91J4doUpMOv6NBwvtEoyha5CDFDES3FNzAVD/nDRNXjW6Aqh0BuwzB79pX8mQSbIkNJ+NaVRT8cMoYB4WwKyNQuFUO8FBZ83SHjVHwavXQf7xAT07Kmb3kqzfNDYkpJeW0cBAlpF8ATrcvZLPrg58BojXRxphr5RUFlFP+NHmXg5wPC19O42753hLty3tD910/XOxQpGNIgPU0e3AdF2I9+katAxqBUttVC8FEwxjKLS6sOQF', u'expiration': 1552700788000, u'accessKeyId': u'ASIAUQ6Z75CF2KID75GG'}}, {u'feeds': [{u'files': [u'25515ece-d44b-42ab-90cd-6eaa330fe8bc.gz', u'564bf16e-fe3f-4a19-b5ca-5f8790c29685.gz', u'bc777e62-29e2-4986-9895-7501dd5e1f45.gz', u'c151c864-08d0-4064-ad6d-7066aab9280a.gz', u'e6c86d66-329d-461d-a1f7-4c5c1fde574b.gz', u'f03e75cd-2d77-4e0c-a33f-51494847c3e2.gz', u'f4527519-3ba3-4b14-b8cc-96956e4b1e7a.gz'], u'id': 241, u'location': u's3://lotame-firehose/2215/na/mobile'}], u's3creds': {u'secretAccessKey': u't36fMtSAgr42Vw4NJZp+6Fox/vuL6YBHa+O11Sdu', u'sessionToken': u'FQoGZXIvYXdzEFcaDHBpNqJPoRtBHg69OCKTAqN1j68Nq57ezxvx+kN5MjpQJKwBQHRgMfENnhgdoYaZEy15ezY735KByVvzo2J66luOPYHNUi/Rn4dh0VZO14HsDIo9HfcIvFWNFVrG/JknM4hn8hIlzPGaIlOU7mimY/07fT9kNPwYeGPV0mm03+V5TQ/LBKoNnl0ihMHqBtAcFhq9VA0FIzOev1qz3sgOoiIxJWtEJz7f6jFts0ZmbqGoBYGZk/9s6mMKDHXQvH1wWSYnwtarNa7R+mBJMR7rShCrZMJ1OuXrDel2teoULG4cpbDCioo1dNeV4uz83wanwPuFScgF+RYkJDHSzmMJUgbob10eeodCJc4VcGkSgJLPg+IRPdLxTQtd5AAfO+MkISthKL+6sOQF', u'expiration': 1552700799000, u'accessKeyId': u'ASIAUQ6Z75CF4IAUVTUE'}}]
```

Looks like a list, so I'll iterate over it and print out each update individually.

```python
>>> for update in updates:
...     print(update)
```
```
{u'feeds': [{u'files': [u'007d5141-e61e-4a38-9b78-5b146936a98c.gz', u'36ede3dd-5bf6-43ff-b7be-30fbac371e92.gz', u'3a263be0-421c-4401-a8fe-b8e3dcb62cf6.gz', u'662d52e7-e4d4-4593-87cd-368f66cfeed5.gz', u'6bae4aa3-8e76-4168-81cf-d60542754f46.gz', u'787b2776-feb0-49a2-8d41-798adbd6e33f.gz', u'bb142eec-8381-4d48-9230-9b1fdbfb61b9.gz'], u'id': 240, u'location': u's3://lotame-firehose/2215/na/cookie'}], u's3creds': {u'secretAccessKey': u'tGlSclMEw8Oah4I679qalwQ3AhuplN4vham2b3CY', u'sessionToken': u'FQoGZXIvYXdzEFcaDC41gUVs7b5tQQlDDyKTArnEJQPxDy4ZOce4bOebQ/3+C7DtjOkCxP1uUJlBImpaurGkmLUHjuYE1Tz2IbbYEIZcvUcrRGX+6txJ7ptZX2UuWBe4fJbPRE7JwwmWWftViqT2bq5KLGHRjklZGq2pgE6vUSk91J4doUpMOv6NBwvtEoyha5CDFDES3FNzAVD/nDRNXjW6Aqh0BuwzB79pX8mQSbIkNJ+NaVRT8cMoYB4WwKyNQuFUO8FBZ83SHjVHwavXQf7xAT07Kmb3kqzfNDYkpJeW0cBAlpF8ATrcvZLPrg58BojXRxphr5RUFlFP+NHmXg5wPC19O42753hLty3tD910/XOxQpGNIgPU0e3AdF2I9+katAxqBUttVC8FEwxjKLS6sOQF', u'expiration': 1552700788000, u'accessKeyId': u'ASIAUQ6Z75CF2KID75GG'}}
{u'feeds': [{u'files': [u'25515ece-d44b-42ab-90cd-6eaa330fe8bc.gz', u'564bf16e-fe3f-4a19-b5ca-5f8790c29685.gz', u'bc777e62-29e2-4986-9895-7501dd5e1f45.gz', u'c151c864-08d0-4064-ad6d-7066aab9280a.gz', u'e6c86d66-329d-461d-a1f7-4c5c1fde574b.gz', u'f03e75cd-2d77-4e0c-a33f-51494847c3e2.gz', u'f4527519-3ba3-4b14-b8cc-96956e4b1e7a.gz'], u'id': 241, u'location': u's3://lotame-firehose/2215/na/mobile'}], u's3creds': {u'secretAccessKey': u't36fMtSAgr42Vw4NJZp+6Fox/vuL6YBHa+O11Sdu', u'sessionToken': u'FQoGZXIvYXdzEFcaDHBpNqJPoRtBHg69OCKTAqN1j68Nq57ezxvx+kN5MjpQJKwBQHRgMfENnhgdoYaZEy15ezY735KByVvzo2J66luOPYHNUi/Rn4dh0VZO14HsDIo9HfcIvFWNFVrG/JknM4hn8hIlzPGaIlOU7mimY/07fT9kNPwYeGPV0mm03+V5TQ/LBKoNnl0ihMHqBtAcFhq9VA0FIzOev1qz3sgOoiIxJWtEJz7f6jFts0ZmbqGoBYGZk/9s6mMKDHXQvH1wWSYnwtarNa7R+mBJMR7rShCrZMJ1OuXrDel2teoULG4cpbDCioo1dNeV4uz83wanwPuFScgF+RYkJDHSzmMJUgbob10eeodCJc4VcGkSgJLPg+IRPdLxTQtd5AAfO+MkISthKL+6sOQF', u'expiration': 1552700799000, u'accessKeyId': u'ASIAUQ6Z75CF4IAUVTUE'}}
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
{u'secretAccessKey': u'tGlSclMEw8Oah4I679qalwQ3AhuplN4vham2b3CY', u'sessionToken': u'FQoGZXIvYXdzEFcaDC41gUVs7b5tQQlDDyKTArnEJQPxDy4ZOce4bOebQ/3+C7DtjOkCxP1uUJlBImpaurGkmLUHjuYE1Tz2IbbYEIZcvUcrRGX+6txJ7ptZX2UuWBe4fJbPRE7JwwmWWftViqT2bq5KLGHRjklZGq2pgE6vUSk91J4doUpMOv6NBwvtEoyha5CDFDES3FNzAVD/nDRNXjW6Aqh0BuwzB79pX8mQSbIkNJ+NaVRT8cMoYB4WwKyNQuFUO8FBZ83SHjVHwavXQf7xAT07Kmb3kqzfNDYkpJeW0cBAlpF8ATrcvZLPrg58BojXRxphr5RUFlFP+NHmXg5wPC19O42753hLty3tD910/XOxQpGNIgPU0e3AdF2I9+katAxqBUttVC8FEwxjKLS6sOQF', u'expiration': 1552700788000, u'accessKeyId': u'ASIAUQ6Z75CF2KID75GG'}
240
s3://lotame-firehose/2215/na/cookie
007d5141-e61e-4a38-9b78-5b146936a98c.gz
36ede3dd-5bf6-43ff-b7be-30fbac371e92.gz
3a263be0-421c-4401-a8fe-b8e3dcb62cf6.gz
662d52e7-e4d4-4593-87cd-368f66cfeed5.gz
6bae4aa3-8e76-4168-81cf-d60542754f46.gz
787b2776-feb0-49a2-8d41-798adbd6e33f.gz
bb142eec-8381-4d48-9230-9b1fdbfb61b9.gz
{u'secretAccessKey': u't36fMtSAgr42Vw4NJZp+6Fox/vuL6YBHa+O11Sdu', u'sessionToken': u'FQoGZXIvYXdzEFcaDHBpNqJPoRtBHg69OCKTAqN1j68Nq57ezxvx+kN5MjpQJKwBQHRgMfENnhgdoYaZEy15ezY735KByVvzo2J66luOPYHNUi/Rn4dh0VZO14HsDIo9HfcIvFWNFVrG/JknM4hn8hIlzPGaIlOU7mimY/07fT9kNPwYeGPV0mm03+V5TQ/LBKoNnl0ihMHqBtAcFhq9VA0FIzOev1qz3sgOoiIxJWtEJz7f6jFts0ZmbqGoBYGZk/9s6mMKDHXQvH1wWSYnwtarNa7R+mBJMR7rShCrZMJ1OuXrDel2teoULG4cpbDCioo1dNeV4uz83wanwPuFScgF+RYkJDHSzmMJUgbob10eeodCJc4VcGkSgJLPg+IRPdLxTQtd5AAfO+MkISthKL+6sOQF', u'expiration': 1552700799000, u'accessKeyId': u'ASIAUQ6Z75CF4IAUVTUE'}
241
s3://lotame-firehose/2215/na/mobile
25515ece-d44b-42ab-90cd-6eaa330fe8bc.gz
564bf16e-fe3f-4a19-b5ca-5f8790c29685.gz
bc777e62-29e2-4986-9895-7501dd5e1f45.gz
c151c864-08d0-4064-ad6d-7066aab9280a.gz
e6c86d66-329d-461d-a1f7-4c5c1fde574b.gz
f03e75cd-2d77-4e0c-a33f-51494847c3e2.gz
f4527519-3ba3-4b14-b8cc-96956e4b1e7a.gz
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
{u'Body': <botocore.response.StreamingBody object at 0x110a05fd0>, u'AcceptRanges': 'bytes', u'ContentType': 'binary/octet-stream', 'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0, 'HostId': 'kzt9oD6kkuQo3xJ+kLGpFIzZV+02jzJz11UoxH31Usx4qx21Keet8eIFFoB9XxqeiCDSUYScX9U=', 'RequestId': '17D2DAC0F051C891', 'HTTPHeaders': {'content-length': '4073', 'x-amz-id-2': 'kzt9oD6kkuQo3xJ+kLGpFIzZV+02jzJz11UoxH31Usx4qx21Keet8eIFFoB9XxqeiCDSUYScX9U=', 'accept-ranges': 'bytes', 'x-amz-expiration': 'expiry-date="Sun, 19 May 2019 00:00:00 GMT", rule-id="45dayTTL"', 'last-modified': 'Wed, 03 Apr 2019 20:13:22 GMT', 'x-amz-request-id': '17D2DAC0F051C891', 'etag': '"e4f16e22c9295ed83f37752518fc275d"', 'date': 'Thu, 04 Apr 2019 01:14:41 GMT', 'server': 'AmazonS3', 'content-type': 'binary/octet-stream'}}, u'LastModified': datetime.datetime(2019, 4, 3, 20, 13, 22, tzinfo=tzutc()), u'ContentLength': 4073, u'ETag': '"e4f16e22c9295ed83f37752518fc275d"', u'Expiration': 'expiry-date="Sun, 19 May 2019 00:00:00 GMT", rule-id="45dayTTL"', u'Metadata': {}}
{u'Body': <botocore.response.StreamingBody object at 0x110165450>, u'AcceptRanges': 'bytes', u'ContentType': 'binary/octet-stream', 'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0, 'HostId': 'HrziqiTR4mY9CYavNkm4VkBkL0Owum42NQkIHbYFTDr52NgfOI8vnEFX0g4gMmiKd5eBLwIrTwY=', 'RequestId': 'A5D599B2A0EA6B88', 'HTTPHeaders': {'content-length': '3794', 'x-amz-id-2': 'HrziqiTR4mY9CYavNkm4VkBkL0Owum42NQkIHbYFTDr52NgfOI8vnEFX0g4gMmiKd5eBLwIrTwY=', 'accept-ranges': 'bytes', 'x-amz-expiration': 'expiry-date="Sun, 19 May 2019 00:00:00 GMT", rule-id="45dayTTL"', 'last-modified': 'Wed, 03 Apr 2019 21:09:29 GMT', 'x-amz-request-id': 'A5D599B2A0EA6B88', 'etag': '"b3fea5e3abf9d2b7e113f0f849dfc12e"', 'date': 'Thu, 04 Apr 2019 01:14:42 GMT', 'server': 'AmazonS3', 'content-type': 'binary/octet-stream'}}, u'LastModified': datetime.datetime(2019, 4, 3, 21, 9, 29, tzinfo=tzutc()), u'ContentLength': 3794, u'ETag': '"b3fea5e3abf9d2b7e113f0f849dfc12e"', u'Expiration': 'expiry-date="Sun, 19 May 2019 00:00:00 GMT", rule-id="45dayTTL"', u'Metadata': {}}
Session(region_name='us-east-1')
s3.ServiceResource()
{u'Body': <botocore.response.StreamingBody object at 0x110a3c890>, u'AcceptRanges': 'bytes', u'ContentType': 'binary/octet-stream', 'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0, 'HostId': 'm4bAwb+52tNJEHSa1QMdmsyHJxXJ2bXRa8dBc88Ns4/bkDyouQDAZCzU7CpnbpCH+94VQS7gqMo=', 'RequestId': 'F60B0CE4FB1B11CA', 'HTTPHeaders': {'content-length': '120846', 'x-amz-id-2': 'm4bAwb+52tNJEHSa1QMdmsyHJxXJ2bXRa8dBc88Ns4/bkDyouQDAZCzU7CpnbpCH+94VQS7gqMo=', 'accept-ranges': 'bytes', 'x-amz-expiration': 'expiry-date="Sun, 19 May 2019 00:00:00 GMT", rule-id="45dayTTL"', 'last-modified': 'Wed, 03 Apr 2019 23:08:01 GMT', 'x-amz-request-id': 'F60B0CE4FB1B11CA', 'etag': '"7267e34647acb92d618d0573960f7ecc"', 'date': 'Thu, 04 Apr 2019 01:14:42 GMT', 'server': 'AmazonS3', 'content-type': 'binary/octet-stream'}}, u'LastModified': datetime.datetime(2019, 4, 3, 23, 8, 1, tzinfo=tzutc()), u'ContentLength': 120846, u'ETag': '"7267e34647acb92d618d0573960f7ecc"', u'Expiration': 'expiry-date="Sun, 19 May 2019 00:00:00 GMT", rule-id="45dayTTL"', u'Metadata': {}}
{u'Body': <botocore.response.StreamingBody object at 0x10fce62d0>, u'AcceptRanges': 'bytes', u'ContentType': 'binary/octet-stream', 'ResponseMetadata': {'HTTPStatusCode': 200, 'RetryAttempts': 0, 'HostId': 'Tk7oNzAfXDa+9BaCf7FqGvfAfIhkGlRY0R3aEnUivNGUywEgWWo1pVEUoFHHeu4apHu6hPr7F9U=', 'RequestId': 'CA4E5B975D536421', 'HTTPHeaders': {'content-length': '132942', 'x-amz-id-2': 'Tk7oNzAfXDa+9BaCf7FqGvfAfIhkGlRY0R3aEnUivNGUywEgWWo1pVEUoFHHeu4apHu6hPr7F9U=', 'accept-ranges': 'bytes', 'x-amz-expiration': 'expiry-date="Mon, 20 May 2019 00:00:00 GMT", rule-id="45dayTTL"', 'last-modified': 'Thu, 04 Apr 2019 00:15:50 GMT', 'x-amz-request-id': 'CA4E5B975D536421', 'etag': '"53f433541b0fd4abb23be76b1b3e454e"', 'date': 'Thu, 04 Apr 2019 01:14:42 GMT', 'server': 'AmazonS3', 'content-type': 'binary/octet-stream'}}, u'LastModified': datetime.datetime(2019, 4, 4, 0, 15, 50, tzinfo=tzutc()), u'ContentLength': 132942, u'ETag': '"53f433541b0fd4abb23be76b1b3e454e"', u'Expiration': 'expiry-date="Mon, 20 May 2019 00:00:00 GMT", rule-id="45dayTTL"', u'Metadata': {}}
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

processing feed 240
    progress: |██████████████████████████████████████████████████| 100.0% complete
    5 files transferred from s3://lotame-firehose/2215/na/cookie to /Users/aconant/Desktop/

processing feed 241
    progress: |██████████████████████████████████████████████████| 100.0% complete
    5 files transferred from s3://lotame-firehose/2215/na/mobile to /Users/aconant/Desktop/
```

Very slick, if I do say so myself. Which, well, I do.

"Put 'em together and what do ya got? Bibbidi-Bobbidi..." automated datastream file downloader.

I know, not as catchy. 

But, if I'm honest, way more pragmatic than a pumpkin carriage. 

And genuinely useful... now I can finally get to working on my waltz skillz for my dance with Prince(ss) Charming while Python works to automatically download all my sweet, sweet data.

