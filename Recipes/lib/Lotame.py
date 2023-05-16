#!/usr/bin/python
#
# Filename: 
#
#     Lotame.py
#
#
# Basic Usage:
#
#     1. import Lotame package:
#          import Lotame
#
#     2. input the appropriate profile (DEFAULT_PROFILE), token, and access
#          into the properties file (DEFAULT_PROPERTIES_FILENAME) 
#
#     3. instantiate a new instance of the Api class:
#          api = Lotame.Api()
#
#     4. use the Api class methods (get,postBody,post,put,delete) to perform operations with the Lotame API:
#          api.get("https://lotame.api","/service")  
#
#

# Utilities
import sys, json, requests, configparser
from datetime import datetime,timedelta
from os.path import expanduser


#
# Prints current LotameApi version
#
def version():
    print("2.0")


#
# Credentials Class
#   Loads credentials and metadata from properties file
#   Stores credentials and metadata for access by consumers
#
class Credentials:
    DEFAULT_PROPERTIES_FILENAME = expanduser("~") + "/" + "lotame.properties"
    DEFAULT_PROFILE = "default"

    def __init__(self, filename=DEFAULT_PROPERTIES_FILENAME, profile=DEFAULT_PROFILE, token=None, access=None,
                 base_url=None, client_id=None):
        if token and access and base_url and client_id:
            self.token = token
            self.access = access
            self.base_url = base_url
            self.client_id = client_id
        else:
            try:
                config = configparser.ConfigParser()
                config.read(filename)
                self.token = token or config.get(profile,"token").strip("\"")
                self.access = access or config.get(profile,"access").strip("\"")
                self.base_url = base_url or config.get(profile,"base_url").strip("\"")
                self.client_id = client_id or config.get(profile,"client_id").strip("\"")
            except configparser.Error as e:
                print("***\r\nYikes! Lotame.py couldn't load Credentials from the lotame.properties file.\r\n\r\nTry checking that the lotame.properties file is: \r\n\t1) located in your home directory or at the location specified by the `filename` parameter\r\n\t2) properly formatted according to DataStream_Cookbook/Recipes/lib/README.md\r\n\r\nGood Luck!\r\n\r\n\t...Just kidding. If issues persist just reach out to Lotame to get things working.\r\n\r\nPython Error below:\r\n***")
                print(e)


#
# Api Class
#   Imports credentials using Credentials Class
#   Utilizes stored credentials to authenticate requests to Lotame Api
#   Provides helper methods for service authentication and api actions
#
class Api:
    # static class variables
    REQUEST_GET = "REQUEST_GET"
    REQUEST_POSTBODY = "REQUEST_POSTBODY"
    REQUEST_POST = "REQUEST_POST"
    REQUEST_PUT = "REQUEST_PUT"
    REQUEST_DELETE = "REQUEST_DELETE"
    DEFAULT_PYTHON_HEADER = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
                             "User-Agent": "python"}
    DEFAULT_JSON_RECEIVE_HEADER = {'Accept': 'application/json'}
    DEFAULT_JSON_SEND_HEADER = {'Content-type': 'application/json', 'Accept': 'application/json'}

    # initialization method
    # allows specification of custom properties file and profile
    # allows passing authentication parameters directly in lieu of properties file 
    def __init__(self, credentials=None):
        if credentials is None:
            credentials = Credentials()
        self.credentials = credentials

    def populateUrlParams(self, url="", key="", val=""):
        if "?" not in url:
            url = url + "?" + str(key) + "=" + str(val)
        else:
            url = url + "&" + str(key) + "=" + str(val)
        return url

    def buildUrl(self, service="", params={}, auto_assign_client_id=True):
        if service == "":
            return ""
        url = self.credentials.base_url + service
        if auto_assign_client_id is True:
            url = url + "?client_id=" + str(self.credentials.client_id)
        for key, val in params.items():
            if isinstance(val, list):
                for v in val:
                    url = self.populateUrlParams(url, key, v)
            else:
                url = self.populateUrlParams(url, key, val)
        return url

    def mergeHeaders(self, base_headers):
        headers = {}
        headers.update(base_headers)
        auth_headers = {
            'x-lotame-token': self.credentials.token,
            'x-lotame-access': self.credentials.access
        }
        headers.update(auth_headers)
        return(headers)

    def performRequest(self, service="", user=None, access=None, type=None, headers=None, body=None):
        response = ""
        full_headers=self.mergeHeaders(headers)
        if type == self.REQUEST_GET:
            response = requests.get(service, headers=full_headers, allow_redirects=False)
        elif type == self.REQUEST_POSTBODY:
            response = requests.post(service, data=json.dumps(body), headers=full_headers, allow_redirects=False)
        elif type == self.REQUEST_POST:
            response = requests.post(service, headers=full_headers, allow_redirects=False)
        elif type == self.REQUEST_PUT:
            response = requests.put(service, data=json.dumps(body), headers=full_headers, allow_redirects=False)
        elif type == self.REQUEST_DELETE:
            response = requests.delete(service, headers=full_headers, allow_redirects=False)
        else:
            response = "Invalid request type"
        return response

    def get(self, service, user=None, access=None):
        # print("GET request " + service)
        return self.performRequest(
            service=service,
            user=user,
            access=access,
            type=self.REQUEST_GET,
            headers=self.DEFAULT_JSON_RECEIVE_HEADER
        ).json()

    def postBody(self, service="", body="", user=None, access=None):
        # print("POST request: " + service)
        # print("body: " + str(body))
        return self.performRequest(
            service=service,
            user=user,
            access=access,
            type=self.REQUEST_POSTBODY,
            headers=self.DEFAULT_JSON_SEND_HEADER,
            body=body
        ).json()

    def post(self, service="", user=None, access=None):
        # print("POST request: " + service)
        return self.performRequest(
            service=service,
            user=user,
            access=access,
            type=self.REQUEST_POST,
            headers=self.DEFAULT_JSON_SEND_HEADER
        ).json()

    def put(self, service="", body="", user=None, access=None):
        # print("POST request: " + service)
        # print("body: " + str(body))
        return self.performRequest(
            service=service,
            user=user,
            access=access,
            type=self.REQUEST_PUT,
            headers=self.DEFAULT_JSON_SEND_HEADER,
            body=body
        ).json()

    def delete(self, service="", user=None, access=None):
        # print("DELETE request: " + service)
        return self.performRequest(
            service=service,
            user=user,
            access=access,
            type=self.REQUEST_DELETE,
            headers=self.DEFAULT_JSON_RECEIVE_HEADER
        ).json()


#
# FirehoseService Class
#   Provides helper methods for the Lotame API firehose service
#
class FirehoseService:
    # statics
    FIREHOSE_FEEDS = "/firehose/feeds"
    FIREHOSE_UPDATES = "/firehose/updates"
    DEFAULT_HOURS = 24
    DEFAULT_MINUTES = 0
    DEFAULT_UTC = 0
    FEED_ID = "feed_id"

    def __init__(self, api=None):
        if api is None:
            api = Api()
        self.api = api

    def getFeeds(self, params={}):
        url = self.api.buildUrl(self.FIREHOSE_FEEDS, params)
        feeds_response = self.api.get(url)
        feeds = []
        for feed_json in feeds_response['feeds']:
            feeds.append(feed_json)
        return feeds

    def getUpdatesForFeed(self, feed_id=0, params={}):
        if params == {}:
            params = {self.FEED_ID: feed_id}
        else:
            params[self.FEED_ID] = feed_id
        url = self.api.buildUrl(self.FIREHOSE_UPDATES, params)
        feed_updates_response = self.api.get(url)
        return feed_updates_response

    def getUpdatesForFeeds(self, feeds=[], params={}):
        feeds_updates_responses = []
        for feed in feeds:
            feeds_updates_responses.append(self.getUpdatesForFeed(feed['id'], params))
        return feeds_updates_responses

    def getUpdates(self, hours=DEFAULT_HOURS, minutes=DEFAULT_MINUTES, since=DEFAULT_UTC):
        params = {}
        if since:
            since_utc = str(int(round(since)))
        elif hours or minutes:
            since_utc = str(int(round(
                ((datetime.utcnow() - timedelta(hours=hours, minutes=minutes)) - datetime(1970, 1, 1)).total_seconds())))
            params = {"since": since_utc}
        feeds = self.getFeeds()
        updates = self.getUpdatesForFeeds(feeds, params)
        return updates

#
# BehaviorService Class
#   Provides helper methods for the Lotame API behavior service
#
class BehaviorService:
    # statics
    BEHAVIOR_SERVICE = "/behaviors"

    def __init__(self, api=None):
        if api is None:
            api = Api()
        self.api = api

    def get(self, behavior=""):
        url = self.api.buildUrl(self.BEHAVIOR_SERVICE + "/" + str(behavior), {}, False)
        behavior = self.api.get(url)
        return behavior

    def getList(self, params={}):
        url = self.api.buildUrl(self.BEHAVIOR_SERVICE, params)
        behavior_list = self.api.get(url)
        return behavior_list


#
# AudienceService Class
#   Provides helper methods for the Lotame API audience service
#
class AudienceService:
    # statics
    AUDIENCE_SERVICE = "/audiences"

    def __init__(self, api=None):
        if api is None:
            api = Api()
        self.api = api

    def get(self, audience=""):
        url = self.api.buildUrl(self.AUDIENCE_SERVICE + "/" + str(audience), {}, False)
        audience = self.api.get(url)
        return audience

    def getList(self, params={}):
        url = self.api.buildUrl(self.AUDIENCE_SERVICE, params)
        audience_list = self.api.get(url)
        return audience_list
