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

import argparse
import sys
import os

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
    print ""
    print "searching for firehose feed updates"

    parser = argparse.ArgumentParser(description='Process parameters for demo training')
    parser.add_argument('--data_path', dest='data_path', required=True,
                        help='the path to save the actual data')
    parser.add_argument('--mapping_path', dest='mapping_path', required=False, default=None,
                        help='path to save the mapping metadata to path')
    parser.add_argument('--hour', dest='hour', required=False, default=1,
                        help='default number of hour data to get')
    args = parser.parse_args()

    output_dir = args.data_path
    mapping_path = args.mapping_path
    hour = args.hour

    firehose = Lotame.FirehoseService()
    updates = firehose.getUpdates(hours=hour)

    print "found " + str(len(updates)) + "\n"

    if len(updates) == 0:
        sys.exit()

    if mapping_path:
        if os.path.isdir(mapping_path):
            print("mapping path exists, start to download mapping file, will overwrite the old file")
        else:
            print("mapping path not exists, create the directory first")
            os.system("mkdir -p %s" % mapping_path)

    mapping_download_finised = set([])
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
            bucket_name = str(re.search("(?<=s3:\/\/)([\w-]+)", feed_location).group(0))
            prefix = str(re.search("(?<=" + bucket_name + "\/)([\/\w-]+)", feed_location).group(0))
            print "processing feed " + str(feed_id)
            # print str(total_objects)+" new files"
            ProgressBar.print_progress(0, total_objects, prefix='\tprogress:', suffix='complete', bar_length=50)
            if mapping_path:
                mapping_file = feed.get('metaDataFile', '')
                # download the mapping file if we find the mapping path argument
                if mapping_file and mapping_file not in mapping_download_finised:
                    mapping_bucket_name = str(re.search("(?<=s3:\/\/)([\w-]+)", mapping_file).group(0))
                    mapping_key = str(re.search("(?<=" + mapping_bucket_name + "\/)(.+)", mapping_file).group(0))
                    mapping_name = str(re.search("[^\/]+$", mapping_file).group(0))
                    s3.Object(mapping_bucket_name, mapping_key).download_file(os.path.join(mapping_path, mapping_name))
                    mapping_download_finised.add(mapping_file)
            for i, file_object in enumerate(file_objects):
                key = prefix + "/" + file_object
                output = output_dir + file_object
                # print "\tdownloading "+output+"\n"
                s3.Object(bucket_name, key).download_file(output)
                ProgressBar.print_progress(i + 1, total_objects, prefix='\tprogress:', suffix='complete', bar_length=50)
            print "\t" + str(
                total_objects) + " files transferred from s3://" + bucket_name + "/" + prefix + " to " + output_dir + "\n"


if __name__ == '__main__':
    sys.exit(main())
