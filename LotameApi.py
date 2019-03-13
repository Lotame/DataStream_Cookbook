#!/usr/bin/python
#
# Filename: 
#
#     LotameApi.py
#
#
# Basic Usage:
#
#     1. import LotameApi package:
#          import LotameApi
#
#     2. input the appropriate profile (DEFAULT_PROFILE), username, and password
#          into the properties file (DEFAULT_PROPERTIES_FILE) 
#
#     3. instantiate a new instance of the Api class:
#          api = LotameApi.Api()
#
#     4. use the Api class methods (get,postBody,post,put,delete) to perform operations with the Lotame Api:
#          api.get("https://lotame.api","/service")  
#
#

# Utilities
import sys, json, requests, ConfigParser

#
# Prints current LotameApi version
#
def version():
    print "2.0"

#
# Credentials Class
#   Loads credentials and metadata from properties file
#   Stores credentials and metadata for access by consumers
#
class Credentials:
    
    DEFAULT_PROPERTIES_FILE="lotameapi.properties"
    DEFAULT_PROFILE="default"

    def __init__(self, filename = None, profile = None):
        try:
            if filename is None:
                filename = self.DEFAULT_PROPERTIES_FILE
            if profile is None:
                profile = self.DEFAULT_PROFILE
            config = ConfigParser.ConfigParser()
            config.read(filename)
            self.username = config.get(profile,"username")
            self.password = config.get(profile,"password")
            self.base_url = config.get(profile,"base_url")
            self.auth_url = config.get(profile,"auth_url")
            self.client_id = config.get(profile,"client_id")
        except ConfigParser.Error as e:
            print(e)

#
# Api Class
#   Imports credentials using Credentials Class
#   Utilizes stored credentials to authenticate requests to Lotame Api
#   Provides helper methods for service authentication and api actions
#
class Api:

    # static class variables
    DEFAULT_PYTHON_HEADER={"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
    DEFAULT_JSON_RECEIVE_HEADER={'Accept':'application/json'}
    DEFAULT_JSON_SEND_HEADER={'Content-type': 'application/json', 'Accept':'application/json'}

    # initialization method
    # allows specification of custom properties file and profile
    # allows passing authentication parameters directly in lieu of properties file 
    def __init__(self, filename = None, profile = None, username = None, password = None, base_url = None, auth_url = None, client_id = None):
        credentials = Credentials(filename,profile)
        self.username = username or credentials.username
        self.password = password or credentials.password
        self.base_url = base_url or credentials.base_url
        self.auth_url = auth_url or credentials.auth_url
        self.client_id = client_id or credentials.client_id

    def buildServiceUrl(self, service = "", params = {}, auto_assign_client_id = True):
        if service == "":
            return ""
        url = self.base_url + service
        if auto_assign_client_id is True:
            url = url + "?client_id=" + str(self.client_id)
        for key, val in params.iteritems():
            if "?" not in url:
                url = url + "?" + str(key) + "=" + str(val)
            else:
                url = url + "&" + str(key) + "=" + str(val)
        return url

    def getTicketGrantingTicket(self, auth_url=None, user=None, password=None):
        if user is None:
            user = self.username
        if password is None:
            password = self.password
        if auth_url is None:
            auth_url = self.auth_url

        payload = {'username':user,'password':password}
        headers = self.DEFAULT_PYTHON_HEADER
        grantLocation = requests.post(auth_url, data=payload).headers['location']
        return grantLocation

    def getServiceTicket(self, service, grantLocation):
        payload = {'service': service}
        serviceTicket = requests.post( grantLocation, data=payload ).text
        return serviceTicket

    def initRequest(self, service, auth_url=None, user=None, password=None):
        grantLocation = self.getTicketGrantingTicket(auth_url,user,password)
        serviceTicket = self.getServiceTicket(service, grantLocation)
        return serviceTicket
     
    def get(self, service, auth_url=None, user=None, password=None):
        print "GET request " + service
        serviceTicket = self.initRequest(service, auth_url, user, password)
        headers = self.DEFAULT_JSON_RECEIVE_HEADER
        if '?' in service:
            response = requests.get( ('%s&ticket=%s') % (service, serviceTicket), headers=headers)
        else:
            response = requests.get( ('%s?ticket=%s') % (service, serviceTicket), headers=headers)
        data = response.json()
        #result = json.dumps(data, indent=4, sort_keys=True)
        return data

    def postBody(self, service, body, auth_url=None, user=None, password=None):
        print "POST request: " + service
        print "body: " + str(body)
        serviceTicket = self.initRequest(service, auth_url, user, password)
        headers = self.DEFAULT_JSON_SEND_HEADER
        if '?' in service:
            response = requests.post( ('%s&ticket=%s') % (service, serviceTicket), data=json.dumps(body), headers=headers)
        else:
            response = requests.post( ('%s?ticket=%s') % (service, serviceTicket), data=json.dumps(body), headers=headers)
        print response
        print "Finished."
        return response

    def post(self, service, auth_url=None, user=None, password=None):
        print "POST request: " + service
        serviceTicket = self.initRequest(service, auth_url, user, password)
        headers = self.DEFAULT_JSON_SEND_HEADER
        if '?' in service:
            response = requests.post( ('%s&ticket=%s') % (service, serviceTicket), headers=headers)
        else:
            response = requests.post( ('%s?ticket=%s') % (service, serviceTicket), headers=headers)
        print response
        print "Finished."
        return response

    def put(self, service, body, auth_url=None, user=None, password=None):
        print "POST request: " + service
        print "body: " + str(body)
        serviceTicket = self.initRequest(service, auth_url, user, password)
        headers = self.DEFAULT_JSON_SEND_HEADER
        if '?' in service:
            response = requests.put( ('%s&ticket=%s') % (service, serviceTicket), data=json.dumps(body), headers=headers)
        else:
            response = requests.put( ('%s?ticket=%s') % (service, serviceTicket), data=json.dumps(body), headers=headers)
        print response
        print "Finished."
        return response

    def delete(self, service, auth_url=None, user=None, password=None):
        print "DELETE request: " + service
        serviceTicket = self.initRequest(service, auth_url, user, password)
        headers = self.DEFAULT_JSON_RECEIVE_HEADER
        if '?' in service:
            response = requests.delete( ('%s&ticket=%s') % (service, serviceTicket), headers=headers)
        else:
            response = requests.delete( ('%s?ticket=%s') % (service, serviceTicket), headers=headers)
        print response
        print "Finished."
        return response