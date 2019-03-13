# DataStream_Cookbook


# Lotame API Utilities
## Overview

### lotameapi.properties
This is a properties file that stores API authentication specific parameters such as username, password, and client id.

See [here](https://docs.python.org/2.7/library/configparser.html) for more details on the properties file spec.

Note that "auth_url" and "base_url" are not intended to be changed by the user. 


### LotameApi.py
This is a python module which contains 2 classes:
>`Credentials`
>
>`Api`

The `Credentials` class manages loading authentication parameters from a properties file (see above), or by directly specifying the necessary values during instantiation.

The `Api` class provides a variety of helper methods for authenticating and querying the Lotame API.


### LotameFirehose.py
This is a python module which contains 1 class:
>`Firehose`

The `Firehose` class includes a variety of helper methods for accessing data provided by the Lotame API Firehose service.





## Usage


##### Note: LotameApi and LotameFirehose were designed for Python 2.7


### clone the repo
```
git clone git@github.com:Lotame/DataStream_Cookbook.git
cd DataStream_Cookbook
```


### configure the lotameapi.properties file
```
vi lotame
```


### LotameApi.py
```python
# launch python
python
```
```python
# import the LotameApi module
import LotameApi

# instantiate a new Api class
api = LotameApi.Api()

# use the Api class helper method to build a valid Lotame API url 
url = api.buildServiceUrl("/your/service/here/")

# use the Api class helper method to perform a GET request against the Lotame API
response = api.get(url)

# print the response from the GET request
print(response)
```


### LotameFirehose.py
```python
# launch python
python
```
```python
# import the LotameFirehose module
import LotameFirehose

# instantiate a new Firehose class
firehose = LotameFirehose.Firehose()

# get firehose updates from the Lotame API for the last hour
updates = firehose.getUpdates(hours=1)

# print the reponse from the Lotame API Firehose service
print(updates)
```