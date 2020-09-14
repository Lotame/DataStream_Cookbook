# Lotame Utilities
## Overview

### lotame.properties
This is a properties file that stores API authentication specific parameters: 'token' and 'access' parameters specifying a token and access key for API authentication, and the client id to be used when connecting to the Lotame API. Instructions for obtaining an API token and access key can be found [here](https://my.lotame.com/t/35h37my/admin-api#authorized-access).

While the properties file location is configurable, by default, the `Credentials` class (see below) expects this file to be located in the user's home directory, e.g. `~/lotame.properties`

See [here](https://docs.python.org/2.7/library/configparser.html) for more details on the properties file spec.

##### Note that "auth_url" and "base_url" are not intended to be changed by the user.




### Lotame.py
This is a python module which contains 5 classes: 

`Credentials` 
manages loading authentication parameters from a properties file (see above), or by directly specifying the necessary values during instantiation.


`Api`
provides a variety of helper methods for authenticating and querying the Lotame API.


`FirehoseService`
contains helper methods for accessing data provided by the Lotame API Firehose service.


`BehaviorService`
contains helper methods for accessing data provided by the Lotame API Behavior service.


`AudienceService`
contains helper methods for accessing data provided by the Lotame API Audience service.


## Usage


##### Note: LotameApi and LotameFirehose were designed for Python 2.7

### git

#### clone the repo
```
git clone git@github.com:Lotame/DataStream_Cookbook.git
cd DataStream_Cookbook
```

### lotame.properties

#### configure the lotameapi.properties file
```
cd lib
vi lotame.properties
```


### Lotame.py

#### instantiate a new `Credentials` instance
```python
# launch python
cd recipes/lib
python
```
```python
# import the Lotame module
import Lotame

# instantiate a new Credentials class using the default ~/lotame.properties
creds = Lotame.Credentials()

# or, instantiate a new Credentials class using a custom file
creds = Lotame.Credentials(filename="/your/custom/file")

# or, instantiate a new Credentials class using manual configuration
creds = Lotame.Credentials(username="youruser",password="yourpassword",client_id=999999,base_url="https://lotame.api/base/url/",auth_url="https://lotame.api/auth/url/")

# show creds
print(creds.username)
print(creds.password)
print(creds.client_id)
print(creds.base_url)
print(creds.auth_url)

```
#### use the `Api` helper methods

```python
# launch python
cd recipes/lib
python
```
```python
# import the Lotame module
import Lotame

# instantiate a new Api class using the default configuration
api = Lotame.Api()

# or, instantiate a new Api class using a custom Credentials class
creds = Lotame.Credentials()
api = Lotame.Api(creds)

# use the Api class helper method to build a valid Lotame API url 
url = api.buildUrl("/your/service/here/")

# use the Api class helper method to perform a GET request against the Lotame API
response = api.get(url)

# show the json response from the GET request
print(response)
```


#### use the `FirehoseService` helper methods
```python
# launch python
cd recipes/lib
python
```
```python
# import the LotameFirehose module
import Lotame

# instantiate a new FirehoseService class using the default configuration
firehose = Lotame.FirehoseService()

# or, instantiate a new FirehoseService class using a custom Credentials and a custom Api class
creds = Lotame.Credentials(filename="/your/custom/file")
api = Lotame.Api(creds)
firehose = Lotame.FirehoseService(api)

# get firehose updates from the Lotame API for the last hour
updates = firehose.getUpdates(hours=1)

# prettyprint the reponses from the Lotame API Firehose service
print(json.dumps(updates, indent=4, sort_keys=True))
```