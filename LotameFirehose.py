#!/usr/bin/python
#
# Filename: 
#
#     LotameFirehose.py
#
#
# Basic Usage:
#
#     1. import LotameFirehose package:
#          import LotameFirehose
#
#     2. input the appropriate profile (DEFAULT_PROFILE), username, and password
#          into the properties file (DEFAULT_PROPERTIES_FILE) 
#
#     3. instantiate a new instance of the Lotame Firehose Api class:
#          firehose = LotameFirehose.Firehose()
#
#     4. use the class methods to perform operations with the Lotame Firehose Api:
#          updates = firehose.getUpdates()  
#
#

# Lotame
import LotameApi

# Utilities
from datetime import datetime,timedelta

class Firehose:

  # statics
  FIREHOSE_FEEDS="/firehose/feeds"
  FIREHOSE_UPDATES="/firehose/updates"
  DEFAULT_HOURS=24
  DEFAULT_MINUTES=0
  DEFAULT_UTC=0
  FEED_ID="feed_id"

  def __init__(self, api=None):
    if api is None:
      self.api = LotameApi.Api()
    else:
      self.api = api

  def getFeeds(self, params={}):
    url = self.api.buildServiceUrl(self.FIREHOSE_FEEDS,params)
    res = self.api.get(url)
    feeds = []
    for feedJson in res['feeds']:
      feeds.append(feedJson)
    return feeds

  def getUpdatesForFeed(self, feed_id=0, params={}):
    if params == {}:
      params = {self.FEED_ID:feed_id}
    else:
      params[self.FEED_ID] = feed_id
    url = self.api.buildServiceUrl(self.FIREHOSE_UPDATES,params)
    feedUpdatesResponse = self.api.get(url)
    return feedUpdatesResponse

  def getUpdatesForFeeds(self, feeds=[], params={}):
    feedUpdatesResponses = []
    for feed in feeds:
      feedUpdatesResponses.append(self.getUpdatesForFeed(feed['id'],params))
    return feedUpdatesResponses

  def getUpdates(self, hours=DEFAULT_HOURS, minutes=DEFAULT_MINUTES, since=DEFAULT_UTC):
    params={}
    if since:
      since_utc = str(int(round(since)))
    elif hours or minutes:
      since_utc = str(int(round(((datetime.now() - timedelta(hours=hours,minutes=minutes)) - datetime(1970,1,1)).total_seconds())))
      params = {"since":since_utc}
    feeds = self.getFeeds()
    updates = self.getUpdatesForFeeds(feeds,params)
    return updates