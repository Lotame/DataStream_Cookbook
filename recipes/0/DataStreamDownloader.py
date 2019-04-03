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