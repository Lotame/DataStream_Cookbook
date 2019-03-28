# Recipe 0
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
>>> import Lotame
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

Wow, lots of stuff in here. Looks like there's a couple of `feeds`, each with an s3 bucket location and a list of files. Also looks like some s3 credentials specified for each `update`. 

So, I'll need to download some files from s3. No problem, but it'd be nice to just automate it.


---
If I want to make this useful, I'll need to iterate over each `update` and each `feed` and store off the values I need as I go. 

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


If I need to automate download files from s3, I'd like to use Python. Seems like Amazon like to use Python too, becuase there's an AWS SDK for Python called `boto3`.

I'm going to import it and use it later for downloading the DataStream files.
```python
>>> import boto3
```

`boto3` uses this thing called a `Session` to manage credentials and state. Each `update` has a different set of AWS credentials, so I'll start by setting up a `boto3.Session` for each `update`.

Also, I'm going to remove all those `print` lines cause that's going to get annoying really fast.
```python
>>> for update in updates:
...     s3creds = update['s3creds']
...     aws_session = boto3.Session(aws_access_key_id=s3creds['accessKeyId'],aws_secret_access_key=s3creds['secretAccessKey'],aws_session_token=s3creds['sessionToken'])
...     print(aws_session)
...     feeds = update['feeds']
...     for feed in feeds:
...         feed_id = feed['id']
...         feed_location = feed['location']
...         file_objects = feed['files']
...         for file_object in file_objects:
...             print(file_object)
```
```
Session(region_name='us-east-1')
007d5141-e61e-4a38-9b78-5b146936a98c.gz
36ede3dd-5bf6-43ff-b7be-30fbac371e92.gz
3a263be0-421c-4401-a8fe-b8e3dcb62cf6.gz
662d52e7-e4d4-4593-87cd-368f66cfeed5.gz
6bae4aa3-8e76-4168-81cf-d60542754f46.gz
787b2776-feb0-49a2-8d41-798adbd6e33f.gz
bb142eec-8381-4d48-9230-9b1fdbfb61b9.gz
Session(region_name='us-east-1')
25515ece-d44b-42ab-90cd-6eaa330fe8bc.gz
564bf16e-fe3f-4a19-b5ca-5f8790c29685.gz
bc777e62-29e2-4986-9895-7501dd5e1f45.gz
c151c864-08d0-4064-ad6d-7066aab9280a.gz
e6c86d66-329d-461d-a1f7-4c5c1fde574b.gz
f03e75cd-2d77-4e0c-a33f-51494847c3e2.gz
f4527519-3ba3-4b14-b8cc-96956e4b1e7a.gz
```
